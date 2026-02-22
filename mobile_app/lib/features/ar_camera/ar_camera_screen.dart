import 'dart:io';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/models/capture_context.dart';
import '../providers/providers.dart';

class ARCameraScreen extends ConsumerStatefulWidget {
  final Function(CaptureContext)? onCapture;
  final VoidCallback? onCancel;

  const ARCameraScreen({super.key, this.onCapture, this.onCancel});

  @override
  ConsumerState<ARCameraScreen> createState() => _ARCameraScreenState();
}

class _ARCameraScreenState extends ConsumerState<ARCameraScreen> with WidgetsBindingObserver, SingleTickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _pulseAnimation;
  late Animation<double> _glowAnimation;
  bool _showSuccessAnimation = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1500),
    )..repeat(reverse: true);

    _pulseAnimation = Tween<double>(begin: 1.0, end: 1.1).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.easeInOut),
    );

    _glowAnimation = Tween<double>(begin: 0.3, end: 0.6).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _animationController.dispose();
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.inactive) {
    } else if (state == AppLifecycleState.resumed) {
    }
  }

  void _onScaleUpdate(ScaleUpdateDetails details) {
    final maskNotifier = ref.read(maskProvider.notifier);
    final screenSize = MediaQuery.of(context).size;
    final currentPosition = ref.read(maskProvider).position;
    final newPosition = Offset(
      currentPosition.dx * screenSize.width + details.focalPointDelta.dx,
      currentPosition.dy * screenSize.height + details.focalPointDelta.dy,
    );
    maskNotifier.updatePosition(newPosition, screenSize);
    maskNotifier.updateScale(details.scale);
  }

  Future<void> _captureFrame() async {
    final captureContext = await ref.read(captureProvider.notifier).captureImage(context);
    if (captureContext != null) {
      setState(() => _showSuccessAnimation = true);
      await Future.delayed(const Duration(milliseconds: 500));
      if (mounted) {
        widget.onCapture?.call(captureContext);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final cameraState = ref.watch(cameraControllerProvider);
    final maskState = ref.watch(maskProvider);
    final captureState = ref.watch(captureProvider);

    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          cameraState.when(
            data: (controller) => controller != null
                ? CameraPreview(controller)
                : const Center(child: Text('No camera', style: TextStyle(color: Colors.white))),
            loading: () => const Center(child: CircularProgressIndicator(color: Colors.white)),
            error: (error, _) => Center(child: Text('Error: $error', style: const TextStyle(color: Colors.white))),
          ),
          Positioned.fill(
            child: GestureDetector(
              onScaleUpdate: _onScaleUpdate,
              behavior: HitTestBehavior.opaque,
              child: AnimatedBuilder(
                animation: _animationController,
                builder: (context, child) {
                  return CustomPaint(
                    painter: DINMaskPainter(
                      position: maskState.position,
                      scale: maskState.scale,
                      alignmentScore: maskState.alignmentScore,
                      isAligned: maskState.isAligned,
                      pulseValue: maskState.isAligned ? _pulseAnimation.value : 1.0,
                      glowValue: _glowAnimation.value,
                    ),
                  );
                },
              ),
            ),
          ),
          if (_showSuccessAnimation)
            Container(
              color: Colors.green.withOpacity(0.3),
              child: const Center(
                child: Icon(Icons.check_circle, color: Colors.white, size: 100),
              ),
            ),
          SafeArea(
            child: Column(
              children: [
                _buildTopBar(maskState.isAligned),
                const Spacer(),
                _buildBottomControls(maskState.isAligned, maskState.alignmentScore, captureState.isCapturing),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTopBar(bool isAligned) {
    final maskState = ref.watch(maskProvider);
    final isDetecting = maskState.isAutoDetecting;
    
    return AnimatedContainer(
      duration: const Duration(milliseconds: 300),
      padding: const EdgeInsets.all(16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          IconButton(
            onPressed: widget.onCancel,
            icon: AnimatedSwitcher(
              duration: const Duration(milliseconds: 200),
              child: Icon(Icons.close, color: Colors.white, size: 28, key: ValueKey(isAligned)),
            ),
          ),
          GestureDetector(
            onTap: isDetecting ? null : () => _runAutoDetect(),
            child: AnimatedContainer(
              duration: const Duration(milliseconds: 300),
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              decoration: BoxDecoration(
                color: isAligned ? Colors.green : Colors.orange,
                borderRadius: BorderRadius.circular(20),
                boxShadow: isAligned
                    ? [BoxShadow(color: Colors.green.withOpacity(0.5), blurRadius: 10, spreadRadius: 2)]
                    : null,
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  isDetecting
                      ? const SizedBox(
                          width: 18,
                          height: 18,
                          child: CircularProgressIndicator(
                            color: Colors.white,
                            strokeWidth: 2,
                          ),
                        )
                      : Icon(
                          isAligned ? Icons.check_circle : Icons.info_outline,
                          color: Colors.white,
                          size: 18,
                        ),
                  const SizedBox(width: 8),
                  Text(
                    isDetecting
                        ? 'Детекция...'
                        : (isAligned ? 'Маска совмещена' : 'Совместите маску'),
                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
            ),
          ),
          IconButton(
            onPressed: isDetecting ? null : () => _runAutoDetect(),
            icon: AnimatedSwitcher(
              duration: const Duration(milliseconds: 200),
              child: Icon(
                isDetecting ? Icons.hourglass_empty : Icons.auto_fix_high,
                color: Colors.white,
                size: 28,
                key: ValueKey(isDetecting),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Future<void> _runAutoDetect() async {
    final cameraState = ref.read(cameraControllerProvider);
    if (!cameraState.hasValue || cameraState.value == null) return;
    
    final maskNotifier = ref.read(maskProvider.notifier);
    maskNotifier.setAutoDetecting(true);
    
    try {
      final controller = cameraState.value!;
      final file = await controller.takePicture();
      final bytes = await File(file.path).readAsBytes();
      
      final cvService = ref.read(cvServiceProvider);
      final result = await cvService.detectLock(imageBase64: bytes.toString());
      
      if (result['success'] == true && result['detections'] != null) {
        final detections = result['detections'] as List;
        if (detections.isNotEmpty) {
          final best = detections.first;
          final bbox = best['bbox'] as List?;
          if (bbox != null && bbox.length == 4) {
            final screenSize = MediaQuery.of(context).size;
            final imageSize = Size(
              controller.value.previewSize!.height,
              controller.value.previewSize!.width,
            );
            
            maskNotifier.applyAutoDetection(
              boundingBox: Rect.fromLTWH(
                (bbox[0] as num).toDouble(),
                (bbox[1] as num).toDouble(),
                (bbox[2] as num).toDouble(),
                (bbox[3] as num).toDouble(),
              ),
              imageSize: imageSize,
              screenSize: screenSize,
            );
            return;
          }
        }
      }
      
      maskNotifier.setAutoDetecting(false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Автоопределение не удалось. Переместите маску вручную.')),
        );
      }
    } catch (e) {
      maskNotifier.setAutoDetecting(false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Ошибка: $e')),
        );
      }
    }
  }

  Widget _buildBottomControls(bool isAligned, double alignmentScore, bool isCapturing) {
    return Container(
      padding: const EdgeInsets.all(24),
      child: Column(
        children: [
          AnimatedSwitcher(
            duration: const Duration(milliseconds: 300),
            child: Text(
              isAligned
                  ? 'Нажмите для захвата'
                  : 'Перетащите маску на отверстие цилиндра',
              key: ValueKey(isAligned),
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.white70, fontSize: 14),
            ),
          ),
          const SizedBox(height: 24),
          GestureDetector(
            onTap: isAligned && !isCapturing ? _captureFrame : null,
            child: AnimatedBuilder(
              animation: _animationController,
              builder: (context, child) {
                return Transform.scale(
                  scale: isCapturing ? 0.9 : (isAligned ? _pulseAnimation.value : 1.0),
                  child: Container(
                    width: 80,
                    height: 80,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(
                        color: isAligned ? Colors.green : Colors.white,
                        width: 4,
                      ),
                      color: isAligned ? Colors.green.withOpacity(_glowAnimation.value) : Colors.transparent,
                      boxShadow: isAligned
                          ? [
                              BoxShadow(
                                color: Colors.green.withOpacity(0.5),
                                blurRadius: 20 * _glowAnimation.value,
                                spreadRadius: 5 * _glowAnimation.value,
                              ),
                            ]
                          : null,
                    ),
                    child: isCapturing
                        ? const CircularProgressIndicator(color: Colors.white)
                        : Icon(
                            isAligned ? Icons.check : Icons.camera_alt,
                            color: Colors.white,
                            size: 36,
                          ),
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 16),
          AnimatedSwitcher(
            duration: const Duration(milliseconds: 300),
            child: Row(
              key: ValueKey(alignmentScore),
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  alignmentScore > 0.8 ? Icons.check_circle : Icons.warning,
                  color: alignmentScore > 0.8 ? Colors.green : Colors.orange,
                  size: 18,
                ),
                const SizedBox(width: 8),
                Text(
                  'Точность: ${(alignmentScore * 100).toInt()}%',
                  style: TextStyle(
                    color: alignmentScore > 0.8 ? Colors.green : Colors.orange,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

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
