import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/constants.dart';
import 'core/router.dart';

void main() {
  runApp(const ProviderScope(child: AILockSelectorApp()));
}

class AILockSelectorApp extends StatelessWidget {
  const AILockSelectorApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: AppConstants.appName,
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      routerConfig: appRouter,
    );
  }
}
