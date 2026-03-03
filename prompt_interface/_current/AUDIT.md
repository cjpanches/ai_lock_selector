---
title: "AUDIT - Запрос на аудит проекта"
version: "1.0"
date_created: "2026-03-01"
status: "ACTIVE"
direction: "user_to_opencode"
---

# Запрос на аудит проекта AI Lock Selector

## Цель аудита

Провести комплексный аудит проекта включая:
1. Внутренних экспертов (AI_EXPERTS)
2. Мастер-систему
3. Поиск неисправностей и конфликтов
4. Анализ связей между компонентами
5. Оценка готовности проекта

## Компоненты для аудита

| Компонент | Директория |
|-----------|------------|
| Mobile App | mobile_app/ |
| Backend | backend/ |
| CV Pipeline | cv_pipeline/ |
| Database | backend/locks.db |
| AI Experts | AI_EXPERTS/ |
| AR Mask | mask/ |

## Ожидаемый результат

- Список найденных багов с приоритетами
- Анализ конфликтов между компонентами
- Рекомендации по исправлениям
- Оценка готовности проекта (0-10)

## Известные проблемы (для проверки)

1. pre_label.py - hardcoded scale_factor = 15.0
2. measurement_service.py - undefined variables
3. YOLO не обучен
4. cv_service.py - stub implementation
