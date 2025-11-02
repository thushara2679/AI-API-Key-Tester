# React Native Patterns Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** React Native Patterns & Techniques Guide
**React Native Version:** 0.72+
**Focus:** Production-grade React Native with 150+ techniques

---

## 📖 Introduction

Comprehensive guide for React Native development covering iOS/Android, native modules, performance, and best practices.

---

## 🎯 Core React Native Patterns

### Component Structure

```typescript
// ✅ GOOD: Functional component with TypeScript
import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  ActivityIndicator,
} from 'react-native';

interface Feature {
  id: string;
  name: string;
  priority: number;
}

interface FeatureListProps {
  features: Feature[];
  onSelectFeature: (feature: Feature) => void;
}

export const FeatureList: React.FC<FeatureListProps> = ({
  features,
  onSelectFeature,
}) => {
  const [isLoading, setIsLoading] = useState(false);

  const renderItem = ({ item }: { item: Feature }) => (
    <FeatureItem
      feature={item}
      onPress={() => onSelectFeature(item)}
    />
  );

  return (
    <View style={styles.container}>
      {isLoading && <ActivityIndicator size="large" />}
      <FlatList
        data={features}
        renderItem={renderItem}
        keyExtractor={(item) => item.id}
        onEndReachedThreshold={0.5}
        onEndReached={() => {
          // Load more
        }}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 16,
  },
});
```

### Navigation Patterns

```typescript
// React Navigation with TypeScript
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

type RootStackParamList = {
  FeatureList: undefined;
  FeatureDetail: { featureId: string };
  CreateFeature: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator();

function FeatureStack() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: true,
        headerTintColor: '#007AFF',
      }}
    >
      <Stack.Screen
        name="FeatureList"
        component={FeatureListScreen}
        options={{ title: 'Features' }}
      />
      <Stack.Screen
        name="FeatureDetail"
        component={FeatureDetailScreen}
        options={({ route }) => ({
          title: route.params.featureId,
        })}
      />
    </Stack.Navigator>
  );
}

function RootNavigator() {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen
          name="Features"
          component={FeatureStack}
          options={{
            tabBarIcon: ({ color }) => (
              <Ionicons name="list" color={color} />
            ),
          }}
        />
        <Tab.Screen
          name="Settings"
          component={SettingsScreen}
          options={{
            tabBarIcon: ({ color }) => (
              <Ionicons name="settings" color={color} />
            ),
          }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
```

---

## 📱 Platform-Specific Code

```typescript
import { Platform, StyleSheet } from 'react-native';

// Platform-specific styling
const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.OS === 'android' ? 25 : 0,
    flex: 1,
  },
  text: {
    fontSize: Platform.OS === 'ios' ? 16 : 14,
  },
});

// Platform-specific components
import { useWindowDimensions } from 'react-native';

function ResponsiveLayout() {
  const { width } = useWindowDimensions();
  const isTablet = width > 768;

  return isTablet ? <TabletLayout /> : <PhoneLayout />;
}

// Platform-specific native modules
import { NativeModules } from 'react-native';

const { DeviceInfo } = NativeModules;

function useDeviceInfo() {
  const [info, setInfo] = useState<any>(null);

  useEffect(() => {
    DeviceInfo.getDeviceInfo().then(setInfo);
  }, []);

  return info;
}
```

---

## 🔄 State Management with Redux

```typescript
import { configureStore } from '@reduxjs/toolkit';
import { createSlice } from '@reduxjs/toolkit';
import { useAppDispatch, useAppSelector } from './store';

// Feature slice
const featureSlice = createSlice({
  name: 'features',
  initialState: {
    items: [] as Feature[],
    loading: false,
    error: null as string | null,
  },
  reducers: {
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    setFeatures: (state, action) => {
      state.items = action.payload;
      state.loading = false;
    },
    setError: (state, action) => {
      state.error = action.payload;
      state.loading = false;
    },
  },
});

// Store
export const store = configureStore({
  reducer: {
    features: featureSlice.reducer,
  },
});

// Hooks
export const useFeatures = () => {
  const dispatch = useAppDispatch();
  const features = useAppSelector(state => state.features.items);

  const loadFeatures = useCallback(async () => {
    dispatch(featureSlice.actions.setLoading(true));
    try {
      const data = await fetchFeatures();
      dispatch(featureSlice.actions.setFeatures(data));
    } catch (error) {
      dispatch(featureSlice.actions.setError(error.message));
    }
  }, [dispatch]);

  return { features, loadFeatures };
};
```

