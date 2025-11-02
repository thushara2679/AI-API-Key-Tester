# State Management Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** State Management Patterns & Architecture
**Focus:** Redux, Zustand, Jotai, MobX patterns

---

## 🎯 State Management Principles

1. **Single Source of Truth** - One state object
2. **State is Read-Only** - Immutable updates
3. **Pure Functions** - Deterministic state changes
4. **Normalized State** - Flat, indexed structure
5. **Selectors** - Derive computed values
6. **Side Effects** - Managed separately

---

## 🏢 Redux Patterns

### Store Setup

```typescript
import { configureStore } from '@reduxjs/toolkit';
import featuresReducer from './slices/featuresSlice';
import deploymentsReducer from './slices/deploymentsSlice';

export const store = configureStore({
  reducer: {
    features: featuresReducer,
    deployments: deploymentsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['features/loadFeaturesSuccess'],
      },
    }).concat(loggerMiddleware),
  devTools: process.env.NODE_ENV !== 'production',
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### Slice Pattern

```typescript
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

interface Feature {
  id: string;
  name: string;
  priority: number;
}

interface FeaturesState {
  byId: Record<string, Feature>;
  allIds: string[];
  loading: boolean;
  error: string | null;
}

export const loadFeatures = createAsyncThunk(
  'features/loadFeatures',
  async (_, { rejectWithValue }) => {
    try {
      const response = await fetch('/api/features');
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

const featuresSlice = createSlice({
  name: 'features',
  initialState: {
    byId: {},
    allIds: [],
    loading: false,
    error: null,
  } as FeaturesState,
  reducers: {
    featureAdded(state, action: PayloadAction<Feature>) {
      const feature = action.payload;
      state.byId[feature.id] = feature;
      state.allIds.push(feature.id);
    },
    featureRemoved(state, action: PayloadAction<string>) {
      const id = action.payload;
      delete state.byId[id];
      state.allIds = state.allIds.filter(fId => fId !== id);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loadFeatures.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loadFeatures.fulfilled, (state, action) => {
        state.loading = false;
        const features = action.payload;
        state.byId = {};
        state.allIds = [];
        features.forEach(feature => {
          state.byId[feature.id] = feature;
          state.allIds.push(feature.id);
        });
      })
      .addCase(loadFeatures.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export default featuresSlice.reducer;
export const { featureAdded, featureRemoved } = featuresSlice.actions;
```

### Selectors

```typescript
import { RootState } from './store';
import { createSelector } from '@reduxjs/toolkit';

// Base selector
export const selectFeaturesState = (state: RootState) => state.features;

// Memoized selectors
export const selectAllFeatures = createSelector(
  [selectFeaturesState],
  (featuresState) => featuresState.allIds.map(id => featuresState.byId[id])
);

export const selectFeatureById = createSelector(
  [selectFeaturesState, (_state, id: string) => id],
  (featuresState, id) => featuresState.byId[id]
);

export const selectFeatureCount = createSelector(
  [selectAllFeatures],
  (features) => features.length
);

export const selectHighPriorityFeatures = createSelector(
  [selectAllFeatures],
  (features) => features.filter(f => f.priority >= 8)
);

export const selectLoadingStatus = createSelector(
  [selectFeaturesState],
  (featuresState) => featuresState.loading
);
```

---

## 🪝 Zustand Patterns

```typescript
import { create } from 'zustand';
import { devtools, persist, immer } from 'zustand/middleware';

interface Feature {
  id: string;
  name: string;
  priority: number;
}

interface FeaturesStore {
  features: Feature[];
  selectedId: string | null;
  loading: boolean;
  
  // Actions
  setFeatures: (features: Feature[]) => void;
  addFeature: (feature: Feature) => void;
  removeFeature: (id: string) => void;
  selectFeature: (id: string) => void;
  setLoading: (loading: boolean) => void;
}

const useFeatureStore = create<FeaturesStore>()(
  devtools(
    persist(
      immer((set) => ({
        features: [],
        selectedId: null,
        loading: false,

        setFeatures: (features) => set({ features }),
        
        addFeature: (feature) => set((state) => {
          state.features.push(feature);
        }),
        
        removeFeature: (id) => set((state) => {
          state.features = state.features.filter(f => f.id !== id);
        }),
        
        selectFeature: (id) => set({ selectedId: id }),
        
        setLoading: (loading) => set({ loading }),
      })),
      { name: 'feature-storage' }
    )
  )
);

// Usage
function FeatureList() {
  const features = useFeatureStore(state => state.features);
  const selectedId = useFeatureStore(state => state.selectedId);
  const selectFeature = useFeatureStore(state => state.selectFeature);

  return (
    <ul>
      {features.map(feature => (
        <li
          key={feature.id}
          onClick={() => selectFeature(feature.id)}
          className={selectedId === feature.id ? 'selected' : ''}
        >
          {feature.name}
        </li>
      ))}
    </ul>
  );
}
```

---

## 🎯 Jotai Patterns

```typescript
import { atom, useAtom, useAtomValue, useSetAtom } from 'jotai';

// Atoms
const featuresAtom = atom<Feature[]>([]);
const selectedIdAtom = atom<string | null>(null);
const loadingAtom = atom(false);

// Derived atoms
const selectedFeatureAtom = atom((get) => {
  const features = get(featuresAtom);
  const selectedId = get(selectedIdAtom);
  return features.find(f => f.id === selectedId);
});

const featureCountAtom = atom((get) => {
  return get(featuresAtom).length;
});

// Async atom
const fetchFeaturesAtom = atom(
  null,
  async (_get, set) => {
    const response = await fetch('/api/features');
    const features = await response.json();
    set(featuresAtom, features);
  }
);

// Usage
function FeatureList() {
  const [features] = useAtom(featuresAtom);
  const [selectedId, setSelectedId] = useAtom(selectedIdAtom);
  const _fetch = useSetAtom(fetchFeaturesAtom);

  useEffect(() => {
    _fetch();
  }, [_fetch]);

  return (
    <ul>
      {features.map(feature => (
        <li
          key={feature.id}
          onClick={() => setSelectedId(feature.id)}
          className={selectedId === feature.id ? 'selected' : ''}
        >
          {feature.name}
        </li>
      ))}
    </ul>
  );
}
```

---

## 📊 MobX Patterns

```typescript
import { makeAutoObservable } from 'mobx';
import { observer } from 'mobx-react-lite';

class FeatureStore {
  features: Feature[] = [];
  selectedId: string | null = null;
  loading = false;

  constructor() {
    makeAutoObservable(this);
  }

  get selectedFeature() {
    return this.features.find(f => f.id === this.selectedId);
  }

  get featureCount() {
    return this.features.length;
  }

  setFeatures(features: Feature[]) {
    this.features = features;
  }

  addFeature(feature: Feature) {
    this.features.push(feature);
  }

  removeFeature(id: string) {
    this.features = this.features.filter(f => f.id !== id);
  }

  selectFeature(id: string) {
    this.selectedId = id;
  }

  async loadFeatures() {
    this.loading = true;
    try {
      const response = await fetch('/api/features');
      const features = await response.json();
      this.setFeatures(features);
    } finally {
      this.loading = false;
    }
  }
}

const featureStore = new FeatureStore();

// Component
const FeatureList = observer(() => {
  useEffect(() => {
    featureStore.loadFeatures();
  }, []);

  return (
    <ul>
      {featureStore.features.map(feature => (
        <li
          key={feature.id}
          onClick={() => featureStore.selectFeature(feature.id)}
          className={featureStore.selectedId === feature.id ? 'selected' : ''}
        >
          {feature.name}
        </li>
      ))}
    </ul>
  );
});
```

---

## 🎓 Comparison

| Feature | Redux | Zustand | Jotai | MobX |
|---------|-------|---------|-------|------|
| Boilerplate | High | Low | Low | Low |
| Learning Curve | Steep | Gentle | Gentle | Medium |
| Bundle Size | Large | Small | Small | Medium |
| DevTools | Excellent | Good | Good | Good |
| TypeScript | Excellent | Excellent | Excellent | Excellent |
| Async | Thunks/Saga | Side effects | Atoms | Async flow |

---

## 📚 Related Documents

- React Patterns (react_patterns.md)
- Performance (performance.md)

---

**END OF STATE MANAGEMENT DOCUMENT**
