import 'package:camera/camera.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

final availableCamerasProvider = FutureProvider<List<CameraDescription>>((ref) async {
  return await availableCameras();
});

final cameraControllerProvider = StateNotifierProvider<CameraControllerNotifier, AsyncValue<CameraController?>>((ref) {
  return CameraControllerNotifier(ref);
});

class CameraControllerNotifier extends StateNotifier<AsyncValue<CameraController?>> {
  final Ref _ref;
  CameraController? _controller;

  CameraControllerNotifier(this._ref) : super(const AsyncValue.loading()) {
    _initCamera();
  }

  Future<void> _initCamera() async {
    try {
      final cameras = await _ref.read(availableCamerasProvider.future);
      if (cameras.isEmpty) {
        state = AsyncValue.error('No cameras available', StackTrace.current);
        return;
      }
      _controller = CameraController(cameras.first, ResolutionPreset.high, enableAudio: false);
      await _controller!.initialize();
      state = AsyncValue.data(_controller);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> takePicture() async {
    if (_controller == null || !_controller!.value.isInitialized) return;
    await _controller!.takePicture();
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }
}
