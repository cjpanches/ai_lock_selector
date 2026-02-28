# AI Lock Selector - YOLO Dataset

## Структура датасета

```
dataset/
├── images/
│   ├── train/      # Обучающие изображения (~80%)
│   └── val/        # Валидационные изображения (~20%)
├── labels/
│   ├── train/      # Аннотации YOLO формата
│   └── val/
├── classes.txt     # Список классов
└── lock_dataset.yaml  # Конфиг для YOLO
```

## Классы для разметки

| ID | Класс | Описание |
|----|-------|----------|
| 0 | lock_plate | Вся планка замка |
| 1 | cylinder_hole | Отверстие цилиндра (DIN) |
| 2 | mounting_hole | Крепёжные отверстия |
| 3 | handle_square | Квадрат ручки |

## Формат аннотаций (YOLO)

Каждому изображению соответствует `.txt` файл с таким форматом:
```
# class_id x_center y_center width height (все значения 0.0 - 1.0)
0 0.5 0.3 0.2 0.8   # lock_plate
1 0.5 0.1 0.05 0.1  # cylinder_hole
2 0.3 0.5 0.02 0.02 # mounting_hole
2 0.7 0.5 0.02 0.02 # mounting_hole
3 0.5 0.2 0.03 0.03 # handle_square
```

## Как добавить изображения

### Вариант 1: Собственные фото
1. Сделайте фото замка сверху (плоский ракурс)
2. Положите в `images/train/` или `images/val/`
3. Разметьте вручную (Roboflow, LabelImg, CVAT)
4. Сохраните аннотации в `labels/train/` или `labels/val/`

### Вариант 2: Пре-разметка CV pipeline
```bash
cd cv_pipeline
python pre_label.py --input images/train --output labels/train
```

## Требования к изображениям

- Разрешение: минимум 640x640
- Формат: JPG или PNG
- Освещение: хорошее, равномерное
- Ракурс: вид сверху (плоский)
- Фон: контрастный

## Ссылки

- [Roboflow](https://roboflow.com) - онлайн разметка
- [LabelImg](https://github.com/tzutalin/labelImg) - десктоп разметка
- [Ultralytics YOLO](https://docs.ultralytics.com) - документация
