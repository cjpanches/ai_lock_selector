"""
Unit tests for Subsystem1 - AI Expert Analysis System

Run with: pytest test_subsystem1.py -v
"""

import os
import sys
import json
import tempfile
import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent))

from subsystem1 import (
    AnalysisResult,
    Subsystem1Logger,
    GrokExpertAnalyzer,
    Subsystem1Orchestrator,
    SUBSYSTEM1_DIR,
    LOGS_DIR
)


class TestAnalysisResult:
    """Тесты для AnalysisResult"""
    
    def test_create_analysis_result(self):
        """Тест создания результата анализа"""
        result = AnalysisResult(
            expert_name="TestExpert",
            timestamp="2024-01-01T00:00:00",
            input_data="test input",
            methodology="test method",
            findings=["finding 1", "finding 2"],
            recommendations=["rec 1"],
            confidence_score=0.8,
            success=True
        )
        
        assert result.expert_name == "TestExpert"
        assert result.confidence_score == 0.8
        assert result.success is True
        assert len(result.findings) == 2
    
    def test_analysis_result_to_dict(self):
        """Тест конвертации в словарь"""
        result = AnalysisResult(
            expert_name="Test",
            timestamp="2024-01-01",
            input_data="input",
            methodology="method",
            findings=[],
            recommendations=[],
            confidence_score=0.5,
            success=True
        )
        
        data = result.__dict__
        assert "expert_name" in data
        assert data["expert_name"] == "Test"


class TestSubsystem1Logger:
    """Тесты для логгера"""
    
    def test_logger_creation(self):
        """Тест создания логгера"""
        logger = Subsystem1Logger("test_logger")
        assert logger.logger is not None
        assert logger.logger.name == "test_logger"
    
    def test_log_directory_created(self):
        """Тест создания директории для логов"""
        assert LOGS_DIR.exists()
        assert LOGS_DIR.is_dir()


class TestGrokExpertAnalyzer:
    """Тесты для Grok анализатора"""
    
    @pytest.fixture
    def analyzer(self):
        """Фикстура для анализатора"""
        return GrokExpertAnalyzer()
    
    def test_analyzer_creation(self, analyzer):
        """Тест создания анализатора"""
        assert analyzer.EXPERT_NAME == "Grok"
        assert analyzer.logger is not None
    
    def test_extract_findings(self, analyzer):
        """Тест извлечения находок"""
        text = """
Некоторый анализ текста:
1. Первая находка
2. Вторая находка
- Третья находка
• Четвертая находка
        """
        findings = analyzer._extract_findings(text)
        
        assert len(findings) > 0
        assert any("находка" in f.lower() for f in findings)
    
    def test_extract_recommendations(self, analyzer):
        """Тест извлечения рекомендаций"""
        text = """
Нужно улучшить код
Следует добавить тесты
Рекомендуется использовать Riverpod
        """
        recs = analyzer._extract_recommendations(text)
        
        assert len(recs) > 0
    
    def test_analyze_project_without_api(self, analyzer):
        """Тест анализа без API ключа"""
        result = analyzer.analyze_project()
        
        assert result.success is True
        assert result.expert_name == "Grok"
        assert result.confidence_score > 0
    
    def test_simulate_analysis(self, analyzer):
        """Тест симуляции анализа"""
        result = analyzer._simulate_analysis("test prompt")
        
        assert result is not None
        assert len(result) > 0


class TestSubsystem1Orchestrator:
    """Тесты для оркестратора"""
    
    @pytest.fixture
    def orchestrator(self):
        """Фикстура для оркестратора"""
        return Subsystem1Orchestrator()
    
    def test_orchestrator_creation(self, orchestrator):
        """Тест создания оркестратора"""
        assert orchestrator.grok is not None
        assert orchestrator.logger is not None
    
    def test_run_full_analysis(self, orchestrator):
        """Тест запуска полного анализа"""
        results = orchestrator.run_full_analysis()
        
        assert "timestamp" in results
        assert "experts" in results
        assert "grok" in results["experts"]
        assert results["status"] == "completed"


class TestIntegration:
    """Интеграционные тесты"""
    
    def test_full_workflow(self):
        """Тест полного рабочего процесса"""
        orchestrator = Subsystem1Orchestrator()
        
        results = orchestrator.run_full_analysis()
        
        assert results["status"] == "completed"
        assert results["experts"]["grok"]["success"] is True
    
    def test_result_saved_to_file(self):
        """Тест сохранения результата в файл"""
        grok_dir = SUBSYSTEM1_DIR / "INFO" / "Grok"
        
        assert grok_dir.exists()
        
        json_files = list(grok_dir.glob("analysis_*.json"))
        assert len(json_files) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
