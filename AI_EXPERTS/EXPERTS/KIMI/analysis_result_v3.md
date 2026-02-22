# ЭКСПЕРТ: KIMI (ARCHITECT)
## Дата: 2026-02-22
## Версия: 3.0.0

### Выводы

Авто-alignment функция реализована с применением корректной архитектуры: Flutter-клиент взаимодействует с CV-бэкеном через `cvServiceProvider`, результаты детекции трансформируются в координаты экрана через `MaskNotifier.applyAutoDetection()`. Использование Riverpod для state management соответствует современным Flutter-практикам. Однако выявлены критические проблемы с координатными преобразованиями и обработкой ошибок, требующие немедленного исправления перед релизом.

### Проблемы

1. **Ошибка трансформации координат** - Критическое влияние на функциональность auto-alignment. В `ar_camera_screen.dart:236-238` используется `previewSize.height` как ширина и `previewSize.width` как высота, что некорректно для большинства камер. PreviewSize уже учитывает ориентацию устройства. **Приоритет: P0**

2. **Неиспользуемый confidence из CV** - Среднее влияние. Метод `applyAutoDetection` принимает `confidence` параметр, но не использует его для `alignmentScore`. Это снижает точность оценки совмещения маски. **Приоритет: P1**

3. **Отсутствие retry логики** - Среднее влияние. При неудаче auto-detection пользователь получает только уведомление, без возможности повторной попытки или ручной корректировки позиции. **Приоритет: P1**

4. **Synchronous UI update during async operation** - Среднее влияние. В `_runAutoDetect` состояние `isAutoDetecting` устанавливается после начала async операции, что может привести к race conditions. **Приоритет: P2**

5. **Отсутствие unit-тестов для MaskNotifier** - Среднее влияние. Новая функциональность `applyAutoDetection` не покрыта тестами, что повышает риск регрессий. **Приоритет: P2**

6. **Hardcoded значения масштабирования** - Низкое влияние. В `mask_provider.dart:89` используется hardcoded `targetWidthPx = 150.0`, что не учитывает различные размеры экранов. **Приоритет: P3**

### Рекомендации

1. **Исправить трансформацию координат** - Сложность: Средняя - Владелец: GROK/Flutter team
   - Заменить `controller.value.previewSize.height/width` на корректное получение размеров превью
   - Добавить логирование для отладки координат

2. **Интегрировать confidence в alignmentScore** - Сложность: Низкая - Владелец: KIMI
   - Модифицировать `applyAutoDetection` для установки `alignmentScore` на основе confidence
   - Добавить: `alignmentScore: confidence ?? 0.5`

3. **Добавить retry и fallback UI** - Сложность: Средняя - Владелец: Flutter team
   - Реализовать кнопку повторной попытки в snackbar
   - Предоставить визуальный feedback для ручной корректировки

4. **Добавить тесты для MaskNotifier** - Сложность: Низкая - Владелец: QA
   - Создать `mask_provider_auto_detect_test.dart`
   - Покрыть edge cases: zero-sized bounding box, extreme aspect ratios

5. **Вынести константы в config** - Сложность: Низкая - Владелец: Flutter team
   - Извлечь `targetWidthPx`, масштабы в `constants.dart`
   - Сделать адаптивными под размер устройства

6. **Добавить timeout для CV запросов** - Сложность: Низкая - Владелец: Backend team
   - Ограничить время ожидания ответа от CV сервиса
   - Добавить CancelToken для возможности отмены

### Оценка компонентов

| Компонент | Оценка | Комментарий |
|-----------|--------|------------|
| Auto-alignment architecture | 7/10 | Корректная архитектура с clear separation of concerns |
| CV integration | 6/10 | Базовое интеграция работает, но lacks resilience |
| State management (Riverpod) | 8/10 | Правильное использование StateNotifierProvider |
| Error handling | 4/10 | Критически недостаточная обработка ошибок |
| Coordinate transformation | 3/10 | Неправильная логика преобразования координат |
| Test coverage (new feature) | 2/10 | Отсутствуют тесты для auto-alignment |
| UI/UX for auto-detection | 7/10 | Хороший визуальный feedback для пользователя |
| Backend CV API | 6/10 | API functional, но требует улучшений latency |
| Performance | 7/10 | Анимации плавные, но есть room для optimization |
| Overall | 6/10 | Функция работоспособна, но требует стабилизации |

---

**Рекомендуемые следующие шаги:**
1. P0: Исправить координатную трансформацию перед тестированием
2. P1: Интегрировать confidence score
3. P1: Добавить unit-тесты для MaskNotifier
4. P2: Вынести hardcoded значения в конфигурацию