---

## 🎨 Styling Patterns

```typescript
// Tailwind-like utility approach with StyleSheet
const utilities = StyleSheet.create({
  // Margin utilities
  m0: { margin: 0 },
  m4: { margin: 16 },
  m8: { margin: 32 },
  
  // Padding utilities
  p0: { padding: 0 },
  p4: { padding: 16 },
  p8: { padding: 32 },
  
  // Flex utilities
  flex: { flex: 1 },
  flexRow: { flexDirection: 'row' },
  flexCenter: { justifyContent: 'center', alignItems: 'center' },
  
  // Text utilities
  textCenter: { textAlign: 'center' },
  textWhite: { color: '#fff' },
});

// Theme-based styling
const theme = {
  colors: {
    primary: '#007AFF',
    secondary: '#5AC8FA',
    success: '#4CD964',
    danger: '#FF3B30',
    background: '#F2F2F7',
  },
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
  },
};

interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  onPress: () => void;
  children: string;
}

const Button: React.FC<ButtonProps> = ({ variant, onPress, children }) => {
  const backgroundColor = theme.colors[variant];
  
  return (
    <TouchableOpacity
      style={[
        utilities.m4,
        utilities.flexCenter,
        { backgroundColor, paddingVertical: theme.spacing.md },
        styles.button,
      ]}
      onPress={onPress}
    >
      <Text style={styles.buttonText}>{children}</Text>
    </TouchableOpacity>
  );
};
```

---

## 🌐 Networking & API

```typescript
// Custom API hook
function useAPI<T>(endpoint: string, options?: RequestInit) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    const fetchData = async () => {
      try {
        const response = await fetch(
          `https://api.example.com${endpoint}`,
          {
            ...options,
            signal: controller.signal,
            headers: {
              'Content-Type': 'application/json',
              ...options?.headers,
            },
          }
        );

        if (!response.ok) {
          throw new Error(`API Error: ${response.status}`);
        }

        const result = await response.json();
        setData(result);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err as Error);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    return () => controller.abort();
  }, [endpoint]);

  return { data, loading, error };
}

// Usage
function FeatureListScreen() {
  const { data: features, loading } = useAPI<Feature[]>('/features');
  
  return (
    <FlatList
      data={features}
      renderItem={({ item }) => <FeatureItem feature={item} />}
      keyExtractor={item => item.id}
      ListEmptyComponent={
        loading ? <ActivityIndicator /> : <Text>No features</Text>
      }
    />
  );
}
```

---

## 💾 Local Storage

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';

// Custom hook for AsyncStorage
function useAsyncStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(initialValue);

  // Load from storage on mount
  useEffect(() => {
    const loadValue = async () => {
      try {
        const stored = await AsyncStorage.getItem(key);
        if (stored) {
          setValue(JSON.parse(stored));
        }
      } catch (error) {
        console.error('Error loading from storage:', error);
      }
    };

    loadValue();
  }, [key]);

  // Save to storage when value changes
  const setValue2 = useCallback(
    async (newValue: T) => {
      try {
        setValue(newValue);
        await AsyncStorage.setItem(key, JSON.stringify(newValue));
      } catch (error) {
        console.error('Error saving to storage:', error);
      }
    },
    [key]
  );

  return [value, setValue2] as const;
}

// Usage
function UserPreferences() {
  const [theme, setTheme] = useAsyncStorage('theme', 'light');
  const [fontSize, setFontSize] = useAsyncStorage('fontSize', 16);

  return (
    <View>
      <Picker
        selectedValue={theme}
        onValueChange={setTheme}
      >
        <Picker.Item label="Light" value="light" />
        <Picker.Item label="Dark" value="dark" />
      </Picker>
    </View>
  );
}
```

