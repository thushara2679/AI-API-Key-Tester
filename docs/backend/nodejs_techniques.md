# Node.js Techniques Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Last Updated:** October 26, 2024
**Document Type:** Node.js Implementation Guide
**Node Version:** 18+
**Focus:** Production-grade Node.js techniques for web services

---

## 📖 Introduction

This document provides comprehensive Node.js techniques, patterns, and best practices for implementing frontend services, APIs, and backend workers in the AI Agent System.

---

## 🚀 Express.js & Async/Await Patterns

### Express Setup with Async Error Handling

```javascript
// app.js
const express = require('express');
const compression = require('compression');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');

const app = express();

// Middleware
app.use(helmet()); // Security headers
app.use(cors()); // CORS
app.use(compression()); // Gzip compression
app.use(express.json({ limit: '10mb' }));
app.use(morgan('combined')); // Logging

// ✅ GOOD: Async route handler with error handling
app.get('/api/features/:featureId', asyncHandler(async (req, res) => {
  const { featureId } = req.params;
  
  // Query database
  const feature = await Feature.findById(featureId);
  
  if (!feature) {
    return res.status(404).json({ error: 'Feature not found' });
  }
  
  res.json(feature);
}));

// Async handler wrapper to catch errors
function asyncHandler(fn) {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
}

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err);
  
  if (err instanceof ValidationError) {
    return res.status(400).json({
      error: 'Validation error',
      details: err.details
    });
  }
  
  if (err instanceof NotFoundError) {
    return res.status(404).json({ error: 'Not found' });
  }
  
  res.status(500).json({ error: 'Internal server error' });
});

// ❌ WRONG: Not handling async errors
app.get('/api/bad', (req, res) => {
  // If this throws, it won't be caught!
  const feature = await Feature.findById(req.params.id);
  res.json(feature);
});
```

### Connection Pooling

```javascript
// db.js
const { Pool } = require('pg');

const pool = new Pool({
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,              // Pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

pool.on('error', (err) => {
  console.error('Unexpected error on idle client', err);
});

async function query(text, params) {
  const start = Date.now();
  try {
    const res = await pool.query(text, params);
    const duration = Date.now() - start;
    logger.info('Query executed', { text, duration, rows: res.rowCount });
    return res;
  } catch (error) {
    logger.error('Query error', { text, error });
    throw error;
  }
}

module.exports = { pool, query };
```

---

## 🔌 TypeScript with Node.js

### TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noUnusedLocals": true,
    "noImplicitReturns": true
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

### Type-Safe Express App

```typescript
// src/app.ts
import express, { Request, Response, NextFunction } from 'express';
import { Database } from './database';
import { Logger } from './logger';

interface AuthenticatedRequest extends Request {
  user: {
    id: string;
    email: string;
    role: 'admin' | 'developer' | 'viewer';
  };
}

class FeatureController {
  constructor(private db: Database, private logger: Logger) {}
  
  async getFeature(req: AuthenticatedRequest, res: Response): Promise<void> {
    try {
      const { featureId } = req.params;
      
      // Type-safe query
      const feature = await this.db.features.findById(featureId);
      
      if (!feature) {
        res.status(404).json({ error: 'Feature not found' });
        return;
      }
      
      // Check authorization
      if (!this.canViewFeature(req.user, feature)) {
        res.status(403).json({ error: 'Forbidden' });
        return;
      }
      
      res.json(feature);
    } catch (error) {
      this.logger.error('Error fetching feature', { error });
      res.status(500).json({ error: 'Internal server error' });
    }
  }
  
  private canViewFeature(user: AuthenticatedRequest['user'], feature: any): boolean {
    return user.role === 'admin' || feature.ownerId === user.id;
  }
}

// Router setup
export function setupRoutes(app: express.Application, db: Database, logger: Logger) {
  const controller = new FeatureController(db, logger);
  
  app.get('/api/features/:featureId', (req: AuthenticatedRequest, res: Response) => {
    controller.getFeature(req, res).catch((error) => {
      logger.error('Unhandled error', { error });
      res.status(500).json({ error: 'Internal server error' });
    });
  });
}
```

---

