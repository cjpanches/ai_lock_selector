import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

final dioProvider = Provider<Dio>((ref) {
  return Dio(BaseOptions(
    baseUrl: 'http://10.0.2.2:8000/api/v1',
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 30),
  ));
});

final cvServiceProvider = Provider<CVService>((ref) {
  return CVService(ref.read(dioProvider));
});

class CVService {
  final Dio _dio;

  CVService(this._dio);

  Future<Map<String, dynamic>> processImage({
    required String imageBase64,
    double? scaleFactor,
    double? markerX,
    double? markerY,
  }) async {
    try {
      final response = await _dio.post(
        '/cv/process',
        data: {
          'image': imageBase64,
          'scale_factor': scaleFactor,
          'marker_x': markerX,
          'marker_y': markerY,
        },
      );
      return response.data;
    } catch (e) {
      return {
        'success': false,
        'error': e.toString(),
      };
    }
  }

  Future<Map<String, dynamic>> detectLock({
    required String imageBase64,
  }) async {
    try {
      final response = await _dio.post(
        '/cv/detect',
        data: {
          'image': imageBase64,
        },
      );
      return response.data;
    } catch (e) {
      return {
        'success': false,
        'error': e.toString(),
      };
    }
  }
}
