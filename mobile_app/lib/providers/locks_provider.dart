import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../../domain/models/lock.dart';
import '../../core/constants.dart';

const String _baseUrl = '${AppConstants.baseUrl}/api/v1';

class LocksResponse {
  final List<Lock> locks;
  final int total;

  LocksResponse({required this.locks, required this.total});

  factory LocksResponse.fromJson(Map<String, dynamic> json) {
    return LocksResponse(
      locks: (json['locks'] as List)
          .map((lock) => Lock.fromJson(lock))
          .toList(),
      total: json['total'] ?? 0,
    );
  }
}

class ApiException implements Exception {
  final String message;
  final int? statusCode;

  ApiException(this.message, {this.statusCode});

  @override
  String toString() => message;
}

Future<LocksResponse> fetchLocks({String? type, String? brand, int limit = 100, int offset = 0}) async {
  final queryParams = <String, String>{
    'limit': limit.toString(),
    'offset': offset.toString(),
  };
  if (type != null) queryParams['type'] = type;
  if (brand != null) queryParams['brand'] = brand;

  final uri = Uri.parse('$_baseUrl/locks').replace(queryParameters: queryParams);
  
  try {
    final response = await http.get(uri).timeout(const Duration(seconds: 10));
    
    if (response.statusCode == 200) {
      return LocksResponse.fromJson(json.decode(response.body));
    } else {
      throw ApiException('Failed to load locks', statusCode: response.statusCode);
    }
  } catch (e) {
    if (e is ApiException) rethrow;
    throw ApiException('Network error: $e');
  }
}

Future<Lock> fetchLock(int id) async {
  final uri = Uri.parse('$_baseUrl/locks/$id');
  
  try {
    final response = await http.get(uri).timeout(const Duration(seconds: 10));
    
    if (response.statusCode == 200) {
      return Lock.fromJson(json.decode(response.body));
    } else if (response.statusCode == 404) {
      throw ApiException('Lock not found', statusCode: 404);
    } else {
      throw ApiException('Failed to load lock', statusCode: response.statusCode);
    }
  } catch (e) {
    if (e is ApiException) rethrow;
    throw ApiException('Network error: $e');
  }
}

final locksProvider = FutureProvider.family<LocksResponse, LocksFilter>((ref, filter) async {
  return fetchLocks(type: filter.type, brand: filter.brand, limit: filter.limit, offset: filter.offset);
});

final lockDetailProvider = FutureProvider.family<Lock, int>((ref, id) async {
  return fetchLock(id);
});

class LocksFilter {
  final String? type;
  final String? brand;
  final int limit;
  final int offset;

  LocksFilter({this.type, this.brand, this.limit = 100, this.offset = 0});

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is LocksFilter &&
          runtimeType == other.runtimeType &&
          type == other.type &&
          brand == other.brand &&
          limit == other.limit &&
          offset == other.offset;

  @override
  int get hashCode =>
      type.hashCode ^ brand.hashCode ^ limit.hashCode ^ offset.hashCode;
}
