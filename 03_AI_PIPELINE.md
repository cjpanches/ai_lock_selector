# AI Pipeline - цепочка обработки

## 1. Входные данные
- Изображение с камеры (JPEG/PNG)
- Масштаб (pixels/mm) из AR-маски

## 2. Этапы обработки

### Этап 1: Предобработка изображения
```
image → grayscale → gaussian_blur → canny_edges
```

### Этап 2: Контурный анализ
```
edges → findContours → filter_by_area → classify_contours
```

### Этап 3: Поиск ключевых элементов
- Планка замка (наибольший прямоугольный контур)
- Отверстие цилиндра (из центра маски)
- Квадрат ручки (квадратное отверстие 8-10мм)
- Крепёжные отверстия (круглые, 6-12мм)

### Этап 4: Вычисление размеров
```
backset = distance(cylinder_center, handle_center) * scale
center_distance = distance(cylinder_center, square_center) * scale
dimensions = bounding_box * scale
```

### Этап 5: Формирование результата
```json
{
  "backset": 55.0,
  "center_distance": 72.0,
  "plate_width": 24.0,
  "plate_height": 235.0,
  "confidence": 0.85
}
```

## 3. CV Модели
- YOLOv8-seg: сегментация замка
- OpenCV: контурный анализ
- SAM (Segment Anything): произвольная сегментация
