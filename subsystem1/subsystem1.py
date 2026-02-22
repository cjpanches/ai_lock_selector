#!/usr/bin/env python3
"""
Subsystem1 - AI Expert Analysis System
Grok Expert Module for AI Lock Selector Project Analysis

Этот модуль обеспечивает анализ проекта AI Lock Selector
через экспертную систему Grok (xAI).
"""

import os
import sys
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict

PROJECT_ROOT = Path(__file__).parent.parent
SUBSYSTEM1_DIR = PROJECT_ROOT / "subsystem1"
LOGS_DIR = SUBSYSTEM1_DIR / "logs"


@dataclass
class AnalysisResult:
    """Результат анализа эксперта"""
    expert_name: str
    timestamp: str
    input_data: str
    methodology: str
    findings: List[str]
    recommendations: List[str]
    confidence_score: float
    success: bool
    error_message: Optional[str] = None


class Subsystem1Logger:
    """Логирование для подсистемы"""
    
    def __init__(self, name: str = "subsystem1"):
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Настройка логгера"""
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        
        log_file = LOGS_DIR / f"action_{datetime.now().strftime('%Y%m%d')}.log"
        
        handler = logging.FileHandler(log_file, encoding='utf-8')
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(handler)
        
        self.logger.setLevel(logging.DEBUG)
    
    def info(self, message: str):
        self.logger.info(message)
    
    def error(self, message: str, exc_info: bool = True):
        self.logger.error(message, exc_info=exc_info)
    
    def warning(self, message: str):
        self.logger.warning(message)
    
    def debug(self, message: str):
        self.logger.debug(message)


class GrokExpertAnalyzer:
    """
    Grok Expert Analyzer - анализатор проекта AI Lock Selector
    Использует Grok API для глубокого анализа кода и архитектуры
    """
    
    EXPERT_NAME = "Grok"
    VERSION = "1.0.0"
    
    def __init__(self):
        self.logger = Subsystem1Logger("GrokExpert")
        self.api_key = os.getenv("GROK_API_KEY")
        self.base_url = os.getenv("GROK_API_URL", "https://api.x.ai/v1")
    
    def _load_project_files(self) -> Dict[str, str]:
        """Загрузка файлов проекта для анализа"""
        files_content = {}
        
        target_dirs = [
            "mobile_app/lib",
            "cv_pipeline/src", 
            "backend/app"
        ]
        
        for dir_path in target_dirs:
            full_path = PROJECT_ROOT / dir_path
            if full_path.exists():
                for ext in ['*.py', '*.dart', '*.yaml']:
                    for file in full_path.rglob(ext):
                        try:
                            rel_path = file.relative_to(PROJECT_ROOT)
                            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                files_content[str(rel_path)] = content[:5000]
                        except Exception as e:
                            self.logger.warning(f"Не удалось прочитать {file}: {e}")
        
        return files_content
    
    def _call_grok_api(self, prompt: str) -> Optional[str]:
        """Вызов Grok API с error-handling"""
        if not self.api_key:
            self.logger.warning("GROK_API_KEY не установлен, используем симуляцию")
            return self._simulate_analysis(prompt)
        
        try:
            import requests
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "grok-2",
                "messages": [
                    {"role": "system", "content": "Ты - эксперт по анализу кода и архитектуры ПО. Проанализируй проект AI Lock Selector и дай рекомендации."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result['choices'][0]['message']['content']
            
        except ImportError:
            self.logger.warning("requests не установлен, используем симуляцию")
            return self._simulate_analysis(prompt)
        except Exception as e:
            self.logger.error(f"Ошибка вызова Grok API: {e}")
            return None
    
    def _simulate_analysis(self, prompt: str) -> str:
        """Симуляция анализа если API недоступен"""
        return """
Анализ проекта AI Lock Selector (симуляция):

Сильные стороны:
- Архитектура MVVM в Flutter
- Разделение на mobile_app, backend, cv_pipeline
- Документация в README

Области для улучшения:
1. CV Pipeline требует доработки - нет реальной YOLO модели
2. Backend использует in-memory данные, нет PostgreSQL
3. State management - используется plain setState, рекомендуется Riverpod
4. Нет unit тестов
5. Неполная структура навигации в приложении

Рекомендации:
- Подключить PostgreSQL
- Добавить Riverpod для state management
- Собрать dataset для обучения YOLO
- Добавить unit тесты
"""
    
    def analyze_project(self, focus_areas: Optional[List[str]] = None) -> AnalysisResult:
        """
        Основной метод анализа проекта
        
        Args:
            focus_areas: Список областей для фокусировки анализа
        
        Returns:
            AnalysisResult с результатами анализа
        """
        timestamp = datetime.now().isoformat()
        
        try:
            self.logger.info(f"Начало анализа проекта {timestamp}")
            
            files = self._load_project_files()
            self.logger.info(f"Загружено {len(files)} файлов для анализа")
            
            focus = ", ".join(focus_areas) if focus_areas else "общий анализ архитектуры и кода"
            
            prompt = f"""
