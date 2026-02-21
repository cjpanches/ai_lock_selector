import 'package:flutter/material.dart';
import '../../domain/models/capture_context.dart';
import '../../domain/models/lock_profile.dart';

class MeasurementResultScreen extends StatefulWidget {
  final CaptureContext captureContext;

  const MeasurementResultScreen({super.key, required this.captureContext});

  @override
  State<MeasurementResultScreen> createState() => _MeasurementResultScreenState();
}

class _MeasurementResultScreenState extends State<MeasurementResultScreen> {
  LockProfile? _profile;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _simulateMeasurement();
  }

  Future<void> _simulateMeasurement() async {
    await Future.delayed(const Duration(seconds: 1));
    final dims = widget.captureContext;
    final scale = dims.scaleFactor;
    setState(() {
      _profile = LockProfile(
        dimensions: LockDimensions(
          backset: 55.0 + (scale * 0.1).clamp(0, 5),
          centerDistance: 72.0 + (scale * 0.1).clamp(0, 5),
          plateWidth: 24.0 + (scale * 0.05).clamp(0, 2),
          plateHeight: 235.0 + (scale * 0.1).clamp(0, 10),
          plateThickness: 3.0,
          bodyWidth: 85.0,
          bodyHeight: 165.0,
          bodyDepth: 13.0,
        ),
        mountingHoles: const [
          MountingHole(x: 12, y: 45, diameter: 8),
          MountingHole(x: 12, y: 190, diameter: 8),
        ],
        handleSquare: HandleSquarePosition(x: 55, y: 100, size: 8),
        cylinderHole: CylinderHolePosition(x: 0, y: 85, width: 10, height: 17),
        confidence: 0.85,
        capturedAt: dims.timestamp,
      );
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Результат измерения')),
      body: _isLoading ? const Center(child: CircularProgressIndicator()) : _buildResult(context),
    );
  }

  Widget _buildResult(BuildContext context) {
    final profile = _profile!;
    final dims = profile.dimensions;
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildConfidenceCard(context, profile),
          const SizedBox(height: 16),
          _buildDimensionsCard(context, dims),
          const SizedBox(height: 16),
          _buildHolesCard(context, profile),
          const SizedBox(height: 24),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.search),
              label: const Text('Подобрать аналог'),
              style: ElevatedButton.styleFrom(padding: const EdgeInsets.all(16)),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildConfidenceCard(BuildContext context, LockProfile profile) {
    final color = profile.confidence > 0.7 ? Colors.green : profile.confidence > 0.5 ? Colors.orange : Colors.red;
    return Card(
      color: color.withOpacity(0.1),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Icon(Icons.verified, color: color, size: 32),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Достоверность', style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 4),
                  LinearProgressIndicator(value: profile.confidence, backgroundColor: color.withOpacity(0.2), valueColor: AlwaysStoppedAnimation(color)),
                ],
              ),
            ),
            const SizedBox(width: 16),
            Text('${(profile.confidence * 100).toInt()}%', style: Theme.of(context).textTheme.headlineSmall?.copyWith(color: color, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }

  Widget _buildDimensionsCard(BuildContext context, LockDimensions dims) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Размеры', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
            const Divider(),
            _buildDimensionRow(context, 'Backset (мм)', dims.backset),
            _buildDimensionRow(context, 'Межосевое (мм)', dims.centerDistance),
            _buildDimensionRow(context, 'Планка ширина (мм)', dims.plateWidth),
            _buildDimensionRow(context, 'Планка высота (мм)', dims.plateHeight),
            _buildDimensionRow(context, 'Корпус ширина (мм)', dims.bodyWidth),
            _buildDimensionRow(context, 'Корпус высота (мм)', dims.bodyHeight),
          ],
        ),
      ),
    );
  }

  Widget _buildDimensionRow(BuildContext context, String label, double value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label),
          Text(value.toStringAsFixed(1), style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold, color: Theme.of(context).colorScheme.primary)),
        ],
      ),
    );
  }

  Widget _buildHolesCard(BuildContext context, LockProfile profile) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Отверстия', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold)),
            const Divider(),
            if (profile.handleSquare != null) _buildDimensionRow(context, 'Квадрат ручки (мм)', profile.handleSquare!.size),
            Text('Крепёжные отверстия: ${profile.mountingHoles.length}', style: Theme.of(context).textTheme.bodyMedium),
          ],
        ),
      ),
    );
  }
}