## 🎨 React Best Practices

### Component Structure

```typescript
// src/components/FeatureForm.tsx
import React, { useState, useCallback } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';

interface FeatureFormProps {
  featureId?: string;
  onSuccess: () => void;
  onError: (error: Error) => void;
}

export const FeatureForm: React.FC<FeatureFormProps> = ({
  featureId,
  onSuccess,
  onError
}) => {
  const [formData, setFormData] = useState({
    name: '',
    complexity: 5,
    description: ''
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  
  // Fetch existing feature if editing
  const { data: feature, isLoading } = useQuery({
    queryKey: ['features', featureId],
    queryFn: () => featureId ? fetchFeature(featureId) : null,
    enabled: !!featureId
  });
  
  // Create/update mutation
  const { mutate, isPending } = useMutation({
    mutationFn: (data) => 
      featureId 
        ? updateFeature(featureId, data)
        : createFeature(data),
    onSuccess: () => {
      onSuccess();
    },
    onError: (error) => {
      onError(error);
    }
  });
  
  // Form submission
  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    const newErrors = validateForm(formData);
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    // Mutation
    mutate(formData);
  }, [formData, mutate]);
  
  // Input change handler
  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'complexity' ? parseInt(value) : value
    }));
    
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  }, [errors]);
  
  if (isLoading) return <div>Loading...</div>;
  
  return (
    <form onSubmit={handleSubmit} className="feature-form">
      <div className="form-group">
        <label htmlFor="name">Feature Name</label>
        <input
          id="name"
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          className={errors.name ? 'error' : ''}
        />
        {errors.name && <span className="error-message">{errors.name}</span>}
      </div>
      
      <div className="form-group">
        <label htmlFor="complexity">Complexity Points</label>
        <input
          id="complexity"
          type="range"
          name="complexity"
          min="1"
          max="13"
          value={formData.complexity}
          onChange={handleChange}
        />
        <span>{formData.complexity}</span>
      </div>
      
      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange as any}
        />
      </div>
      
      <button type="submit" disabled={isPending}>
        {isPending ? 'Saving...' : 'Save Feature'}
      </button>
    </form>
  );
};

// Validation
function validateForm(data: any): Record<string, string> {
  const errors: Record<string, string> = {};
  
  if (!data.name || data.name.length < 2) {
    errors.name = 'Name must be at least 2 characters';
  }
  
  if (!data.complexity || data.complexity < 1 || data.complexity > 13) {
    errors.complexity = 'Complexity must be between 1 and 13';
  }
  
  if (!data.description || data.description.length < 10) {
    errors.description = 'Description must be at least 10 characters';
  }
  
  return errors;
}

// API functions
async function fetchFeature(id: string) {
  const response = await fetch(`/api/features/${id}`);
  if (!response.ok) throw new Error('Failed to fetch feature');
  return response.json();
}

async function createFeature(data: any) {
  const response = await fetch('/api/features', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!response.ok) throw new Error('Failed to create feature');
  return response.json();
}

async function updateFeature(id: string, data: any) {
  const response = await fetch(`/api/features/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!response.ok) throw new Error('Failed to update feature');
  return response.json();
}
```

### State Management with Zustand

```typescript
// src/store/featureStore.ts
import { create } from 'zustand';

interface Feature {
  id: string;
  name: string;
  complexity: number;
  status: 'not_started' | 'in_progress' | 'completed';
}

