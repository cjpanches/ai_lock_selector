---
title: "TEMPLATE - Шаблон промпта"
version: "1.0"
date_created: "2026-03-01"
status: "TEMPLATE"
direction: "template"
---

# TEMPLATE - [Название промпта]

## Когда использовать

[Описание когда использовать этот промпт]

## Структура

```markdown
---
title: "Название"
version: "1.0"
date_created: "YYYY-MM-DD"
status: "ACTIVE"
direction: "user_to_opencode | user_to_experts | external"
expert: "KIMI | GROK | GPT | GEMINI | CLAUDE | ..."
---

# Основной контент

## Раздел 1
[Контент]

## Раздел 2
[Контент]
```

## Поля метаданных

| Поле | Описание |
|------|----------|
| title | Название промпта |
| version | Версия semver |
| date_created | Дата создания |
| status | ACTIVE / ARCHIVED / TEMPLATE |
| direction | Направление (user→AI или AI→user) |
| expert | Имя эксперта (если применимо) |

## Примеры

См. _current/ для реальных примеров.
