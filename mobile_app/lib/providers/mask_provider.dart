import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class MaskState {
  final Offset position;
  final double scale;
  final bool isAligned;
  final double alignmentScore;
  final bool isAutoDetecting;
  final Rect? detectedBounds;

  const MaskState({
    this.position = const Offset(0.5, 0.3),
    this.scale = 1.0,
    this.isAligned = false,
    this.alignmentScore = 0.0,
    this.isAutoDetecting = false,
    this.detectedBounds,
  });

  MaskState copyWith({
    Offset? position,
    double? scale,
    bool? isAligned,
    double? alignmentScore,
    bool? isAutoDetecting,
    Rect? detectedBounds,
  }) {
    return MaskState(
      position: position ?? this.position,
      scale: scale ?? this.scale,
      isAligned: isAligned ?? this.isAligned,
      alignmentScore: alignmentScore ?? this.alignmentScore,
      isAutoDetecting: isAutoDetecting ?? this.isAutoDetecting,
      detectedBounds: detectedBounds ?? this.detectedBounds,
    );
  }
}

final maskProvider = StateNotifierProvider<MaskNotifier, MaskState>((ref) {
  return MaskNotifier();
});

class MaskNotifier extends StateNotifier<MaskState> {
  MaskNotifier() : super(const MaskState());

  void updatePosition(Offset newPosition, Size screenSize) {
    state = state.copyWith(
      position: Offset(
        (newPosition.dx / screenSize.width).clamp(0.0, 1.0),
        (newPosition.dy / screenSize.height).clamp(0.0, 1.0),
      ),
    );
    _checkAlignment();
  }

  void updateScale(double scale) {
    state = state.copyWith(scale: (state.scale * scale).clamp(0.5, 2.0));
    _checkAlignment();
  }

  void setAutoDetecting(bool detecting) {
    state = state.copyWith(isAutoDetecting: detecting);
  }

  void applyAutoDetection({
    required Rect boundingBox,
    required Size imageSize,
    required Size screenSize,
    double? confidence,
  }) {
    final imageCenterX = boundingBox.left + boundingBox.width / 2;
    final imageCenterY = boundingBox.top + boundingBox.height / 2;
    
    final normalizedX = imageCenterX / imageSize.width;
    final normalizedY = imageCenterY / imageSize.height;
    
    final aspectRatio = screenSize.width / screenSize.height;
    final imageAspectRatio = imageSize.width / imageSize.height;
    
    double scale = 1.0;
    if (imageAspectRatio > aspectRatio) {
      scale = screenSize.width / imageSize.width;
    } else {
      scale = screenSize.height / imageSize.height;
    }
    
    final detectedWidthPx = boundingBox.width * scale;
    final targetWidthPx = 150.0;
    scale = targetWidthPx / detectedWidthPx;
    
    final cvConfidence = confidence ?? 0.5;
    final alignmentScore = cvConfidence.clamp(0.0, 1.0);
    
    state = state.copyWith(
      position: Offset(normalizedX.clamp(0.0, 1.0), normalizedY.clamp(0.0, 1.0)),
      scale: scale.clamp(0.5, 2.0),
      detectedBounds: boundingBox,
      isAutoDetecting: false,
      alignmentScore: alignmentScore,
      isAligned: alignmentScore > 0.8,
    );
  }

  void _checkAlignment() {
    final scaleDiff = (state.scale - 1.0).abs();
    final alignmentScore = scaleDiff < 0.2 ? 1.0 - scaleDiff : 0.0;
    state = state.copyWith(
      alignmentScore: alignmentScore,
      isAligned: alignmentScore > 0.8,
    );
  }

  void reset() {
    state = const MaskState();
  }
}
