# Mobile Development Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Mobile Development Guide
**Focus:** React Native & Flutter frameworks

---

## ⚛️ React Native Advanced

### Native Module Development

```typescript
// Android (Java)
package com.example.app;

import com.facebook.react.bridge.NativeModule;
import com.facebook.react.bridge.ReactApplicationContext;
import com.facebook.react.bridge.ReactContext;
import com.facebook.react.bridge.ReactMethod;

public class BiometricModule extends ReactContextBaseJavaModule {
    public BiometricModule(ReactApplicationContext context) {
        super(context);
    }

    @Override
    public String getName() {
        return "BiometricModule";
    }

    @ReactMethod
    public void authenticate(Promise promise) {
        try {
            BiometricPrompt.PromptInfo promptInfo = 
                new BiometricPrompt.PromptInfo.Builder()
                    .setTitle("Authenticate")
                    .setNegativeButtonText("Cancel")
                    .build();

            new BiometricPrompt(getCurrentActivity(), executor, callback)
                .authenticate(promptInfo);

            promise.resolve("authenticated");
        } catch (Exception e) {
            promise.reject("AUTH_ERROR", e);
        }
    }
}

// React Native usage
import { NativeModules } from 'react-native';

const { BiometricModule } = NativeModules;

async function authenticateUser() {
    try {
        const result = await BiometricModule.authenticate();
        console.log(result);
    } catch (error) {
        console.error('Auth failed:', error);
    }
}
```

### Performance Optimization

```typescript
// Memoization
const FeatureItem = React.memo(({ feature, onPress }: any) => (
    <TouchableOpacity onPress={() => onPress(feature)}>
        <Text>{feature.name}</Text>
    </TouchableOpacity>
));

// FlatList optimization
<FlatList
    data={features}
    renderItem={({ item }) => <FeatureItem feature={item} />}
    keyExtractor={item => item.id}
    maxToRenderPerBatch={10}
    updateCellsBatchingPeriod={50}
    removeClippedSubviews={true}
    scrollEventThrottle={16}
    getItemLayout={(data, index) => ({
        length: 100,
        offset: 100 * index,
        index
    })}
/>

// Image optimization
import FastImage from 'react-native-fast-image';

<FastImage
    source={{ uri: imageUrl, cache: FastImage.cacheControl.immutable }}
    style={{ width: 200, height: 200 }}
    resizeMode={FastImage.resizeMode.contain}
/>
```

### Navigation Patterns

```typescript
// React Navigation with deep linking
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import * as Linking from 'expo-linking';

const Stack = createNativeStackNavigator();

const linking = {
    prefixes: ['https://myapp.com', 'myapp://'],
    config: {
        screens: {
            Features: 'features',
            FeatureDetail: 'features/:id',
            Deployments: 'deployments',
        },
    },
};

function RootNavigator() {
    return (
        <NavigationContainer linking={linking}>
            <Stack.Navigator>
                <Stack.Screen name="Features" component={FeaturesScreen} />
                <Stack.Screen
                    name="FeatureDetail"
                    component={FeatureDetailScreen}
                    options={({ route }) => ({
                        title: route.params.name,
                    })}
                />
            </Stack.Navigator>
        </NavigationContainer>
    );
}
```

---

## 🎯 Flutter Framework

### Dart Basics & State Management

```dart
// StatefulWidget
class FeatureScreen extends StatefulWidget {
    const FeatureScreen({Key? key}) : super(key: key);

    @override
    State<FeatureScreen> createState() => _FeatureScreenState();
}

class _FeatureScreenState extends State<FeatureScreen> {
    List<Feature> features = [];
    bool isLoading = false;

    @override
    void initState() {
        super.initState();
        _loadFeatures();
    }

    Future<void> _loadFeatures() async {
        setState(() => isLoading = true);
        try {
            final loadedFeatures = await FeatureService.getFeatures();
            setState(() => features = loadedFeatures);
        } catch (e) {
            _showError(e.toString());
        } finally {
            setState(() => isLoading = false);
        }
    }

    void _showError(String message) {
        ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(message)),
        );
    }

    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(title: const Text('Features')),
            body: isLoading
                ? const Center(child: CircularProgressIndicator())
                : ListView.builder(
                    itemCount: features.length,
                    itemBuilder: (context, index) {
                        return FeatureItem(feature: features[index]);
                    },
                ),
        );
    }
}
```

