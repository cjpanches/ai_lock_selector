# AR UI Guidelines

## Overview

Руководство по реализации AR (Augmented Reality) интерфейса в Flutter приложении для отображения эталонного контура euro cylinder.

## AR Overlay Purpose

1. **Visual Guidance**: Показать пользователю эталонную форму euro cylinder
2. **Positioning Help**: Помощь в правильном позиционировании камеры
3. **Calibration Reference**: Reference point for measurements
4. **User Experience**: Modern, professional feel

## Design Specifications

### Euro Cylinder Overlay

**Source**: `mask/euro_profile_exact.svg`

**Dimensions** (real-world):
- Total Height: 33mm
- Top Circle: 17mm diameter
- Slot Width: 10mm
- Bottom: 10mm diameter

**Visual Style**:
- Color: Semi-transparent white/cyan
- Stroke: 2-3px, dashed
- Fill: 10-20% opacity
- Corner markers: Small circles at key points

### Screen Layout

```
┌────────────────────────────────────┐
│  ┌──────────────────────────────┐  │
│  │                              │  │
│  │      Camera Preview          │  │
│  │                              │  │
│  │    ┌─────────────┐          │  │
│  │    │  Euro      │           │  │
│  │    │  Cylinder  │           │  │
│  │    │  Overlay   │           │  │
│  │    └─────────────┘          │  │
│  │                              │  │
│  └──────────────────────────────┘  │
│                                    │
│  ┌────┐              ┌─────────┐  │
│  │ ⚡ │              │  📷     │  │
│  └────┘              └─────────┘  │
│                                    │
│  Instructions: "Align the cylinder" │
└────────────────────────────────────┘
```

## Implementation

### Flutter Packages

```yaml
dependencies:
  camera: ^0.11.0
  flutter_svg: ^2.0.10
  vector_math: ^2.1.4
```

### Loading SVG

```dart
import 'package:flutter_svg/flutter_svg.dart';

Widget buildAROverlay() {
  return SvgPicture.asset(
    'assets/euro_profile_exact.svg',
    colorFilter: ColorFilter.mode(
      Colors.white.withOpacity(0.5),
      BlendMode.srcATop,
    ),
  );
}
```

### Camera Integration

```dart
import 'package:camera/camera.dart';

class CameraScreen extends StatefulWidget {
  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  CameraController? _controller;
  
  @override
  void initState() {
    super.initState();
    _initCamera();
  }
  
  Future<void> _initCamera() async {
    final cameras = await availableCameras();
    _controller = CameraController(
      cameras.first,
      ResolutionPreset.high,
    );
    await _controller!.initialize();
  }
  
  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // Camera preview
        CameraPreview(_controller!),
        
        // AR Overlay
        Positioned.fill(
          child: CustomPaint(
            painter: EuroCylinderPainter(),
          ),
        ),
      ],
    );
  }
}
```

### Custom Painter

```dart
class EuroCylinderPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.cyan.withOpacity(0.5)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;
    
    // Draw euro cylinder outline
    // Scale based on detected object size
    
    final rect = Rect.fromCenter(
      center: Offset(size.width / 2, size.height / 2),
      width: 100, // Scale from detection
      height: 330, // 33mm aspect ratio
    );
    
    canvas.drawOval(rect, paint);
  }
  
  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
```

## UI States

### 1. Initial State
- Overlay visible but dimmed (30% opacity)
- Text: "Position camera to see lock"

### 2. Scanning State
- Overlay pulses slowly
- Text: "Analyzing..."

### 3. Detected State
- Overlay bright (70% opacity)
- Green border if aligned
- Text: "Lock detected - measuring..."

### 4. Success State
- Overlay shows measurement points
- Draw lines from cylinder to handle
- Text: "Measurement complete"

### 5. Error State
- Overlay turns red
- Text: "Try again - ensure good lighting"

## Accessibility

- High contrast mode option
- Large touch targets (min 48x48)
- Screen reader support
- Haptic feedback on capture

## Animations

| Animation | Duration | Curve |
|-----------|----------|-------|
| Overlay appear | 300ms | easeInOut |
| Pulse effect | 1500ms | linear (repeat) |
| Success checkmark | 400ms | bounceOut |
| Error shake | 300ms | elasticOut |

## Responsive Design

- Overlay scales with screen size
- Maintains aspect ratio
- Minimum touch target: 48x48
- Safe areas respected (notch, home indicator)

## Related Documents

- [mask/euro_profile_exact.svg](./mask/euro_profile_exact.svg) - Source SVG
- [AGENTS.md](./AGENTS.md) - Flutter implementation
- [05_AR_MEASUREMENT_TECH.md](./05_AR_MEASUREMENT_TECH.md) - Technical specs
