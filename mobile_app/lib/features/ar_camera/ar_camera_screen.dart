import 'dart:convert';
import 'dart:io';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/models/capture_context.dart';
import '../../providers/providers.dart';
import 'din_mask_painter.dart';

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

  Future<void> _captureFrame({bool forceCapture = false}) async {
    final captureContext = await ref.read(captureProvider.notifier).captureImage(context, forceCapture: forceCapture);
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
              child: CustomPaint(
                painter: DINMaskPainter(
                  position: maskState.position,
                  scale: maskState.scale,
                  isAligned: maskState.isAligned,
                ),
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
    
    return AnimatedContainer(
      duration: const Duration(milliseconds: 300),
      padding: const EdgeInsets.all(16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          IconButton(
            onPressed: widget.onCancel,
            icon: const Icon(Icons.close, color: Colors.white, size: 28),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            decoration: BoxDecoration(
              color: Colors.black54,
              borderRadius: BorderRadius.circular(20),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  Icons.vpn_key,
                  color: Colors.white,
                  size: 18,
                ),
                const SizedBox(width: 8),
                Text(
                  'DIN 17×33мм',
                  style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                ),
              ],
            ),
          ),
          const SizedBox(width: 48),
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
      final result = await cvService.detectLock(imageBase64: base64Encode(bytes));
      
      if (result['success'] == true && result['detections'] != null) {
        final detections = result['detections'] as List;
        if (detections.isNotEmpty) {
          final best = detections.first;
          final bbox = best['bbox'] as List?;
          final confidence = (best['confidence'] as num?)?.toDouble();
          if (bbox != null && bbox.length == 4) {
            final screenSize = MediaQuery.of(context).size;
            final imageSize = Size(
              controller.value.previewSize!.width,
              controller.value.previewSize!.height,
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
              confidence: confidence,
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
                  : 'Перетащите маску или удерживайте для принудительного снимка',
              key: ValueKey(isAligned),
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.white70, fontSize: 14),
            ),
          ),
          const SizedBox(height: 24),
          GestureDetector(
            onTap: isCapturing ? null : () => _captureFrame(forceCapture: false),
            onLongPress: isCapturing ? null : () => _captureFrame(forceCapture: true),
            child: AnimatedBuilder(
              animation: _animationController,
              builder: (context, child) {
                return Transform.scale(
                  scale: isCapturing ? 0.9 : 1.0,
                  child: Container(
                    width: 80,
                    height: 80,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(
                        color: Colors.white,
                        width: 4,
                      ),
                      color: Colors.transparent,
                    ),
                    child: isCapturing
                        ? const CircularProgressIndicator(color: Colors.white)
                        : Icon(
                            Icons.camera_alt,
                            color: Colors.white,
                            size: 36,
                          ),
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 16),
        ],
      ),
    );
  }
}
}

