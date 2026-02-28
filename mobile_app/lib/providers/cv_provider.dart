import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../core/constants.dart';

const int maxRetries = 3;
const Duration requestTimeout = Duration(seconds: 10);

final dioProvider = Provider<Dio>((ref) {
  return Dio(BaseOptions(
    baseUrl: '${AppConstants.baseUrl}/api/v1',
    connectTimeout: requestTimeout,
    receiveTimeout: requestTimeout,
  ));
});

final cvServiceProvider = Provider<CVService>((ref) {
  return CVService(ref.read(dioProvider));
});

class CVService {
  final Dio _dio;

  CVService(this._dio);

  Future<Map<String, dynamic>> _executeWithRetry(
    Future<Response> Function() request,
  ) async {
    int attempts = 0;
    DioException? lastError;

    while (attempts < maxRetries) {
      try {
        final response = await request();
        return response.data;
      } on DioException catch (e) {
        lastError = e;
        attempts++;
        if (attempts < maxRetries) {
          await Future.delayed(Duration(milliseconds: 500 * attempts));
        }
      } catch (e) {
        return {
          'success': false,
          'error': e.toString(),
        };
      }
    }

    return {
      'success': false,
      'error': 'Max retries exceeded: ${lastError?.message ?? "Unknown error"}',
    };
  }

  Future<Map<String, dynamic>> processImage({
    required String imageBase64,
    double? scaleFactor,
    double? markerX,
    double? markerY,
  }) async {
    return _executeWithRetry(() => _dio.post(
      '/cv/process',
      data: {
        'image': imageBase64,
        'scale_factor': scaleFactor,
        'marker_x': markerX,
        'marker_y': markerY,
      },
    ));
  }

  Future<Map<String, dynamic>> detectLock({
    required String imageBase64,
  }) async {
    return _executeWithRetry(() => _dio.post(
      '/cv/detect',
      data: {
        'image': imageBase64,
      },
    ));
  }
}
