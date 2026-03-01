# App Flow

## User Journey

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Welcome   │────▶│   Camera     │────▶│  AR Align   │
│   Screen    │     │   Screen    │     │   Screen    │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Catalog   │◀────│   Results   │◀────│  Processing │
│   Screen    │     │   Screen    │     │   Screen    │
└─────────────┘     └─────────────┘     └─────────────┘
```

## Screen Details

### 1. Welcome Screen
- App logo and title
- "Start" button to begin
- Optional: Language selector

### 2. Camera Screen
- Live camera preview
- AR overlay with euro cylinder mask
- Capture button
- Flash toggle
- Gallery access button

### 3. AR Alignment Screen
- Static image after capture
- AR overlay visible for reference
- "Confirm" and "Retake" buttons
- Optional: Adjust position slider

### 4. Processing Screen
- Loading indicator
- "Analyzing image..." message
- Progress visualization
- Cancel button

### 5. Results Screen
- **Measured Values**:
  - Backset (mm)
  - Center Distance (mm)
  - Plate Width (mm)
  - Plate Height (mm)
- **Confidence Score**: 0-100%
- **Top Matches**: List of matching locks from database
- **Actions**:
  - Save to history
  - Share results
  - Retake photo

### 6. Catalog Screen (Optional)
- Browse all locks in database
- Filter by:
  - Brand
  - Type (embedded, overlay, latch)
  - Backset range
  - Center distance range
- Search by name/vendor code

## API Interactions

### Capture Flow
```dart
// 1. Capture image
final image = await cameraController.takePicture();

// 2. Send to backend
final response = await http.post(
  '/api/v1/measure',
  body: {'image': imageBytes},
);

// 3. Get results
final result = MeasureResponse.fromJson(response.body);
// result.backset, result.centerDistance, result.matches
```

### Match Flow
```dart
// 1. Send measured profile
final response = await http.post(
  '/api/v1/match',
  body: {
    'backset': 45.0,
    'center_distance': 72.0,
    'plate_width': 5.5,
  },
);

// 2. Get matches
final matches = List<LockMatch>.from(response['matches']);
```

## Navigation (GoRouter)

```dart
Routes:
  /                 → WelcomeScreen
  /camera           → CameraScreen
  /ar-align         → ARAlignScreen
  /processing       → ProcessingScreen
  /results          → ResultsScreen
  /catalog          → CatalogScreen
  /catalog/:id      → LockDetailScreen
```

## State Management (Riverpod)

### Providers
```dart
// Camera state
final cameraControllerProvider = StateNotifierProvider<...>

// Measure state
final measureStateProvider = StateNotifierProvider<...>

// Results state
final resultsProvider = StateNotifierProvider<...>

// Database locks
final locksProvider = FutureProvider<List<Lock>>()

// Filter state
final filterProvider = StateProvider<FilterState>()
```

## Error Handling

| Scenario | User Message | Action |
|----------|--------------|--------|
| No lock detected | "Lock not found in image" | Offer retake |
| Poor image quality | "Image too blurry" | Suggest better lighting |
| No matches found | "No matching locks" | Show catalog |
| Network error | "Connection error" | Retry button |

## Related Documents

- [AGENTS.md](./AGENTS.md) - Flutter implementation details
- [OPENCODE_STARTUP.md](./OPENCODE_STARTUP.md) - Quick start
- [08_API_SPEC.md](./08_API_SPEC.md) - API endpoints
