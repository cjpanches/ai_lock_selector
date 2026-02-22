## ГЕНЕРАЦИЯ КОДА GPT
### Дата: 2026-02-22

## АНАЛИЗ ЗАДАЧ

### Задачи которые можно решить генерацией кода:
1. **Pydantic config warning** - заменить class Config на model_config
2. **PostgreSQL миграция** - подготовить настройки для asyncpg
3. **LSP errors ignore** - добавить настройки для игнорирования ложных ошибок
4. **Flutter catalog stub** - добавить базовую реализацию каталога

### Задачи которые требуют ручной работы:
1. **Датасет для YOLO** - нужно собрать 500+ реальных фото замков
2. **Обучение YOLO** - требует размеченный датасет
3. **Интеграция камеры** - требует физическое устройство для тестирования
4. **Flutter тесты** - требует Flutter SDK

## СГЕНЕРИРОВАННЫЙ КОД

### Задача 1: Исправление Pydantic config warning
**Файл:** backend/app/core/config.py
**Описание:** Замена deprecated class Config на model_config

```python
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    
    app_name: str = "AI Lock Selector"
    debug: bool = True
    
    database_url: str = "sqlite+aiosqlite:///./locks.db"
    
    cors_origins: list = ["*"]


@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
```

### Задача 2: PostgreSQL настройки
**Файл:** backend/app/db/postgres.py
**Описание:** Подготовка для PostgreSQL миграции

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator


class Base(DeclarativeBase):
    pass


class PostgreSQLManager:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=True)
        self.async_session_maker = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session
    
    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def close(self):
        await self.engine.dispose()


def create_postgres_manager(database_url: str) -> PostgreSQLManager:
    return PostgreSQLManager(database_url)
```

### Задача 3: LSP ignore настройки
**Файл:** backend/pyproject.toml (создать)
**Описание:** Игнорирование ложных LSP ошибок

```toml
[tool.pyright]
reportMissingTypeStubs = false
reportUnknownMemberType = false
pythonVersion = "3.12"

[tool.pyright.analysis]
autoSearchPaths = true
useLibraryCodeForTypes = true
reportMissingImports = false

[tool.ruff]
select = ["E", "F", "W", "I"]
ignore = []

[tool.ruff.per-file-ignores]
"__init__.py" = ["F401"]
"cv_pipeline/*" = ["E501", "E722"]
```

### Задача 4: Flutter Catalog Screen stub
**Файл:** mobile_app/lib/features/catalog/catalog_screen.dart
**Описание:** Базовая реализация экрана каталога

```dart
import 'package:flutter/material.dart';
import 'package:dio/dio.dart';

class CatalogScreen extends StatefulWidget {
  const CatalogScreen({super.key});

  @override
  State<CatalogScreen> createState() => _CatalogScreenState();
}

class _CatalogScreenState extends State<CatalogScreen> {
  List<dynamic> _locks = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadLocks();
  }

  Future<void> _loadLocks() async {
    try {
      final dio = Dio(BaseOptions(baseUrl: 'http://localhost:8000'));
      final response = await dio.get('/api/v1/locks');
      setState(() {
        _locks = response.data['locks'] ?? [];
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Ошибка загрузки: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Каталог замков'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _locks.isEmpty
              ? const Center(child: Text('Нет данных'))
              : ListView.builder(
                  itemCount: _locks.length,
                  itemBuilder: (context, index) {
                    final lock = _locks[index];
                    return ListTile(
                      title: Text(lock['name'] ?? ''),
                      subtitle: Text(lock['brand'] ?? ''),
                      trailing: Text(lock['vendor_code'] ?? ''),
                    );
                  },
                ),
    );
  }
}
```

### Задача 5: YOLO training script
**Файл:** cv_pipeline/train_yolo.py
**Описание:** Скрипт для обучения YOLO (после сбора датасета)

```python
from ultralytics import YOLO
import yaml
import os


def create_dataset_config(dataset_path: str) -> dict:
    """Создание конфигурации датасета для YOLO"""
    return {
        'path': dataset_path,
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'names': {
            0: 'lock_plate',
            1: 'cylinder_hole',
            2: 'mounting_hole',
            3: 'handle_square'
        }
    }


def train_yolo(
    model_size: str = 'yolov8n.pt',
    data_yaml: str = 'dataset.yaml',
    epochs: int = 100,
    imgsz: int = 640,
    batch: int = 16,
    project: str = 'runs/detect',
    name: str = 'train'
) -> YOLO:
    """Обучение YOLO модели"""
    model = YOLO(model_size)
    
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        project=project,
        name=name,
        patience=10,
        save=True,
        plots=True,
        val=True,
    )
    
    return model


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, required=True)
    parser.add_argument('--epochs', type=int, default=100)
    args = parser.parse_args()
    
    train_yolo(data_yaml=args.data, epochs=args.epochs)
```

## РЕКОМЕНДАЦИИ ПО ЗОНЕ GPT

1. **Приоритетные задачи которые решаются кодом:**
   - Pydantic config - готово, нужно применить
   - PostgreSQL manager - код готов, требует подключения
   - Catalog screen - код готов, требует роута
   - YOLO training - код готов, требует датасет

2. **Задачи требующие ручной работы:**
   - Сбор датасета (500+ фото)
   - Разметка (CVAT или Roboflow)
   - Тестирование на устройстве
   - CI/CD настройка

3. **Следующие шаги:**
   - Применить исправление config.py
   - Запустить backend и проверить
   - Создать catalog screen и добавить в router
   - Собрать датасет для YOLO
