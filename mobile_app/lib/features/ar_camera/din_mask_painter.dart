import 'package:flutter/material.dart';

class DINMaskPainter extends CustomPainter {
  static const double maskWidthPx = 60.0;
  static const double maskHeightPx = 120.0;

  final Offset position;
  final double scale;
  final bool isAligned;

  DINMaskPainter({
    required this.position,
    required this.scale,
    required this.isAligned,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(
      position.dx * size.width,
      position.dy * size.height,
    );

    final maskWidth = maskWidthPx * scale;
    final maskHeight = maskHeightPx * scale;

    final strokeColor = isAligned ? Colors.green : Colors.red;
    final fillColor = isAligned ? Colors.green.withOpacity(0.15) : Colors.red.withOpacity(0.15);

    final strokePaint = Paint()
      ..color = strokeColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    final fillPaint = Paint()
      ..color = fillColor
      ..style = PaintingStyle.fill;

    canvas.save();
    canvas.translate(center.dx, center.dy);

    final rect = Rect.fromCenter(
      center: Offset.zero,
      width: maskWidth,
      height: maskHeight,
    );

    final path = _buildEuroProfilePath(rect);

    canvas.drawPath(path, fillPaint);
    canvas.drawPath(path, strokePaint);

    canvas.restore();
  }

  Path _buildEuroProfilePath(Rect rect) {
    final path = Path();
    
    final w = rect.width;
    final h = rect.height;
    
    // Scale factors: 33mm height = h pixels
    // 17mm width = w pixels (top semicircle diameter)
    final mmToPxY = h / 33.0;
    final mmToPxX = w / 17.0;
    
    // Key coordinates from euro_profile_exact.svg (in mm):
    // Top point: (16.5, 0)
    // Right intersection: (21.5, 15.37386354243376)
    // Right slot bottom: (21.5, 23)
    // Left slot bottom: (11.5, 23)
    // Left intersection: (11.5, 15.37386354243376)
    
    // Convert to pixel coordinates (centered)
    final halfW = w / 2;
    final halfH = h / 2;
    
    // Top point (center X = 0 in our coordinate system)
    final topY = -halfH;
    
    // Right intersection point
    final rightX = (21.5 - 16.5) * mmToPxX;  // 5mm to the right of center
    final rightIntY = -halfH + 15.37386 * mmToPxY;
    
    // Right slot bottom
    final rightSlotY = -halfH + 23.0 * mmToPxY;
    
    // Left intersection
    final leftX = (11.5 - 16.5) * mmToPxX;   // 5mm to the left of center
    final leftIntY = -halfH + 15.37386 * mmToPxY;
    
    // Bottom center
    final bottomY = halfH;
    
    // Radii in pixels
    final topRadius = 8.5 * mmToPxY;  // 8.5mm
    final bottomRadius = 5.0 * mmToPxY; // 5mm
    
    // Start at top center
    path.moveTo(0, topY);
    
    // Top semicircle (clockwise) from top to right intersection
    path.arcToPoint(
      Offset(rightX, rightIntY),
      radius: Radius.circular(topRadius),
      clockwise: true,
      largeArc: false,
    );
    
    // Line down to slot bottom (right side)
    path.lineTo(rightX, rightSlotY);
    
    // Bottom semicircle (clockwise) from right to left
    path.arcToPoint(
      Offset(leftX, rightSlotY),
      radius: Radius.circular(bottomRadius),
      clockwise: true,
      largeArc: false,
    );
    
    // Line up to left intersection
    path.lineTo(leftX, leftIntY);
    
    // Left semicircle (clockwise) back to top
    path.arcToPoint(
      Offset(0, topY),
      radius: Radius.circular(topRadius),
      clockwise: true,
      largeArc: false,
    );
    
    path.close();
    return path;
  }

  @override
  bool shouldRepaint(covariant DINMaskPainter oldDelegate) =>
      position != oldDelegate.position ||
      scale != oldDelegate.scale ||
      isAligned != oldDelegate.isAligned;
}
