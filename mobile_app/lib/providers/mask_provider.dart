import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class MaskState {
  final Offset position;
  final double scale;
  final bool isAligned;
  final double alignmentScore;

  const MaskState({
    this.position = const Offset(0.5, 0.3),
    this.scale = 1.0,
    this.isAligned = false,
    this.alignmentScore = 0.0,
  });

  MaskState copyWith({
    Offset? position,
    double? scale,
    bool? isAligned,
    double? alignmentScore,
  }) {
    return MaskState(
      position: position ?? this.position,
      scale: scale ?? this.scale,
      isAligned: isAligned ?? this.isAligned,
      alignmentScore: alignmentScore ?? this.alignmentScore,
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
