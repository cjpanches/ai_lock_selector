import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:ai_lock_selector/providers/capture_provider.dart';

void main() {
  group('CaptureProvider', () {
    test('initial state is correct', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      final state = container.read(captureProvider);

      expect(state.isCapturing, false);
      expect(state.lastCapture, null);
      expect(state.error, null);
    });

    test('reset clears state', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      container.read(captureProvider.notifier).reset();

      final state = container.read(captureProvider);
      expect(state.isCapturing, false);
      expect(state.lastCapture, null);
    });
  });

  group('CaptureState', () {
    test('copyWith works correctly', () {
      const state = CaptureState(isCapturing: false);
      final newState = state.copyWith(isCapturing: true, error: 'test error');

      expect(newState.isCapturing, true);
      expect(newState.error, 'test error');
    });

    test('copyWith preserves other fields', () {
      const state = CaptureState(isCapturing: true);
      final newState = state.copyWith(error: 'error');

      expect(newState.isCapturing, true);
      expect(newState.error, 'error');
    });
  });
}
