class AppConstants {
  static const String appName = 'AI Lock Selector';
  static const String appVersion = '1.0.0';
  static const String baseUrl = 'http://localhost:8001';

  // DIN Euro Cylinder Hole dimensions (mm) - for CV calibration
  static const double dinCylinderWidth = 10.0;
  static const double dinCylinderHeight = 17.0;
  static const double dinHoleWidth = 17.0;
  static const double dinHoleHeight = 33.0;

  // Derived proportions for mask rendering
  static const double dinHoleTopRadius = 8.5;
  static const double dinHoleBottomRadius = 5.0;

  static const double minConfidence = 0.7;
  static const double backsetTolerance = 2.0;
  static const double centerDistanceTolerance = 3.0;
  static const double plateWidthTolerance = 2.0;
  static const double plateHeightTolerance = 3.0;
}

class AssetPaths {
  static const String masksPath = 'assets/masks/';
  static const String imagesPath = 'assets/images/';
}
