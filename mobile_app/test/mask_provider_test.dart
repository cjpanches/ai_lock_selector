import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter/widgets.dart';
import 'package:ai_lock_selector/providers/mask_provider.dart';

void main() {
  group('MaskProvider', () {
    test('initial state is correct', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      final state = container.read(maskProvider);

      expect(state.position.dx, 0.5);
      expect(state.position.dy, 0.3);
      expect(state.scale, 1.0);
      expect(state.isAligned, false);
      expect(state.alignmentScore, 0.0);
    });

    test('updatePosition clamps values', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      container.read(maskProvider.notifier).updatePosition(
        const Offset(500, 500),
        const Size(100, 100),
      );

      final state = container.read(maskProvider);
      expect(state.position.dx, 1.0);
      expect(state.position.dy, 1.0);
    });

    test('updateScale clamps scale', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      container.read(maskProvider.notifier).updateScale(5.0);

      final state = container.read(maskProvider);
      expect(state.scale, 2.0);
    });

    test('reset returns to initial state', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      container.read(maskProvider.notifier).updateScale(0.1);
      container.read(maskProvider.notifier).reset();

      final state = container.read(maskProvider);
      expect(state.scale, 1.0);
      expect(state.position, const Offset(0.5, 0.3));
    });

    test('alignment check works correctly', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      container.read(maskProvider.notifier).updateScale(1.1);

      final state = container.read(maskProvider);
      expect(state.isAligned, true);
      expect(state.alignmentScore, greaterThan(0.8));
    });

    test('setAutoDetecting updates state', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      container.read(maskProvider.notifier).setAutoDetecting(true);

      final state = container.read(maskProvider);
      expect(state.isAutoDetecting, true);
    });

    test('applyAutoDetection sets position correctly', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      container.read(maskProvider.notifier).applyAutoDetection(
        boundingBox: const Rect.fromLTWH(100, 100, 200, 150),
        imageSize: const Size(1920, 1080),
        screenSize: const Size(1080, 1920),
      );

      final state = container.read(maskProvider);
      expect(state.position.dx, closeTo(0.2, 0.01));
      expect(state.position.dy, closeTo(0.15, 0.01));
      expect(state.isAutoDetecting, false);
    });

    test('applyAutoDetection calculates scale', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      container.read(maskProvider.notifier).applyAutoDetection(
        boundingBox: const Rect.fromLTWH(100, 100, 200, 150),
        imageSize: const Size(1920, 1080),
        screenSize: const Size(1080, 1920),
      );

      final state = container.read(maskProvider);
      expect(state.scale, greaterThan(0.5));
      expect(state.scale, lessThanOrEqualTo(2.0));
    });
  });
}
