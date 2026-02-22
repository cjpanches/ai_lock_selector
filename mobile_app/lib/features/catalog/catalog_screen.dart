import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/models/lock.dart';
import '../../providers/locks_provider.dart';

class CatalogScreen extends ConsumerStatefulWidget {
  const CatalogScreen({super.key});

  @override
  ConsumerState<CatalogScreen> createState() => _CatalogScreenState();
}

class _CatalogScreenState extends ConsumerState<CatalogScreen> {
  String? _selectedType;

  @override
  Widget build(BuildContext context) {
    final filter = LocksFilter(type: _selectedType);
    final locksAsync = ref.watch(locksProvider(filter));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Каталог замков'),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.filter_list),
            onPressed: _showFilterDialog,
          ),
        ],
      ),
      body: Column(
        children: [
          if (_selectedType != null)
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Chip(
                label: Text('Фильтр: ${LockType.getDisplayName(_selectedType!)}'),
                deleteIcon: const Icon(Icons.close, size: 18),
                onDeleted: () => setState(() => _selectedType = null),
              ),
            ),
          Expanded(
            child: locksAsync.when(
              data: (response) => _buildLocksList(response.locks),
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (error, stack) => _buildError(error),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLocksList(List<Lock> locks) {
    if (locks.isEmpty) {
      return const Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.inventory_2_outlined, size: 64, color: Colors.grey),
            SizedBox(height: 16),
            Text('Замки не найдены', style: TextStyle(fontSize: 18, color: Colors.grey)),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: locks.length,
      itemBuilder: (context, index) => _LockCard(lock: locks[index]),
    );
  }

  Widget _buildError(Object error) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.error_outline, size: 64, color: Colors.red),
            const SizedBox(height: 16),
            Text(
              'Ошибка загрузки',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 8),
            Text(
              error.toString(),
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: Colors.grey),
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () => ref.invalidate(locksProvider(LocksFilter(type: _selectedType))),
              icon: const Icon(Icons.refresh),
              label: const Text('Повторить'),
            ),
          ],
        ),
      ),
    );
  }

  void _showFilterDialog() {
    showModalBottomSheet(
      context: context,
      builder: (context) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              title: const Text('Все типы'),
              leading: const Icon(Icons.clear_all),
              selected: _selectedType == null,
              onTap: () {
                setState(() => _selectedType = null);
                Navigator.pop(context);
              },
            ),
            const Divider(),
            ...LockType.values.map((type) => ListTile(
              title: Text(LockType.getDisplayName(type)),
              leading: Icon(_getLockIcon(type)),
              selected: _selectedType == type,
              onTap: () {
                setState(() => _selectedType = type);
                Navigator.pop(context);
              },
            )),
          ],
        ),
      ),
    );
  }

  IconData _getLockIcon(String type) {
    switch (type) {
      case 'embedded':
        return Icons.lock;
      case 'overlay':
        return Icons.lock_open;
      case 'latch':
        return Icons.door_front_door;
      case 'deadbolt':
        return Icons.lock;
      case 'electronic':
        return Icons.smart_toy;
      case 'cylinder':
        return Icons.vpn_key;
      default:
        return Icons.lock;
    }
  }
}

class LockType {
  static const String embedded = 'embedded';
  static const String overlay = 'overlay';
  static const String latch = 'latch';
  static const String deadbolt = 'deadbolt';
  static const String electronic = 'electronic';
  static const String cylinder = 'cylinder';

  static const List<String> values = [
    embedded,
    overlay,
    latch,
    deadbolt,
    electronic,
    cylinder,
  ];

  static String getDisplayName(String type) {
    switch (type) {
      case embedded:
        return 'Врезной';
      case overlay:
        return 'Накладной';
      case latch:
        return 'Защёлка';
      case deadbolt:
        return 'Врезной с задвижкой';
      case electronic:
        return 'Электронный';
      case cylinder:
        return 'Цилиндровый';
      default:
        return type;
    }
  }
}

class _LockCard extends StatelessWidget {
  final Lock lock;

  const _LockCard({required this.lock});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ExpansionTile(
        leading: CircleAvatar(
          backgroundColor: Theme.of(context).colorScheme.primaryContainer,
          child: Icon(
            _getLockIcon(lock.type),
            color: Theme.of(context).colorScheme.primary,
          ),
        ),
        title: Text(lock.name, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text('${lock.vendorCode} • ${lock.brand ?? "Нет бренда"}'),
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildInfoRow('Тип', lock.typeDisplayName),
                _buildInfoRow('Backset', '${lock.backset} мм'),
                _buildInfoRow('Межосевое расстояние', '${lock.centerDistance} мм'),
                _buildInfoRow('Ширина планки', '${lock.plateWidth} мм'),
                _buildInfoRow('Высота планки', '${lock.plateHeight} мм'),
                _buildInfoRow('Толщина планки', '${lock.plateThickness} мм'),
                _buildInfoRow('Ширина корпуса', '${lock.bodyWidth} мм'),
                _buildInfoRow('Высота корпуса', '${lock.bodyHeight} мм'),
                _buildInfoRow('Глубина корпуса', '${lock.bodyDepth} мм'),
                if (lock.cylinderHoleDiameter != null)
                  _buildInfoRow('Диаметр цилиндра', '${lock.cylinderHoleDiameter} мм'),
                if (lock.squareHoleSize != null)
                  _buildInfoRow('Квадрат ручки', '${lock.squareHoleSize} мм'),
                if (lock.description != null) ...[
                  const SizedBox(height: 8),
                  Text(lock.description!, style: Theme.of(context).textTheme.bodySmall),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label, style: const TextStyle(color: Colors.grey)),
          Text(value, style: const TextStyle(fontWeight: FontWeight.w500)),
        ],
      ),
    );
  }

  IconData _getLockIcon(String type) {
    switch (type) {
      case 'embedded':
        return Icons.lock;
      case 'overlay':
        return Icons.lock_open;
      case 'latch':
        return Icons.door_front_door;
      case 'deadbolt':
        return Icons.lock;
      case 'electronic':
        return Icons.smart_toy;
      case 'cylinder':
        return Icons.vpn_key;
      default:
        return Icons.lock;
    }
  }
}
