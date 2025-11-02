# Backend-Frontend Integration Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Backend-Frontend Integration Guide
**Focus:** 150+ integration techniques

---

## 🤝 Communication Patterns

### Request-Response Pattern

```typescript
// Backend (Express)
app.post('/api/features', async (req, res) => {
  try {
    const feature = await Feature.create(req.body);
    res.status(201).json({
      success: true,
      data: feature,
      timestamp: new Date()
    });
  } catch (error) {
    res.status(400).json({
      success: false,
      error: error.message,
      code: 'VALIDATION_ERROR'
    });
  }
});

// Frontend (React)
async function createFeature(data: FeatureCreate) {
  const response = await fetch('/api/features', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  const result = await response.json();

  if (!response.ok) {
    throw new Error(result.error || 'Failed to create feature');
  }

  return result.data;
}
```

### Event-Driven Pattern

```typescript
// Backend event emitter
class FeatureEventBus {
  private emitter = new EventEmitter();

  onFeatureCreated(handler: (feature: Feature) => void) {
    this.emitter.on('feature:created', handler);
  }

  emitFeatureCreated(feature: Feature) {
    this.emitter.emit('feature:created', feature);
    
    // Publish to message queue
    messageQueue.publish('feature.created', feature);
    
    // Update WebSocket clients
    io.emit('feature:created', feature);
  }
}

// Frontend listener
const eventBus = new EventSource('/api/events');

eventBus.addEventListener('feature:created', (event) => {
  const feature = JSON.parse(event.data);
  updateFeatureList(feature);
});
```

### Polling Pattern

```typescript
// Frontend poll
class APIPoller {
  private intervalId: NodeJS.Timeout | null = null;

  startPolling(
    endpoint: string,
    callback: (data: any) => void,
    interval: number = 5000
  ) {
    this.intervalId = setInterval(async () => {
      try {
        const response = await fetch(endpoint);
        const data = await response.json();
        callback(data);
      } catch (error) {
        console.error('Polling error:', error);
      }
    }, interval);
  }

  stopPolling() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  }
}

// Exponential backoff polling
async function pollWithBackoff(
  endpoint: string,
  condition: (data: any) => boolean,
  maxWait: number = 30000
) {
  let attempt = 0;
  const startTime = Date.now();

  while (Date.now() - startTime < maxWait) {
    const response = await fetch(endpoint);
    const data = await response.json();

    if (condition(data)) {
      return data;
    }

    const delay = Math.min(1000 * Math.pow(2, attempt++), 5000);
    await new Promise(resolve => setTimeout(resolve, delay));
  }

  throw new Error('Polling timeout');
}
```

---

## 📦 Data Transfer

### Data Serialization

```typescript
// JSON serialization
const feature = {
  id: '1',
  createdAt: new Date(),
  metadata: new Map([['key', 'value']])
};

// Custom serializer
class Serializer {
  static serialize(obj: any): string {
    return JSON.stringify(obj, (key, value) => {
      if (value instanceof Date) {
        return { __type: 'Date', value: value.toISOString() };
      }
      if (value instanceof Map) {
        return { __type: 'Map', value: Array.from(value.entries()) };
      }
      return value;
    });
  }

  static deserialize(json: string): any {
    return JSON.parse(json, (key, value) => {
      if (value?.__type === 'Date') {
        return new Date(value.value);
      }
      if (value?.__type === 'Map') {
        return new Map(value.value);
      }
      return value;
    });
  }
}

// MessagePack (binary serialization)
import msgpack from 'msgpack-lite';

const buffer = msgpack.encode(feature);
const deserialized = msgpack.decode(buffer);
```

### Large File Transfer