---

## 📸 Camera & Media

```typescript
import { launchCamera, launchImageLibrary } from 'react-native-image-picker';

function CameraScreen() {
  const [image, setImage] = useState<any>(null);

  const takePhoto = async () => {
    try {
      const result = await launchCamera({
        mediaType: 'photo',
        includeBase64: false,
      });

      if (result.assets && result.assets.length > 0) {
        setImage(result.assets[0]);
      }
    } catch (error) {
      console.error('Camera error:', error);
    }
  };

  const selectFromLibrary = async () => {
    try {
      const result = await launchImageLibrary({
        mediaType: 'photo',
      });

      if (result.assets && result.assets.length > 0) {
        setImage(result.assets[0]);
      }
    } catch (error) {
      console.error('Library error:', error);
    }
  };

  return (
    <View style={styles.container}>
      {image && (
        <Image
          source={{ uri: image.uri }}
          style={styles.image}
        />
      )}
      <Button title="Take Photo" onPress={takePhoto} />
      <Button title="Choose from Library" onPress={selectFromLibrary} />
    </View>
  );
}
```

---

## 🔔 Push Notifications

```typescript
import PushNotification from 'react-native-push-notification';

// Setup push notifications
PushNotification.configure({
  onNotification(notification) {
    console.log('Notification received:', notification);
  },
  permissions: {
    alert: true,
    badge: true,
    sound: true,
  },
});

// Send notification
function sendNotification(title: string, message: string) {
  PushNotification.localNotification({
    channelId: 'default',
    title,
    message,
    priority: 'high',
  });
}

// Schedule notification
function scheduleNotification(title: string, message: string, delayMs: number) {
  PushNotification.localNotificationSchedule({
    channelId: 'default',
    title,
    message,
    date: new Date(Date.now() + delayMs),
  });
}
```

---

## 🧪 Testing

```typescript
import { render, screen, fireEvent } from '@testing-library/react-native';

describe('FeatureList', () => {
  it('renders feature list', () => {
    const features = [
      { id: '1', name: 'Feature 1', priority: 1 },
    ];

    render(<FeatureList features={features} onSelectFeature={jest.fn()} />);
    
    expect(screen.getByText('Feature 1')).toBeTruthy();
  });

  it('calls onSelectFeature when item pressed', () => {
    const features = [
      { id: '1', name: 'Feature 1', priority: 1 },
    ];
    const onSelect = jest.fn();

    render(<FeatureList features={features} onSelectFeature={onSelect} />);
    
    fireEvent.press(screen.getByText('Feature 1'));
    
    expect(onSelect).toHaveBeenCalledWith(features[0]);
  });
});
```

---

## ⚡ Performance Optimization

```typescript
// Memoization
const FeatureItem = React.memo(
  ({ feature, onPress }: any) => (
    <TouchableOpacity onPress={() => onPress(feature)}>
      <Text>{feature.name}</Text>
    </TouchableOpacity>
  ),
  (prevProps, nextProps) => {
    return prevProps.feature.id === nextProps.feature.id;
  }
);

// FlatList optimization
<FlatList
  data={features}
  renderItem={renderItem}
  keyExtractor={item => item.id}
  maxToRenderPerBatch={10}
  updateCellsBatchingPeriod={50}
  removeClippedSubviews={true}
  scrollEventThrottle={16}
  ListEmptyComponent={<EmptyState />}
  ListHeaderComponent={<Header />}
/>

// Image optimization
import FastImage from 'react-native-fast-image';

<FastImage
  source={{ uri: imageUrl }}
  style={{ width: 200, height: 200 }}
  resizeMode={FastImage.resizeMode.contain}
/>
```

---

## 📚 Related Documents

- State Management (state_management.md)
- Performance (performance.md)
- UI/UX Patterns (ui_ux_patterns.md)

---

**END OF REACT NATIVE PATTERNS DOCUMENT**
