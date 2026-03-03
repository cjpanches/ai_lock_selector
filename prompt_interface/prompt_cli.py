#!/usr/bin/env python3
"""
AI Lock Selector - Prompt Interface CLI
Version: 2.0.0
Date: 2026-03-02

Утилита для управления мастер-промптами проекта.
Упрощённая версия: 4 актуальных промпта
"""

import os
import sys
import json
import shutil
import subprocess
import webbrowser
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional
import urllib.request

# Конфигурация
BASE_DIR = Path("/home/bot/projects/ai_lock_project")
PROMPT_DIR = BASE_DIR / "prompt_interface"
CURRENT_DIR = PROMPT_DIR / "_current"
TEMPLATES_DIR = PROMPT_DIR / "_templates"
HISTORY_DIR = PROMPT_DIR / "_history"
SYNC_DIR = PROMPT_DIR / "_sync"
IMPORTS_DIR = PROMPT_DIR / "_imports"
AI_RESPONSES_DIR = CURRENT_DIR / "AI_RESPONSES"

# Цвета для терминала
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_success(text: str):
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str):
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")


def print_info(text: str):
    print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")


def get_prompts(category: str = "current") -> list[dict]:
    """Получить список промптов по категории."""
    if category == "current":
        directory = CURRENT_DIR
    elif category == "templates":
        directory = TEMPLATES_DIR
    elif category == "history":
        directory = HISTORY_DIR
    else:
        directory = CURRENT_DIR
    
    prompts = []
    if directory.exists():
        for f in directory.rglob("*.md"):
            prompts.append({
                "name": f.stem,
                "path": str(f),
                "category": category,
                "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            })
    return sorted(prompts, key=lambda x: x["name"])


def list_prompts(category: str = "current"):
    """Показать список промптов."""
    prompts = get_prompts(category)
    
    if not prompts:
        print_error(f"Промпты категории '{category}' не найдены")
        return
    
    print_header(f"📋 Промпты ({category})")
    
    emoji = {
        "AI_MASTER": "🤖",
        "STARTUP": "🚀",
        "AUDIT": "🔍",
        "FIX_BUG": "📝",
    }
    
    for i, p in enumerate(prompts, 1):
        e = emoji.get(p['name'], "📄")
        status = "⭐" if category == "current" else "📋"
        print(f"  {i}. {e} {p['name']} {status}")
        print(f"     {p['modified']}")
    print()


def copy_prompt(name: str) -> bool:
    """Копировать промпт в буфер обмена."""
    prompts = get_prompts("current")
    
    # Поиск по имени (case insensitive)
    matches = [p for p in prompts if name.lower() in p["name"].lower()]
    
    if not matches:
        print_error(f"Промпт '{name}' не найден")
        print_info("Доступные промпты:")
        list_prompts("current")
        return False
    
    if len(matches) > 1:
        print_error(f"Найдено несколько совпадений:")
        for m in matches:
            print(f"  - {m['name']}")
        return False
    
    prompt_path = Path(matches[0]["path"])
    content = prompt_path.read_text()
    
    # Копируем в буфер (xsel для Linux)
    try:
        subprocess.run(["xsel", "--clipboard", "--input"], input=content.encode(), check=True)
        print_success(f"Скопировано в буфер: {matches[0]['name']}")
        return True
    except FileNotFoundError:
        # Альтернатива: xclip
        try:
            subprocess.run(["xclip", "-selection", "clipboard"], input=content.encode(), check=True)
            print_success(f"Скопировано в буфер: {matches[0]['name']}")
            return True
        except:
            # Выводим в stdout если нет буфера
            print(f"\n{Colors.WARNING}Буфер недоступен. Содержимое:{Colors.ENDC}\n")
            print(content)
            return True


def show_prompt(name: str):
    """Показать содержимое промпта."""
    prompts = get_prompts("current")
    matches = [p for p in prompts if name.lower() in p["name"].lower()]
    
    if not matches:
        print_error(f"Промпт '{name}' не найден")
        return
    
    prompt_path = Path(matches[0]["path"])
    print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.CYAN}{prompt_path.name}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'='*60}{Colors.ENDC}\n")
    print(prompt_path.read_text())


def export_prompt(name: str, format: str = "txt") -> bool:
    """Экспортировать промпт в txt файл."""
    prompts = get_prompts("current")
    matches = [p for p in prompts if name.lower() in p["name"].lower()]
    
    if not matches:
        print_error(f"Промпт '{name}' не найден")
        return False
    
    prompt_path = Path(matches[0]["path"])
    content = prompt_path.read_text()
    
    # Убираем yaml frontmatter для чистого txt
    lines = content.split('\n')
    if lines[0] == '---':
        # Находим вторую ---
        start = 1
        for i, line in enumerate(lines[1:], 1):
            if line == '---':
                start = i + 1
                break
        content = '\n'.join(lines[start:])
    
    # Сохраняем
    export_dir = CURRENT_DIR / "exports"
    export_dir.mkdir(exist_ok=True)
    
    export_file = export_dir / f"{name}.txt"
    export_file.write_text(content)
    
    print_success(f"Экспортировано: {export_file}")
    return True


