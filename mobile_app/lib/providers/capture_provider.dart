import 'dart:io';
import 'dart:typed_data';
import 'dart:ui';
import 'package:camera/camera.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/models/capture_context.dart';
import 'camera_provider.dart';
import 'mask_provider.dart';

final captureProvider = StateNotifierProvider<CaptureNotifier, CaptureState>((ref) {
  return CaptureNotifier(ref);
});

class CaptureState extends Equatable {
  final bool isCapturing;
  final CaptureContext? lastCapture;
  final String? error;

  const CaptureState({
    this.isCapturing = false,
    this.lastCapture,
    this.error,
  });

  @override
  List<Object?> get props => [isCapturing, lastCapture, error];

  CaptureState copyWith({
    bool? isCapturing,
    CaptureContext? lastCapture,
    String? error,
  }) {
    return CaptureState(
      isCapturing: isCapturing ?? this.isCapturing,
      lastCapture: lastCapture ?? this.lastCapture,
      error: error,
    );
  }
}

class CaptureNotifier extends StateNotifier<CaptureState> {
  final Ref _ref;

  CaptureNotifier(this._ref) : super(const CaptureState());

  Future<CaptureContext?> captureImage(BuildContext context) async {
    final cameraState = _ref.read(cameraControllerProvider);
    final maskState = _ref.read(maskProvider);

    if (!cameraState.hasValue || cameraState.value == null) {
      state = state.copyWith(error: 'Camera not initialized');
      return null;
    }

    if (!maskState.isAligned) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Пожалуйста, совместите маску с отверстием цилиндра')),
      );
      return null;
    }

    state = state.copyWith(isCapturing: true, error: null);

    try {
      final controller = cameraState.value!;
      final file = await controller.takePicture();
      final bytes = await File(file.path).readAsBytes();
      final imageSize = Size(
        controller.value.previewSize!.height.toDouble(),
        controller.value.previewSize!.width.toDouble(),
      );
      final scaleFactor = (150.0 * maskState.scale) / 10.0;
      final screenCenter = Offset(
        maskState.position.dx * MediaQuery.of(context).size.width,
        maskState.position.dy * MediaQuery.of(context).size.height,
      );

      final captureContext = CaptureContext(
        imageBytes: bytes,
        imageResolution: imageSize,
        scaleFactor: scaleFactor,
        markerCenter: screenCenter,
        timestamp: DateTime.now(),
      );

      state = state.copyWith(isCapturing: false, lastCapture: captureContext);
      return captureContext;
    } catch (e) {
      state = state.copyWith(isCapturing: false, error: e.toString());
      return null;
    }
  }

  void reset() {
    state = const CaptureState();
  }
}
