# Vue.js Patterns Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Vue.js Patterns & Techniques Guide
**Vue Version:** 3.3+
**Focus:** Production-grade Vue.js with composition API

---

## 🎯 Composition API Patterns

### Basic Setup

```typescript
<template>
  <div class="features">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <ul v-else>
      <li v-for="feature in features" :key="feature.id">
        {{ feature.name }}
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

interface Feature {
  id: string;
  name: string;
  priority: number;
}

const features = ref<Feature[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);

const sortedFeatures = computed(() => {
  return features.value.sort((a, b) => b.priority - a.priority);
});

const loadFeatures = async () => {
  loading.value = true;
  try {
    const response = await fetch('/api/features');
    features.value = await response.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadFeatures();
});
</script>

<style scoped>
.features {
  padding: 1rem;
}
</style>
```

### Custom Composables

```typescript
// useFeatures.ts
import { ref, reactive, computed } from 'vue';

interface UseFeaturesOptions {
  fetchOnMount?: boolean;
}

export function useFeatures(options: UseFeaturesOptions = {}) {
  const features = ref([]);
  const loading = ref(false);
  const error = ref<string | null>(null);
  const filters = reactive({
    status: 'all',
    priority: 'all',
  });

  const filteredFeatures = computed(() => {
    return features.value.filter(feature => {
      if (filters.status !== 'all' && feature.status !== filters.status) {
        return false;
      }
      if (filters.priority !== 'all' && feature.priority !== filters.priority) {
        return false;
      }
      return true;
    });
  });

  const fetchFeatures = async () => {
    loading.value = true;
    try {
      const response = await fetch('/api/features');
      features.value = await response.json();
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  };

  const createFeature = async (feature: any) => {
    const response = await fetch('/api/features', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(feature),
    });
    const newFeature = await response.json();
    features.value.push(newFeature);
    return newFeature;
  };

  const deleteFeature = async (id: string) => {
    await fetch(`/api/features/${id}`, { method: 'DELETE' });
    features.value = features.value.filter(f => f.id !== id);
  };

  return {
    features,
    filteredFeatures,
    loading,
    error,
    filters,
    fetchFeatures,
    createFeature,
    deleteFeature,
  };
}

// Usage
<script setup lang="ts">
import { useFeatures } from './useFeatures';

const { filteredFeatures, loading, fetchFeatures } = useFeatures();

onMounted(() => {
  fetchFeatures();
});
</script>
```

---

## 🏗️ Component Patterns

### Props and Emits

```typescript
<template>
  <div class="feature-card" @click="selectFeature">
    <h3>{{ feature.name }}</h3>
    <p>Priority: {{ feature.priority }}</p>
    <button @click.stop="deleteFeature">Delete</button>
  </div>
</template>

<script setup lang="ts">
interface Feature {
  id: string;
  name: string;
  priority: number;
}

interface Props {
  feature: Feature;
  highlighted?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  highlighted: false,
});

const emit = defineEmits<{
  select: [feature: Feature];
  delete: [id: string];
}>();

const selectFeature = () => {
  emit('select', props.feature);
};

const deleteFeature = () => {
  emit('delete', props.feature.id);
};
</script>

<style scoped>
.feature-card {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  cursor: pointer;
}

.feature-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
```

### Slots

```typescript
<template>
  <div class="modal">
    <div class="modal-content">
      <header class="modal-header">
        <h2>
          <slot name="title">Default Title</slot>
        </h2>
        <button @click="close">×</button>
      </header>
      
      <main class="modal-body">
        <slot>Default content</slot>
      </main>
      
      <footer class="modal-footer">
        <slot name="footer">
          <button @click="close">Cancel</button>
          <button @click="submit">OK</button>
        </slot>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  submit: [];
  close: [];
}>();

const close = () => emit('close');
const submit = () => emit('submit');
</script>

// Usage
<Modal @close="handleClose" @submit="handleSubmit">
  <template #title>Create Feature</template>
  <FeatureForm />
  <template #footer>
    <button @click="handleCancel">Cancel</button>
    <button @click="handleCreate">Create</button>
  </template>
</Modal>
```