interface FeatureStore {
  features: Feature[];
  selectedFeature: Feature | null;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setFeatures: (features: Feature[]) => void;
  selectFeature: (feature: Feature | null) => void;
  addFeature: (feature: Feature) => void;
  updateFeature: (id: string, updates: Partial<Feature>) => void;
  removeFeature: (id: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useFeatureStore = create<FeatureStore>((set) => ({
  features: [],
  selectedFeature: null,
  isLoading: false,
  error: null,
  
  setFeatures: (features) => set({ features }),
  
  selectFeature: (feature) => set({ selectedFeature: feature }),
  
  addFeature: (feature) => set((state) => ({
    features: [...state.features, feature]
  })),
  
  updateFeature: (id, updates) => set((state) => ({
    features: state.features.map(f => 
      f.id === id ? { ...f, ...updates } : f
    ),
    selectedFeature: state.selectedFeature?.id === id 
      ? { ...state.selectedFeature, ...updates }
      : state.selectedFeature
  })),
  
  removeFeature: (id) => set((state) => ({
    features: state.features.filter(f => f.id !== id),
    selectedFeature: state.selectedFeature?.id === id ? null : state.selectedFeature
  })),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  setError: (error) => set({ error })
}));

// Usage
export function FeatureList() {
  const { features, selectedFeature, selectFeature } = useFeatureStore();
  
  return (
    <ul>
      {features.map(feature => (
        <li
          key={feature.id}
          onClick={() => selectFeature(feature)}
          className={selectedFeature?.id === feature.id ? 'selected' : ''}
        >
          {feature.name} (CP: {feature.complexity})
        </li>
      ))}
    </ul>
  );
}
```

---

## 🧪 Testing with Jest

### Unit Testing

```typescript
// src/__tests__/features.test.ts
import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { FeatureService } from '../services/FeatureService';
import { Database } from '../database';

describe('FeatureService', () => {
  let service: FeatureService;
  let mockDb: jest.Mocked<Database>;
  
  beforeEach(() => {
    mockDb = {
      features: {
        findById: jest.fn(),
        create: jest.fn(),
        update: jest.fn(),
        delete: jest.fn()
      }
    } as any;
    
    service = new FeatureService(mockDb);
  });
  
  it('should fetch feature by id', async () => {
    const mockFeature = { id: 'feat-1', name: 'OAuth' };
    mockDb.features.findById.mockResolvedValue(mockFeature);
    
    const result = await service.getFeature('feat-1');
    
    expect(result).toEqual(mockFeature);
    expect(mockDb.features.findById).toHaveBeenCalledWith('feat-1');
  });
  
  it('should create feature', async () => {
    const newFeature = { name: 'OAuth', complexity: 8 };
    const created = { id: 'feat-1', ...newFeature };
    mockDb.features.create.mockResolvedValue(created);
    
    const result = await service.createFeature(newFeature);
    
    expect(result.id).toBeDefined();
    expect(result.name).toBe('OAuth');
    expect(mockDb.features.create).toHaveBeenCalledWith(newFeature);
  });
  
  it('should throw on invalid complexity', async () => {
    const invalid = { name: 'Test', complexity: 20 };
    
    await expect(service.createFeature(invalid)).rejects.toThrow();
  });
});
```

### Integration Testing

```typescript
// src/__tests__/integration/features.integration.test.ts
import request from 'supertest';
import { app } from '../../app';
import { Database } from '../../database';

describe('Features API Integration', () => {
  let db: Database;
  
  beforeAll(async () => {
    db = new Database();
    await db.connect();
  });
  
  afterAll(async () => {
    await db.disconnect();
  });
  
  afterEach(async () => {
    // Clear database
    await db.features.deleteMany({});
  });
  
  it('POST /api/features should create feature', async () => {
    const response = await request(app)
      .post('/api/features')
      .send({
        name: 'OAuth Integration',
        complexity: 8,
        description: 'Implement OAuth 2.0'
      });
    
    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty('id');
    expect(response.body.name).toBe('OAuth Integration');
  });
  
  it('GET /api/features/:id should return feature', async () => {
    // Create feature
    const feature = await db.features.create({
      name: 'Test Feature',
      complexity: 5
    });
    
    // Get feature
    const response = await request(app)
      .get(`/api/features/${feature.id}`);
    
    expect(response.status).toBe(200);
    expect(response.body.id).toBe(feature.id);
  });
});
```

---

## 📦 Performance Optimization

### Caching Strategy

```typescript
// src/cache.ts
import Redis from 'ioredis';

const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  lazyConnect: true,
  enableReadyCheck: false,
  enableOfflineQueue: false,
  maxRetriesPerRequest: 1,
  retryStrategy: (times) => Math.min(times * 50, 2000)
});

