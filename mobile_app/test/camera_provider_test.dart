import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:ai_lock_selector/providers/camera_provider.dart';

void main() {
  group('CameraProvider', () {
    test('initial state is loading', () {
      final container = ProviderContainer();
      addTearDown(container.dispose);

      final state = container.read(cameraControllerProvider);

      expect(state.isLoading, true);
    });
  });
}