```typescript
// Backend file upload handler
const multer = require('multer');
const upload = multer({
  dest: '/uploads',
  limits: { fileSize: 100 * 1024 * 1024 }, // 100MB
  fileFilter: (req, file, cb) => {
    if (!['image/jpeg', 'application/pdf'].includes(file.mimetype)) {
      return cb(new Error('Invalid file type'));
    }
    cb(null, true);
  }
});

app.post('/api/uploads', upload.single('file'), (req, res) => {
  res.json({ url: `/uploads/${req.file.filename}` });
});

// Frontend chunked upload
class ChunkedUploader {
  private chunkSize = 5 * 1024 * 1024; // 5MB chunks

  async upload(file: File, endpoint: string): Promise<string> {
    const totalChunks = Math.ceil(file.size / this.chunkSize);
    const uploadId = generateUUID();

    for (let i = 0; i < totalChunks; i++) {
      const start = i * this.chunkSize;
      const end = Math.min(start + this.chunkSize, file.size);
      const chunk = file.slice(start, end);

      const formData = new FormData();
      formData.append('uploadId', uploadId);
      formData.append('chunkIndex', i.toString());
      formData.append('totalChunks', totalChunks.toString());
      formData.append('chunk', chunk);

      await fetch(endpoint, {
        method: 'POST',
        body: formData
      });
    }

    // Notify completion
    const response = await fetch(`${endpoint}/complete`, {
      method: 'POST',
      body: JSON.stringify({ uploadId })
    });

    return (await response.json()).url;
  }
}
```

---

## 🔄 Sync Patterns

### Optimistic Updates

```typescript
// Frontend optimistic update
async function updateFeature(id: string, updates: any) {
  // Update UI immediately
  const oldFeature = getFeature(id);
  const newFeature = { ...oldFeature, ...updates };
  setFeature(id, newFeature);

  try {
    // Send to backend
    const response = await fetch(`/api/features/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(updates)
    });

    if (!response.ok) {
      // Revert on error
      setFeature(id, oldFeature);
      throw new Error('Update failed');
    }

    const confirmed = await response.json();
    setFeature(id, confirmed);
  } catch (error) {
    // Revert and show error
    setFeature(id, oldFeature);
    showError(error.message);
  }
}
```

### Conflict Resolution

```typescript
// Last-write-wins
interface VersionedFeature {
  id: string;
  version: number;
  data: Feature;
}

async function updateWithConflictDetection(
  feature: VersionedFeature
): Promise<VersionedFeature> {
  const response = await fetch(`/api/features/${feature.id}`, {
    method: 'PATCH',
    headers: { 'If-Match': feature.version.toString() },
    body: JSON.stringify(feature.data)
  });

  if (response.status === 409) {
    // Conflict - fetch latest version
    const latest = await fetch(`/api/features/${feature.id}`).then(r => r.json());
    throw new ConflictError('Feature was modified', latest);
  }

  return response.json();
}

// Operational Transform (for collaborative editing)
type Operation = { type: 'insert' | 'delete', position: number, content?: string };

function applyOperation(text: string, op: Operation): string {
  switch (op.type) {
    case 'insert':
      return text.slice(0, op.position) + op.content + text.slice(op.position);
    case 'delete':
      return text.slice(0, op.position) + text.slice(op.position + 1);
  }
}

function transformOperations(op1: Operation, op2: Operation): Operation {
  if (op1.type === 'insert' && op2.type === 'insert') {
    if (op1.position < op2.position) return op1;
    if (op1.position > op2.position) {
      return { ...op1, position: op1.position + op2.content!.length };
    }
    return op1; // Same position, keep as is
  }
  return op2;
}
```

---

## 🔐 Secure Communication

### CSRF Protection

```typescript
// Backend CSRF token
app.post('/api/features', (req, res, next) => {
  const csrfToken = req.headers['x-csrf-token'];
  const sessionToken = req.session.csrfToken;

  if (csrfToken !== sessionToken) {
    return res.status(403).json({ error: 'Invalid CSRF token' });
  }

  next();
});

// Frontend CSRF token
async function createFeature(data: any) {
  const response = await fetch('/api/features', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-Token': getCsrfToken()
    },
    body: JSON.stringify(data)
  });

  return response.json();
}
```

### Data Encryption

```typescript
// Client-side encryption (before sending)
import { encrypt, decrypt } from 'tweetnacl-util';
import { secretbox } from 'tweetnacl';