export async function cacheGet<T>(key: string): Promise<T | null> {
  try {
    const value = await redis.get(key);
    return value ? JSON.parse(value) : null;
  } catch (error) {
    console.error(`Cache get error for key ${key}:`, error);
    return null;
  }
}

export async function cacheSet<T>(
  key: string,
  value: T,
  ttl: number = 3600
): Promise<void> {
  try {
    await redis.setex(key, ttl, JSON.stringify(value));
  } catch (error) {
    console.error(`Cache set error for key ${key}:`, error);
  }
}

export async function cacheDel(key: string): Promise<void> {
  try {
    await redis.del(key);
  } catch (error) {
    console.error(`Cache delete error for key ${key}:`, error);
  }
}

// Decorator for caching
export function Cacheable(ttl: number = 3600) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    
    descriptor.value = async function (...args: any[]) {
      const cacheKey = `${target.constructor.name}:${propertyKey}:${JSON.stringify(args)}`;
      
      // Try cache
      const cached = await cacheGet(cacheKey);
      if (cached) return cached;
      
      // Execute method
      const result = await originalMethod.apply(this, args);
      
      // Cache result
      await cacheSet(cacheKey, result, ttl);
      
      return result;
    };
    
    return descriptor;
  };
}

// Usage
class FeatureService {
  @Cacheable(3600)
  async getFeature(featureId: string) {
    return await db.features.findById(featureId);
  }
}
```

### Lazy Loading & Code Splitting

```typescript
// src/routes.tsx
import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';

// Lazy load components
const Features = lazy(() => import('./pages/Features'));
const Deployments = lazy(() => import('./pages/Deployments'));
const Admin = lazy(() => import('./pages/Admin'));

export function AppRoutes() {
  return (
    <Routes>
      <Route
        path="/features"
        element={
          <Suspense fallback={<LoadingSpinner />}>
            <Features />
          </Suspense>
        }
      />
      <Route
        path="/deployments"
        element={
          <Suspense fallback={<LoadingSpinner />}>
            <Deployments />
          </Suspense>
        }
      />
      <Route
        path="/admin"
        element={
          <Suspense fallback={<LoadingSpinner />}>
            <Admin />
          </Suspense>
        }
      />
    </Routes>
  );
}
```

---

## 🔒 Security Best Practices

### Authentication & Authorization

```typescript
// src/middleware/auth.ts
import jwt from 'jsonwebtoken';
import { Request, Response, NextFunction } from 'express';

interface AuthPayload {
  sub: string;
  email: string;
  role: 'admin' | 'developer' | 'viewer';
}

declare global {
  namespace Express {
    interface Request {
      user: AuthPayload;
    }
  }
}

export function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({ error: 'Missing token' });
  }
  
  try {
    const payload = jwt.verify(
      token,
      process.env.JWT_SECRET!
    ) as AuthPayload;
    
    req.user = payload;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}

// Role-based access control
export function authorize(...roles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

// Usage
app.delete(
  '/api/features/:id',
  authMiddleware,
  authorize('admin'),
  asyncHandler(deleteFeature)
);
```

### Input Validation

```typescript
// src/middleware/validation.ts
import { body, validationResult } from 'express-validator';
import { Request, Response, NextFunction } from 'express';

export function validateFeatureCreate() {
  return [
    body('name')
      .trim()
      .isLength({ min: 2, max: 255 })
      .withMessage('Name must be 2-255 characters'),
    body('complexity')
      .isInt({ min: 1, max: 13 })
      .withMessage('Complexity must be 1-13'),
    body('description')
      .trim()
      .isLength({ min: 10, max: 2000 })
      .withMessage('Description must be 10-2000 characters'),
    validateInput
  ];
}

function validateInput(req: Request, res: Response, next: NextFunction) {
  const errors = validationResult(req);
  
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  
  next();
}

// Usage
app.post(
  '/api/features',
  validateFeatureCreate(),
  asyncHandler(createFeature)
);
```

---

## 📚 Related Documents

- API Design (api_design.md)
- React Components & Patterns
- Performance Optimization (performance_optimization.md)

---

## 📝 Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Oct 26, 2024 | Node.js Team | Initial version |

---

**END OF NODE.JS TECHNIQUES DOCUMENT**
