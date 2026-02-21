import 'dart:typed_data';
import 'dart:ui';

class CaptureContext {
  final Uint8List imageBytes;
  final Size imageResolution;
  final double scaleFactor;
  final Offset? markerCenter;
  final DateTime timestamp;

  CaptureContext({
    required this.imageBytes,
    required this.imageResolution,
    required this.scaleFactor,
    this.markerCenter,
    required this.timestamp,
  });

  double pixelsToMm(double pixels) => pixels / scaleFactor;
  double mmToPixels(double mm) => mm * scaleFactor;
}