---

## 🎯 State Management with Pinia

```typescript
// stores/featureStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

interface Feature {
  id: string;
  name: string;
  priority: number;
}

export const useFeatureStore = defineStore('features', () => {
  const features = ref<Feature[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const featureCount = computed(() => features.value.length);

  const highPriorityFeatures = computed(() =>
    features.value.filter(f => f.priority >= 8)
  );

  const fetchFeatures = async () => {
    loading.value = true;
    try {
      const response = await fetch('/api/features');
      features.value = await response.json();
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  };

  const addFeature = (feature: Feature) => {
    features.value.push(feature);
  };

  const removeFeature = (id: string) => {
    features.value = features.value.filter(f => f.id !== id);
  };

  return {
    features,
    loading,
    error,
    featureCount,
    highPriorityFeatures,
    fetchFeatures,
    addFeature,
    removeFeature,
  };
});

// Usage in component
<script setup lang="ts">
import { useFeatureStore } from '@/stores/featureStore';

const store = useFeatureStore();

onMounted(() => {
  store.fetchFeatures();
});
</script>

<template>
  <div>
    <p>Total: {{ store.featureCount }}</p>
    <ul>
      <li v-for="feature in store.features" :key="feature.id">
        {{ feature.name }}
      </li>
    </ul>
  </div>
</template>
```

---

## 📋 Form Handling with VeeValidate

```typescript
<template>
  <Form @submit="onSubmit" class="form">
    <div class="form-group">
      <label for="email">Email</label>
      <Field
        id="email"
        type="email"
        name="email"
        v-slot="{ field, meta }"
        rules="required|email"
      >
        <input
          v-bind="field"
          :class="{ 'is-invalid': meta.touched && meta.invalid }"
        />
      </Field>
      <ErrorMessage name="email" />
    </div>

    <div class="form-group">
      <label for="password">Password</label>
      <Field
        id="password"
        type="password"
        name="password"
        v-slot="{ field, meta }"
        rules="required|min:8"
      >
        <input
          v-bind="field"
          :class="{ 'is-invalid': meta.touched && meta.invalid }"
        />
      </Field>
      <ErrorMessage name="password" />
    </div>

    <button type="submit">Login</button>
  </Form>
</template>

<script setup lang="ts">
import { Form, Field, ErrorMessage } from 'vee-validate';
import * as yup from 'yup';

const validationSchema = yup.object({
  email: yup.string().email().required(),
  password: yup.string().min(8).required(),
});

const onSubmit = async (values: any) => {
  console.log('Form submitted:', values);
};
</script>
```

---

## 🎨 Component Transitions

```typescript
<template>
  <div>
    <TransitionGroup name="list" tag="ul">
      <li v-for="feature in features" :key="feature.id">
        {{ feature.name }}
      </li>
    </TransitionGroup>

    <Transition name="fade">
      <div v-if="showModal" class="modal">
        <p>Modal content</p>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const features = ref([]);
const showModal = ref(false);
</script>

<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
```

---

## 🔄 Router Patterns

```typescript
// router.ts
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/features',
    component: () => import('@/views/Features.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/features/:id',
    component: () => import('@/views/FeatureDetail.vue'),
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    next('/login');
  } else {
    next();
  }
});

export default router;

// Usage in component
<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const goToFeature = (id: string) => {
  router.push({ name: 'FeatureDetail', params: { id } });
};

const featureId = computed(() => route.params.id);
</script>
```

---

## 📚 Related Documents

- React Patterns (react_patterns.md)
- State Management (state_management.md)
- Performance (performance.md)

---

**END OF VUE.JS PATTERNS DOCUMENT**
