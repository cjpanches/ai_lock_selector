import 'package:equatable/equatable.dart';

class LockProfile extends Equatable {
  final String? id;
  final LockDimensions dimensions;
  final List<MountingHole> mountingHoles;
  final HandleSquarePosition? handleSquare;
  final CylinderHolePosition? cylinderHole;
  final double confidence;
  final DateTime capturedAt;
  final String? imagePath;

  const LockProfile({
    this.id,
    required this.dimensions,
    required this.mountingHoles,
    this.handleSquare,
    this.cylinderHole,
    required this.confidence,
    required this.capturedAt,
    this.imagePath,
  });

  Map<String, dynamic> toJson() => {
    'id': id,
    'dimensions': dimensions.toJson(),
    'mounting_holes': mountingHoles.map((h) => h.toJson()).toList(),
    'handle_square': handleSquare?.toJson(),
    'cylinder_hole': cylinderHole?.toJson(),
    'confidence': confidence,
    'captured_at': capturedAt.toIso8601String(),
    'image_path': imagePath,
  };

  @override
  List<Object?> get props => [id, dimensions, mountingHoles, handleSquare, confidence, capturedAt];
}

class LockDimensions extends Equatable {
  final double backset;
  final double centerDistance;
  final double plateWidth;
  final double plateHeight;
  final double plateThickness;
  final double bodyWidth;
  final double bodyHeight;
  final double bodyDepth;

  const LockDimensions({
    required this.backset,
    required this.centerDistance,
    required this.plateWidth,
    required this.plateHeight,
    required this.plateThickness,
    required this.bodyWidth,
    required this.bodyHeight,
    required this.bodyDepth,
  });

  Map<String, dynamic> toJson() => {
    'backset': backset,
    'center_distance': centerDistance,
    'plate_width': plateWidth,
    'plate_height': plateHeight,
    'plate_thickness': plateThickness,
    'body_width': bodyWidth,
    'body_height': bodyHeight,
    'body_depth': bodyDepth,
  };

  @override
  List<Object?> get props => [backset, centerDistance, plateWidth, plateHeight, plateThickness, bodyWidth, bodyHeight, bodyDepth];
}

class MountingHole extends Equatable {
  final double x;
  final double y;
  final double diameter;

  const MountingHole({required this.x, required this.y, required this.diameter});

  Map<String, dynamic> toJson() => {'x': x, 'y': y, 'diameter': diameter};

  @override
  List<Object?> get props => [x, y, diameter];
}

class HandleSquarePosition extends Equatable {
  final double x;
  final double y;
  final double size;

  const HandleSquarePosition({required this.x, required this.y, required this.size});

  Map<String, dynamic> toJson() => {'x': x, 'y': y, 'size': size};

  @override
  List<Object?> get props => [x, y, size];
}

class CylinderHolePosition extends Equatable {
  final double x;
  final double y;
  final double width;
  final double height;

  const CylinderHolePosition({required this.x, required this.y, required this.width, required this.height});

  Map<String, dynamic> toJson() => {'x': x, 'y': y, 'width': width, 'height': height};

  @override
  List<Object?> get props => [x, y, width, height];
}