### Provider Pattern (State Management)

```dart
// Define provider
class FeatureProvider with ChangeNotifier {
    List<Feature> _features = [];
    bool _isLoading = false;

    List<Feature> get features => _features;
    bool get isLoading => _isLoading;

    Future<void> loadFeatures() async {
        _isLoading = true;
        notifyListeners();

        try {
            _features = await FeatureService.getFeatures();
        } catch (e) {
            print('Error: $e');
        } finally {
            _isLoading = false;
            notifyListeners();
        }
    }

    void addFeature(Feature feature) {
        _features.add(feature);
        notifyListeners();
    }

    void deleteFeature(String id) {
        _features.removeWhere((f) => f.id == id);
        notifyListeners();
    }
}

// Use provider
class FeatureScreen extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        return Scaffold(
            body: Consumer<FeatureProvider>(
                builder: (context, provider, _) {
                    if (provider.isLoading) {
                        return const Center(child: CircularProgressIndicator());
                    }

                    return ListView.builder(
                        itemCount: provider.features.length,
                        itemBuilder: (context, index) {
                            final feature = provider.features[index];
                            return ListTile(
                                title: Text(feature.name),
                                onTap: () => provider.deleteFeature(feature.id),
                            );
                        },
                    );
                },
            ),
            floatingActionButton: FloatingActionButton(
                onPressed: () {
                    context.read<FeatureProvider>()
                        .loadFeatures();
                },
                child: const Icon(Icons.refresh),
            ),
        );
    }
}

// Provide at app level
void main() {
    runApp(
        MultiProvider(
            providers: [
                ChangeNotifierProvider(create: (_) => FeatureProvider()),
            ],
            child: const MyApp(),
        ),
    );
}
```

### Navigation in Flutter

```dart
import 'package:go_router/go_router.dart';

// Define routes
final router = GoRouter(
    routes: [
        GoRoute(
            path: '/',
            builder: (context, state) => const FeaturesScreen(),
            routes: [
                GoRoute(
                    path: 'feature/:id',
                    builder: (context, state) {
                        final id = state.pathParameters['id']!;
                        return FeatureDetailScreen(id: id);
                    },
                ),
            ],
        ),
    ],
);

// Use in app
void main() {
    runApp(MaterialApp.router(
        routerConfig: router,
        title: 'Feature Manager',
    ));
}

// Navigate
void navigateToFeature(BuildContext context, String id) {
    context.push('/feature/$id');
}
```

### Platform Channels

```dart
// Dart side
import 'package:flutter/services.dart';

class PlatformService {
    static const platform = MethodChannel('com.example.app/platform');

    static Future<String> authenticate() async {
        try {
            final String result = await platform.invokeMethod('authenticate');
            return result;
        } catch (e) {
            return 'Failed to authenticate: $e';
        }
    }

    static Future<void> vibrate(int duration) async {
        try {
            await platform.invokeMethod('vibrate', {'duration': duration});
        } catch (e) {
            print('Error: $e');
        }
    }
}

// Kotlin side
import android.os.Build
import android.os.VibrationEffect
import android.os.Vibrator
import androidx.annotation.NonNull
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.embedding.engine.dart.DartExecutor
import io.flutter.plugin.common.MethodChannel

class MainActivity: FlutterActivity() {
    private val CHANNEL = "com.example.app/platform"

    override fun configureFlutterEngine(@NonNull flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
            .setMethodCallHandler { call, result ->
                when (call.method) {
                    "authenticate" -> {
                        result.success("authenticated")
                    }
                    "vibrate" -> {
                        val duration = call.argument<Int>("duration") ?: 100
                        val vibrator = getSystemService(Vibrator::class.java)
                        if (Build.VERSION.SDK_INT >= 26) {
                            vibrator.vibrate(
                                VibrationEffect.createOneShot(
                                    duration.toLong(),
                                    VibrationEffect.DEFAULT_AMPLITUDE
                                )
                            )
                        } else {
                            vibrator.vibrate(duration.toLong())
                        }
                        result.success(null)
                    }
                    else -> result.notImplemented()
                }
            }
    }
}
```