def search_prompts(query: str):
    """Поиск по промптам."""
    print_header(f"🔍 Поиск: '{query}'")
    
    all_prompts = get_prompts("current") + get_prompts("templates")
    results = []
    
    for p in all_prompts:
        content = Path(p["path"]).read_text()
        if query.lower() in content.lower():
            results.append(p)
    
    if not results:
        print_error("Ничего не найдено")
        return
    
    print(f"Найдено {len(results)} результатов:\n")
    for r in results:
        print(f"  📄 {r['name']} ({r['category']})")


def save_ai_response(content: str, name: str | None = None) -> bool:
    """Сохранить ответ от AI."""
    AI_RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    
    if not name:
        now = datetime.now()
        name = now.strftime("%Y%m%d_%H%M%S")
    
    response_file = AI_RESPONSES_DIR / f"response_{name}.txt"
    response_file.write_text(content)
    
    print_success(f"Сохранено: {response_file}")
    return True


def list_ai_responses():
    """Показать сохранённые ответы AI."""
    if not AI_RESPONSES_DIR.exists():
        print_info("Ответов пока нет")
        return
    
    responses = sorted(AI_RESPONSES_DIR.glob("*.txt"), key=lambda f: f.stat().st_mtime, reverse=True)
    
    if not responses:
        print_info("Ответов пока нет")
        return
    
    print_header("💾 Сохранённые ответы AI")
    
    for r in responses:
        mtime = datetime.fromtimestamp(r.stat().st_mtime)
        size = r.stat().st_size
        print(f"  📄 {r.name}")
        print(f"     {mtime.strftime('%Y-%m-%d %H:%M')} | {size} bytes")
    print()


def show_help():
    """Показать справку."""
    help_text = """
🎯 AI Lock Selector - Prompt Interface CLI v2.0

Использование: prompt_cli.py <команда> [аргументы]

📋 КОМАНДЫ:

  Работа с промптами:
    list [category]           Список промптов
    copy <name>              Копировать промпт в буфер
    show <name>              Показать содержимое промпта
    export <name>            Экспортировать в .txt
    search <query>           Поиск по промптам
    
  Ответы AI:
    responses                 Список сохранённых ответов
    save <текст>             Сохранить ответ от AI
    
  Другое:
    status                   Статус системы
    help                     Эта справка

📂 КАТЕГОРИИ:
  current    - Актуальные промпты (4 шт)
  templates  - Шаблоны

🤖 ДОСТУПНЫЕ ПРОМПТЫ:
  🤖 AI_MASTER   - Универсальный для любого AI
  🚀 STARTUP     - Контекст проекта
  🔍 AUDIT       - Шаблон аудита
  📝 FIX_BUG     - Шаблон бага

🔗 БЫСТРЫЕ ССЫЛКИ:
  Dashboard:     http://localhost:8081/prompt_dashboard.html
  Status:       http://localhost:8080/ai_lock_project_status.html
  Backend API:  http://localhost:8001

"""
    print(help_text)


def main():
    parser = argparse.ArgumentParser(description="Prompt Interface CLI v2.0")
    parser.add_argument("command", nargs="?", default="help")
    parser.add_argument("arg1", nargs="?", default="")
    parser.add_argument("arg2", nargs="?", default="")
    
    args = parser.parse_args()
    
    # Выполняем команду
    if args.command == "list":
        list_prompts(args.arg1 or "current")
    
    elif args.command == "copy":
        if not args.arg1:
            print_error("Укажите имя промпта")
            print_info("prompt_cli.py copy AI_MASTER")
        else:
            copy_prompt(args.arg1)
    
    elif args.command == "show":
        if not args.arg1:
            print_error("Укажите имя промпта")
        else:
            show_prompt(args.arg1)
    
    elif args.command == "export":
        if not args.arg1:
            print_error("Укажите имя промпта")
        else:
            export_prompt(args.arg1)
    
    elif args.command == "search":
        if not args.arg1:
            print_error("Укажите запрос")
        else:
            search_prompts(args.arg1)
    
    elif args.command == "responses":
        list_ai_responses()
    
    elif args.command == "save":
        if not args.arg1:
            print_error("Укажите текст или имя файла")
        else:
            save_ai_response(args.arg1)
    
    elif args.command == "status":
        print_header("📊 Status v2.0")
        print(f"Prompt Directory: {PROMPT_DIR}")
        print(f"Current Prompts: {len(get_prompts('current'))}")
        print(f"Templates: {len(get_prompts('templates'))}")
        
        if AI_RESPONSES_DIR.exists():
            responses = len(list(AI_RESPONSES_DIR.glob("*.txt")))
            print(f"AI Responses: {responses}")
        
        print("\nАктуальные промпты:")
        for p in get_prompts('current'):
            print(f"  - {p['name']}")
    
    elif args.command in ["help", "-h", "--help"]:
        show_help()
    
    else:
        print_error(f"Неизвестная команда: {args.command}")
        print_info("Используйте: prompt_cli.py help")


if __name__ == "__main__":
    main()