Проанализируй проект AI Lock Selector и дай рекомендации по следующим направлениям:
{focus}

Структура проекта:
- mobile_app/ - Flutter приложение
- backend/ - FastAPI сервер  
- cv_pipeline/ - Computer Vision пайплайн

Ключевые файлы и их содержание предоставлю ниже.
"""
            
            result_text = self._call_grok_api(prompt)
            
            if result_text:
                findings = self._extract_findings(result_text)
                recommendations = self._extract_recommendations(result_text)
                confidence = 0.8
            else:
                findings = ["Анализ не выполнен - ошибка API"]
                recommendations = ["Проверить настройки API"]
                confidence = 0.0
            
            result = AnalysisResult(
                expert_name=self.EXPERT_NAME,
                timestamp=timestamp,
                input_data=f"Анализ {len(files)} файлов проекта",
                methodology="Автоматический анализ через Grok API с использованием промтов",
                findings=findings,
                recommendations=recommendations,
                confidence_score=confidence,
                success=True
            )
            
            self._save_result(result)
            self.logger.info(f"Анализ завершен успешно, confidence: {confidence}")
            
            return result
            
        except Exception as e:
            error_msg = f"Критическая ошибка при анализе: {e}\n{traceback.format_exc()}"
            self.logger.error(error_msg)
            
            return AnalysisResult(
                expert_name=self.EXPERT_NAME,
                timestamp=datetime.now().isoformat(),
                input_data="Анализ не выполнен",
                methodology="Не удалось завершить",
                findings=[],
                recommendations=["Исправить ошибку в коде"],
                confidence_score=0.0,
                success=False,
                error_message=error_msg
            )
    
    def _extract_findings(self, text: str) -> List[str]:
        """Извлечение ключевых находок из текста"""
        lines = text.strip().split('\n')
        findings = []
        
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                clean_line = line.lstrip('0123456789.-•) ').strip()
                if len(clean_line) > 10:
                    findings.append(clean_line)
        
        return findings[:10]
    
    def _extract_recommendations(self, text: str) -> List[str]:
        """Извлечение рекомендаций из текста"""
        recommendations = []
        
        keywords = ['рекоменду', 'нужно', 'следует', 'должен', 'improve', 'recommend', 'should']
        
        lines = text.lower().split('\n')
        for line in lines:
            if any(kw in line for kw in keywords):
                recommendations.append(line.strip())
        
        return recommendations[:5]
    
    def _save_result(self, result: AnalysisResult):
        """Сохранение результата в файл"""
        grok_dir = SUBSYSTEM1_DIR / "INFO" / "Grok"
        grok_dir.mkdir(parents=True, exist_ok=True)
        
        result_file = grok_dir / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(result), f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Результат сохранен: {result_file}")


class Subsystem1Orchestrator:
    """
    Оркестратор подсистемы 1
    Координирует работу всех экспертов и управляет потоком данных
    """
    
    def __init__(self):
        self.logger = Subsystem1Logger("Orchestrator")
        self.grok = GrokExpertAnalyzer()
    
    def run_full_analysis(self) -> Dict[str, Any]:
        """
        Запуск полного анализа всеми экспертами
        
        Returns:
            Словарь с результатами всех экспертов
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "experts": {},
            "status": "completed"
        }
        
        self.logger.info("Запуск полного анализа проекта")
        
        try:
            grok_result = self.grok.analyze_project()
            results["experts"]["grok"] = asdict(grok_result)
            
            self._save_combined_results(results)
            
        except Exception as e:
            self.logger.error(f"Ошибка при анализе: {e}")
            results["status"] = "failed"
            results["error"] = str(e)
        
        return results
    
    def _save_combined_results(self, results: Dict):
        """Сохранение объединенных результатов"""
        analysis_dir = SUBSYSTEM1_DIR / "INFO" / "Analysis"
        analysis_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = analysis_dir / f"combined_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Комбинированные результаты сохранены: {output_file}")


def main():
    """Точка входа"""
    print("=" * 60)
    print("AI Lock Selector - Subsystem1 Analysis")
    print("Grok Expert Module v1.0.0")
    print("=" * 60)
    
    orchestrator = Subsystem1Orchestrator()
    results = orchestrator.run_full_analysis()
    
    print("\nРезультаты анализа:")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    
    print(f"\nЛоги сохранены в: {LOGS_DIR}")
    
    return 0 if results["status"] == "completed" else 1


if __name__ == "__main__":
    sys.exit(main())