---

## 🔄 Cross-Platform Data Sync

### Offline-First Architecture

```dart
// Local database with Hive
import 'package:hive/hive.dart';

@HiveType()
class Feature {
    @HiveField(0)
    final String id;

    @HiveField(1)
    final String name;

    @HiveField(2)
    final int priority;

    @HiveField(3)
    final DateTime? syncedAt;

    Feature({
        required this.id,
        required this.name,
        required this.priority,
        this.syncedAt,
    });
}

// Repository pattern
class FeatureRepository {
    late Box<Feature> _box;

    Future<void> init() async {
        Hive.registerAdapter(FeatureAdapter());
        _box = await Hive.openBox<Feature>('features');
    }

    Future<List<Feature>> getFeatures() async {
        try {
            // Try network first
            final features = await _fetchFromNetwork();
            
            // Save to local
            await _box.clear();
            for (var feature in features) {
                await _box.put(feature.id, feature);
            }
            
            return features;
        } catch (e) {
            // Fall back to local
            return _box.values.toList();
        }
    }

    Future<void> addFeature(Feature feature) async {
        // Save locally
        await _box.put(feature.id, feature);

        // Sync when online
        try {
            await _syncFeatures();
        } catch (e) {
            print('Sync failed: $e');
        }
    }

    Future<void> _syncFeatures() async {
        final unsyncedFeatures = _box.values
            .where((f) => f.syncedAt == null)
            .toList();

        for (var feature in unsyncedFeatures) {
            await _uploadToServer(feature);
        }
    }

    Future<List<Feature>> _fetchFromNetwork() async {
        // API call
    }

    Future<void> _uploadToServer(Feature feature) async {
        // API call
    }
}
```

---

## 🎬 Animation & UI

### Flutter Animations

```dart
class FeatureAnimation extends StatefulWidget {
    @override
    State<FeatureAnimation> createState() => _FeatureAnimationState();
}

class _FeatureAnimationState extends State<FeatureAnimation>
    with SingleTickerProviderStateMixin {
    late AnimationController _controller;
    late Animation<double> _opacityAnimation;

    @override
    void initState() {
        super.initState();
        _controller = AnimationController(
            duration: const Duration(seconds: 2),
            vsync: this,
        );

        _opacityAnimation = Tween<double>(begin: 0.0, end: 1.0)
            .animate(CurvedAnimation(parent: _controller, curve: Curves.easeIn));

        _controller.forward();
    }

    @override
    Widget build(BuildContext context) {
        return FadeTransition(
            opacity: _opacityAnimation,
            child: const Text('Animated Text'),
        );
    }

    @override
    void dispose() {
        _controller.dispose();
        super.dispose();
    }
}
```

---

## 📊 Performance Optimization

### Memory Management

```dart
// Dispose resources
@override
void dispose() {
    _controller?.dispose();
    _subscription?.cancel();
    super.dispose();
}

// Lazy evaluation
class LazyWidget extends StatefulWidget {
    @override
    State<LazyWidget> createState() => _LazyWidgetState();
}

class _LazyWidgetState extends State<LazyWidget> {
    Future<List<Feature>>? _futureFeatures;

    @override
    void initState() {
        super.initState();
        _futureFeatures = FeatureService.getFeatures();
    }

    @override
    Widget build(BuildContext context) {
        return FutureBuilder<List<Feature>>(
            future: _futureFeatures,
            builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                    return const CircularProgressIndicator();
                }
                return ListView(
                    children: snapshot.data?.map((f) => Text(f.name)).toList() ?? [],
                );
            },
        );
    }
}
```

---

## 📚 Related Documents

- Desktop Development (desktop_development.md)
- Cross-Platform Strategies (cross_platform.md)
- Native iOS Development (native_ios.md)
- Native Android Development (native_android.md)

---

**END OF MOBILE DEVELOPMENT DOCUMENT**