async function encryptSensitiveData(data: any, publicKey: string) {
  const encrypted = secretbox.after(
    Buffer.from(JSON.stringify(data)),
    Buffer.from(publicKey, 'base64')
  );

  return encrypted.toString('base64');
}

// Server-side decryption
app.post('/api/sensitive', express.json(), (req, res) => {
  try {
    const decrypted = secretbox.open(
      Buffer.from(req.body.encrypted, 'base64'),
      Buffer.from(process.env.PRIVATE_KEY, 'base64')
    );

    const data = JSON.parse(Buffer.from(decrypted).toString());
    res.json({ success: true });
  } catch (error) {
    res.status(400).json({ error: 'Decryption failed' });
  }
});
```

---

## 📊 State Synchronization

### State Sync Manager

```typescript
class StateSyncManager {
  private pendingChanges: Map<string, any> = new Map();
  private syncInterval: NodeJS.Timeout | null = null;

  async addChange(key: string, value: any) {
    this.pendingChanges.set(key, value);
    
    // Debounced sync
    if (!this.syncInterval) {
      this.syncInterval = setTimeout(() => this.sync(), 1000);
    }
  }

  private async sync() {
    if (this.pendingChanges.size === 0) return;

    const changes = Object.fromEntries(this.pendingChanges);

    try {
      const response = await fetch('/api/state/sync', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(changes)
      });

      if (!response.ok) throw new Error('Sync failed');

      this.pendingChanges.clear();
    } catch (error) {
      console.error('Sync error:', error);
      // Retry on next interval
    }

    this.syncInterval = null;
  }
}
```

---

## 🔌 API Versioning

### Version Management

```typescript
// URL-based versioning
app.get('/api/v1/features', (req, res) => {
  // V1 implementation
});

app.get('/api/v2/features', (req, res) => {
  // V2 implementation
});

// Header-based versioning
app.get('/api/features', (req, res) => {
  const version = req.headers['api-version'] || '1';
  
  if (version === '2') {
    return res.json({ features: [], format: 'v2' });
  }
  
  return res.json({ data: { features: [] } });
});

// Accept header
app.get('/api/features', (req, res) => {
  const accept = req.headers.accept;
  
  if (accept.includes('application/vnd.api+json;version=2')) {
    return res.json({ /* v2 */ });
  }
  
  return res.json({ /* v1 */ });
});

// Frontend version handling
const API_VERSION = '2';

async function fetchFeatures() {
  const response = await fetch('/api/features', {
    headers: { 'API-Version': API_VERSION }
  });

  const data = await response.json();
  return normalizeResponse(data, API_VERSION);
}

function normalizeResponse(data: any, version: string) {
  if (version === '1') {
    return { features: data.data.features };
  }
  return data;
}
```

---

## 📈 Monitoring & Logging

### Request Logging

```typescript
// Backend request logger
class RequestLogger {
  logRequest(req: express.Request, res: express.Response) {
    const start = Date.now();

    res.on('finish', () => {
      const duration = Date.now() - start;

      console.log(JSON.stringify({
        timestamp: new Date().toISOString(),
        method: req.method,
        path: req.path,
        status: res.statusCode,
        duration,
        userId: req.user?.id,
        userAgent: req.get('user-agent')
      }));
    });
  }
}

// Frontend request logging
class ClientLogger {
  async logRequest(method: string, url: string, response: Response) {
    const duration = performance.now();

    await fetch('/api/logs', {
      method: 'POST',
      body: JSON.stringify({
        timestamp: new Date().toISOString(),
        method,
        url,
        status: response.status,
        duration
      })
    });
  }
}
```

---

## 📚 Related Documents

- API Integration (api_integration.md)
- Database Integration (database_integration.md)
- Real-time Communication (real_time_communication.md)

---

**END OF BACKEND-FRONTEND INTEGRATION DOCUMENT**
