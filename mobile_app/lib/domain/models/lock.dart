class LockType {
  static const String embedded = 'embedded';
  static const String overlay = 'overlay';
  static const String latch = 'latch';
  static const String deadbolt = 'deadbolt';
  static const String electronic = 'electronic';
  static const String cylinder = 'cylinder';

  static String getDisplayName(String type) {
    switch (type) {
      case embedded:
        return 'Врезной';
      case overlay:
        return 'Накладной';
      case latch:
        return 'Защёлка';
      case deadbolt:
        return 'Врезной с задвижкой';
      case electronic:
        return 'Электронный';
      case cylinder:
        return 'Цилиндровый';
      default:
        return type;
    }
  }

  static String getIcon(String type) {
    switch (type) {
      case embedded:
        return 'lock';
      case overlay:
        return 'lock_open';
      case latch:
        return 'door_front';
      case deadbolt:
        return 'lock';
      case electronic:
        return 'smart_toy';
      case cylinder:
        return 'vpn_key';
      default:
        return 'lock';
    }
  }
}

class Lock {
  final int? id;
  final String vendorCode;
  final String name;
  final String? brand;
  final String type;
  final double backset;
  final double centerDistance;
  final double plateWidth;
  final double plateHeight;
  final double plateThickness;
  final double bodyWidth;
  final double bodyHeight;
  final double bodyDepth;
  final double? cylinderHoleDiameter;
  final double? squareHoleSize;
  final String? imageUrl;
  final String? drawingUrl;
  final String? description;

  Lock({
    this.id,
    required this.vendorCode,
    required this.name,
    this.brand,
    required this.type,
    required this.backset,
    required this.centerDistance,
    required this.plateWidth,
    required this.plateHeight,
    required this.plateThickness,
    required this.bodyWidth,
    required this.bodyHeight,
    required this.bodyDepth,
    this.cylinderHoleDiameter,
    this.squareHoleSize,
    this.imageUrl,
    this.drawingUrl,
    this.description,
  });

  factory Lock.fromJson(Map<String, dynamic> json) {
    return Lock(
      id: json['id'],
      vendorCode: json['vendor_code'] ?? '',
      name: json['name'] ?? '',
      brand: json['brand'],
      type: json['type'] ?? 'embedded',
      backset: (json['backset'] ?? 0).toDouble(),
      centerDistance: (json['center_distance'] ?? 0).toDouble(),
      plateWidth: (json['plate_width'] ?? 0).toDouble(),
      plateHeight: (json['plate_height'] ?? 0).toDouble(),
      plateThickness: (json['plate_thickness'] ?? 0).toDouble(),
      bodyWidth: (json['body_width'] ?? 0).toDouble(),
      bodyHeight: (json['body_height'] ?? 0).toDouble(),
      bodyDepth: (json['body_depth'] ?? 0).toDouble(),
      cylinderHoleDiameter: json['cylinder_hole_diameter']?.toDouble(),
      squareHoleSize: json['square_hole_size']?.toDouble(),
      imageUrl: json['image_url'],
      drawingUrl: json['drawing_url'],
      description: json['description'],
    );
  }

  String get typeDisplayName => LockType.getDisplayName(type);
}
