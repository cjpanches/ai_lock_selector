import 'package:flutter/material.dart';

class DINMaskPainter extends CustomPainter {
  final Offset position;
  final double scale;
  final double alignmentScore;
  final bool isAligned;
  final double pulseValue;
  final double glowValue;

  DINMaskPainter({
    required this.position,
    required this.scale,
    required this.alignmentScore,
    required this.isAligned,
    this.pulseValue = 1.0,
    this.glowValue = 0.5,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(position.dx * size.width, position.dy * size.height);
    const baseMaskWidth = 150.0;
    const baseMaskHeight = 100.0;
    final maskWidth = baseMaskWidth * pulseValue;
    final maskHeight = baseMaskHeight * pulseValue;

    final fillColor = isAligned ? Colors.green : Colors.red;
    final strokeColor = isAligned ? Colors.green : Colors.red;

    final fillPaint = Paint()
      ..color = fillColor.withOpacity(glowValue * 0.5)
      ..style = PaintingStyle.fill;

    final strokePaint = Paint()
      ..color = strokeColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3;

    final glowPaint = Paint()
      ..color = fillColor.withOpacity(glowValue * 0.3)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 8
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 8);

    canvas.save();
    canvas.translate(center.dx, center.dy);
    canvas.scale(scale);
    canvas.scale(pulseValue);

    final rect = Rect.fromCenter(center: Offset.zero, width: maskWidth, height: maskHeight);
    final dinPath = _buildDINPath(rect);

    canvas.drawPath(dinPath, glowPaint);
    canvas.drawPath(dinPath, fillPaint);
    canvas.drawPath(dinPath, strokePaint);

    _drawDINLabel(canvas, rect);

    canvas.restore();
  }

  void _drawDINLabel(Canvas canvas, Rect rect) {
    final textPainter = TextPainter(
      text: const TextSpan(
        text: 'DIN',
        style: TextStyle(
          color: Colors.white,
          fontSize: 12,
          fontWeight: FontWeight.bold,
        ),
      ),
      textDirection: TextDirection.ltr,
    );
    textPainter.layout();
    textPainter.paint(canvas, Offset(-textPainter.width / 2, rect.bottom + 5));
  }

  Path _buildDINPath(Rect rect) {
    final path = Path();
    final waistWidth = rect.width * 0.3;
    final waistHeight = rect.height * 0.4;
    path.moveTo(rect.left, rect.top);
    path.lineTo(rect.left + (rect.width - waistWidth) / 2, rect.top);
    path.lineTo(rect.left + (rect.width - waistWidth) / 2, rect.top + (rect.height - waistHeight) / 2);
    path.lineTo(rect.left, rect.bottom);
    path.lineTo(rect.right, rect.bottom);
    path.lineTo(rect.right - (rect.width - waistWidth) / 2, rect.top + (rect.height + waistHeight) / 2);
    path.lineTo(rect.right - (rect.width - waistWidth) / 2, rect.top);
    path.lineTo(rect.right, rect.top);
    path.close();
    return path;
  }

  @override
  bool shouldRepaint(covariant DINMaskPainter oldDelegate) =>
      position != oldDelegate.position ||
      scale != oldDelegate.scale ||
      isAligned != oldDelegate.isAligned ||
      pulseValue != oldDelegate.pulseValue ||
      glowValue != oldDelegate.glowValue;
}
