import 'dart:async';
import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import '../../domain/models/capture_context.dart';

class ARCameraScreen extends StatefulWidget {
  final Function(CaptureContext)? onCapture;
  final VoidCallback? onCancel;

  const ARCameraScreen({super.key, this.onCapture, this.onCancel});

  @override
  State<ARCameraScreen> createState() => _ARCameraScreenState();
}

class _ARCameraScreenState extends State<ARCameraScreen> with WidgetsBindingObserver {
  CameraController? _controller;
  List<CameraDescription>? _cameras;
  bool _isInitialized = false;
  bool _isCapturing = false;
  Offset _maskPosition = const Offset(0.5, 0.3);
  double _maskScale = 1.0;
  bool _isMaskAligned = false;
  double _alignmentScore = 0.0;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _initializeCamera();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    _controller?.dispose();
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (_controller == null || !_controller!.value.isInitialized) return;
    if (state == AppLifecycleState.inactive) {
      _controller?.dispose();
    } else if (state == AppLifecycleState.resumed) {
      _initializeCamera();
    }
  }

  Future<void> _initializeCamera() async {
    try {
      _cameras = await availableCameras();
      if (_cameras == null || _cameras!.isEmpty) return;
      _controller = CameraController(_cameras!.first, ResolutionPreset.high, enableAudio: false);
      await _controller!.initialize();
      if (mounted) setState(() => _isInitialized = true);
    } catch (e) {
      debugPrint('Camera init error: $e');
    }
  }

  void _onScaleUpdate(ScaleUpdateDetails details) {
    setState(() {
      _maskPosition = Offset(
        (_maskPosition.dx + details.focalPointDelta.dx / MediaQuery.of(context).size.width).clamp(0.0, 1.0),
        (_maskPosition.dy + details.focalPointDelta.dy / MediaQuery.of(context).size.height).clamp(0.0, 1.0),
      );
      _maskScale = (_maskScale * details.scale).clamp(0.5, 2.0);
    });
    _checkAlignment();
  }

  void _checkAlignment() {
    final scaleDiff = (_maskScale - 1.0).abs();
    _alignmentScore = scaleDiff < 0.2 ? 1.0 - scaleDiff : 0.0;
    _isMaskAligned = _alignmentScore > 0.8;
  }

  Future<void> _captureFrame() async {
    if (_controller == null || !_controller!.value.isInitialized || _isCapturing) return;
    if (!_isMaskAligned) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Пожалуйста, совместите маску с отверстием цилиндра')),
      );
      return;
    }
    setState(() => _isCapturing = true);
    try {
      final XFile file = await _controller!.takePicture();
      final Uint8List bytes = await File(file.path).readAsBytes();
      final imageSize = Size(_controller!.value.previewSize!.height.toDouble(), _controller!.value.previewSize!.width.toDouble());
      final scaleFactor = (150.0 * _maskScale) / 10.0;
      final screenCenter = Offset(_maskPosition.dx * MediaQuery.of(context).size.width, _maskPosition.dy * MediaQuery.of(context).size.height);
      final captureContext = CaptureContext(imageBytes: bytes, imageResolution: imageSize, scaleFactor: scaleFactor, markerCenter: screenCenter, timestamp: DateTime.now());
      widget.onCapture?.call(captureContext);
    } catch (e) {
      debugPrint('Capture error: $e');
    } finally {
      setState(() => _isCapturing = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          if (_isInitialized && _controller != null) CameraPreview(_controller!) else const Center(child: CircularProgressIndicator(color: Colors.white)),
          Positioned.fill(
            child: GestureDetector(
              onScaleUpdate: _onScaleUpdate,
              child: RepaintBoundary(
                child: CustomPaint(painter: DINMaskPainter(position: _maskPosition, scale: _maskScale, alignmentScore: _alignmentScore, isAligned: _isMaskAligned)),
              ),
            ),
          ),
          SafeArea(
            child: Column(
              children: [
                _buildTopBar(),
                const Spacer(),
                _buildBottomControls(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTopBar() {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          IconButton(onPressed: widget.onCancel, icon: const Icon(Icons.close, color: Colors.white, size: 28)),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            decoration: BoxDecoration(color: _isMaskAligned ? Colors.green : Colors.orange, borderRadius: BorderRadius.circular(20)),
            child: Text(_isMaskAligned ? 'Маска совмещена' : 'Совместите маску', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
          ),
          const SizedBox(width: 48),
        ],
      ),
    );
  }

  Widget _buildBottomControls() {
    return Container(
      padding: const EdgeInsets.all(24),
      child: Column(
        children: [
          const Text('Перетащите маску на отверстие цилиндра', textAlign: TextAlign.center, style: TextStyle(color: Colors.white70, fontSize: 14)),
          const SizedBox(height: 24),
          GestureDetector(
            onTap: _captureFrame,
            child: Container(
              width: 80,
              height: 80,
              decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: Colors.white, width: 4), color: _isMaskAligned ? Colors.green : Colors.transparent),
              child: _isCapturing ? const CircularProgressIndicator(color: Colors.white) : Icon(_isMaskAligned ? Icons.check : Icons.camera_alt, color: Colors.white, size: 36),
            ),
          ),
          const SizedBox(height: 16),
          Text('Точность: ${(_alignmentScore * 100).toInt()}%', style: TextStyle(color: _isMaskAligned ? Colors.green : Colors.orange, fontWeight: FontWeight.bold)),
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

  DINMaskPainter({required this.position, required this.scale, required this.alignmentScore, required this.isAligned});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(position.dx * size.width, position.dy * size.height);
    const maskWidth = 150.0;
    const maskHeight = 100.0;
    final paint = Paint()..color = isAligned ? Colors.green.withOpacity(0.5) : Colors.red.withOpacity(0.5)..style = PaintingStyle.fill;
    final strokePaint = Paint()..color = isAligned ? Colors.green : Colors.red..style = PaintingStyle.stroke..strokeWidth = 3;
    canvas.save();
    canvas.translate(center.dx, center.dy);
    canvas.scale(scale);
    final rect = Rect.fromCenter(center: Offset.zero, width: maskWidth, height: maskHeight);
    final dinPath = _buildDINPath(rect);
    canvas.drawPath(dinPath, paint);
    canvas.drawPath(dinPath, strokePaint);
    canvas.restore();
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
  bool shouldRepaint(covariant DINMaskPainter oldDelegate) => position != oldDelegate.position || scale != oldDelegate.scale || isAligned != oldDelegate.isAligned;
}
