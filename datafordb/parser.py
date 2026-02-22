#!/usr/bin/env python3
"""
Parser for goodlock.ru HTML catalog
Extracts lock data from HTML files
"""

import os
import re
import csv
from pathlib import Path
from typing import Dict, List, Optional
from html.parser import HTMLParser


class LockTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_tbody = False
        self.in_tr = False
        self.in_td = False
        self.current_row = []
        self.current_key = ""
        self.current_value = ""
        self.data: Dict[str, str] = {}
        self.in_title = False
        self.in_h1 = False
        self.title = ""
        self.h1 = ""
    
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == "h1":
            self.in_h1 = True
        
        if tag == "table":
            self.in_table = True
            self.in_tbody = False
        
        if tag == "tbody" and self.in_table:
            self.in_tbody = True
        
        if tag == "tr" and self.in_tbody:
            self.in_tr = True
            self.current_row = []
        
        if tag == "td" and self.in_tr:
            self.in_td = True
    
    def handle_endtag(self, tag):
        if tag == "h1":
            self.in_h1 = False
        
        if tag == "table":
            self.in_table = False
            self.in_tbody = False
        
        if tag == "tr" and self.in_tr:
            self.in_tr = False
            if len(self.current_row) >= 2:
                key = self.current_row[0].strip()
                value = self.current_row[1].strip()
                if key and value:
                    self.data[key] = value
            self.current_row = []
        
        if tag == "td" and self.in_td:
            self.in_td = False
    
    def handle_data(self, data):
        if self.in_h1:
            self.h1 += data
        
        if self.in_td:
            self.current_row.append(data)


def parse_lock_html(file_path: str) -> Optional[Dict]:
    """Parse a single lock HTML file."""
    try:
        with open(file_path, 'r', encoding='iso-8859-1', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
    
    try:
        content = content.encode('iso-8859-1').decode('windows-1251')
    except Exception:
        pass
    
    parser = LockTableParser()
    try:
        parser.feed(content)
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None
    
    return {
        'name': parser.h1.strip() if parser.h1 else Path(file_path).stem,
        'specs': parser.data
    }


def extract_technical_fields(specs: Dict[str, str]) -> Dict:
    """Extract standardized fields from specs."""
    
    field_map = {
        'Удаление ключевого отверстия (Backset)': 'backset',
        'Межосевое расстояние': 'center_distance',
        'Ширина планки': 'plate_width',
        'Высота планки': 'plate_height',
        'Толщина планки': 'plate_thickness',
        'Ширина корпуса': 'body_width',
        'Высота корпуса': 'body_height',
        'Глубина корпуса': 'body_depth',
        'Диаметр цилиндра': 'cylinder_hole_diameter',
        'Размер квадрата': 'square_hole_size',
        'Тип упаковки': 'package_type',
        'Назначение': 'purpose',
        'Тип крепления': 'mounting_type',
        'Тип ригелей': 'bolt_type',
        'Количество ригелей': 'bolt_count',
        'Вылет ригелей': 'bolt_throw',
        'Диаметр ригеля': 'bolt_diameter',
        'Тип механизма секретности': 'mechanism_type',
        'Тип ключа': 'key_type',
        'Количество ключей': 'key_count',
        'Комплектация цилиндром': 'cylinder_included',
        'Типоразмер цилиндра': 'cylinder_size',
        'Материал цилиндра': 'cylinder_material',
    }
    
    result = {}
    for orig_key, std_key in field_map.items():
        value = specs.get(orig_key, '')
        if value:
            result[std_key] = value
    
    return result


def parse_lock_name(name: str) -> Dict:
    """Parse lock name to extract brand and series."""
    result = {
        'brand': '',
        'series': '',
        'color': ''
    }
    
    brand_match = re.search(r'(Apecs|ABUS|Mottura|KALE|MOIA|Amig|Avers|Vanger|dormakaba)', name, re.IGNORECASE)
    if brand_match:
        result['brand'] = brand_match.group(1)
    
    series_match = re.search(r'(\d+[\d/]*)', name)
    if series_match:
        result['series'] = series_match.group(1)
    
    color_match = re.search(r'(CR|G|AB|AC|NI|NIS|GM|SG|TO)', name)
    if color_match:
        result['color'] = color_match.group(1)
    
    return result


def parse_all_locks(data_dir: str) -> List[Dict]:
    """Parse all lock HTML files in directory."""
    locks = []
    
    html_files = list(Path(data_dir).glob("*.html"))
    print(f"Found {len(html_files)} HTML files")
    
    for html_file in html_files:
        if ':Zone.Identifier' in str(html_file):
            continue
            
        data = parse_lock_html(str(html_file))
        if not data:
            continue
        
        name_info = parse_lock_name(data['name'])
        tech_fields = extract_technical_fields(data['specs'])
        
        lock = {
            'vendor_code': html_file.stem[:50],
            'name': data['name'],
            'brand': name_info['brand'],
            'series': name_info['series'],
            'color': name_info['color'],
            **tech_fields
        }
        
        locks.append(lock)
    
    return locks


def save_to_csv(locks: List[Dict], output_file: str):
    """Save parsed locks to CSV."""
    if not locks:
        print("No locks to save")
        return
    
    fieldnames = list(locks[0].keys())
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(locks)
    
    print(f"Saved {len(locks)} locks to {output_file}")


if __name__ == "__main__":
    import sys
    
    data_dir = "/home/bot/porojects/ai_lock_project/datafordb/2/3"
    output_file = "/home/bot/porojects/ai_lock_project/datafordb/locks_parsed.csv"
    
    locks = parse_all_locks(data_dir)
    print(f"\nParsed {len(locks)} locks")
    
    if locks:
        print("\nSample lock:")
        print(locks[0])
        
        save_to_csv(locks, output_file)
