# Integration Testing Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Integration Testing Guide
**Focus:** 50+ integration testing techniques

---

## 🔗 Integration Testing Fundamentals

### Testing API Endpoints

```typescript
// Using Supertest
import request from 'supertest';
import { app } from '../app';

describe('Feature API - Integration', () => {
  describe('POST /api/features', () => {
    it('should create feature', async () => {
      const response = await request(app)
        .post('/api/features')
        .set('Authorization', 'Bearer token')
        .send({
          name: 'OAuth',
          priority: 10,
          description: 'OAuth authentication'
        })
        .expect(201);
      
      expect(response.body).toHaveProperty('id');
      expect(response.body.name).toBe('OAuth');
    });
    
    it('should return 400 for invalid data', async () => {
      await request(app)
        .post('/api/features')
        .send({ name: '' })
        .expect(400);
    });
    
    it('should return 401 without token', async () => {
      await request(app)
        .post('/api/features')
        .send({ name: 'OAuth' })
        .expect(401);
    });
  });
  
  describe('GET /api/features/:id', () => {
    it('should fetch feature', async () => {
      const createRes = await request(app)
        .post('/api/features')
        .set('Authorization', 'Bearer token')
        .send({ name: 'OAuth', priority: 10 });
      
      const featureId = createRes.body.id;
      
      const getRes = await request(app)
        .get(`/api/features/${featureId}`)
        .expect(200);
      
      expect(getRes.body.name).toBe('OAuth');
    });
    
    it('should return 404 for non-existent feature', async () => {
      await request(app)
        .get('/api/features/invalid-id')
        .expect(404);
    });
  });
});
```

### Database Integration

```typescript
// Testing with real database
import { DatabaseClient } from '../database';

describe('Feature Repository - Database Integration', () => {
  let db: DatabaseClient;
  
  beforeAll(async () => {
    db = new DatabaseClient(process.env.TEST_DB_URL);
    await db.connect();
    await db.migrate();
  });
  
  beforeEach(async () => {
    await db.clearTables(['features', 'audit_logs']);
  });
  
  afterAll(async () => {
    await db.disconnect();
  });
  
  it('should save and retrieve feature', async () => {
    const feature = { name: 'OAuth', priority: 10 };
    const saved = await db.features.save(feature);
    
    const retrieved = await db.features.findById(saved.id);
    
    expect(retrieved.name).toBe('OAuth');
    expect(retrieved.id).toBe(saved.id);
  });
  
  it('should cascade delete related records', async () => {
    const feature = await db.features.save({ name: 'OAuth', priority: 10 });
    await db.tests.save({ featureId: feature.id, name: 'test1' });
    
    await db.features.delete(feature.id);
    
    const tests = await db.tests.findByFeatureId(feature.id);
    expect(tests).toHaveLength(0);
  });
  
  it('should maintain referential integrity', async () => {
    expect(async () => {
      await db.tests.save({ featureId: 'invalid-id', name: 'test1' });
    }).rejects.toThrow();
  });
});
```

---

## 🔄 Service Integration Tests

### Microservices Communication

```typescript
// Testing service-to-service calls
describe('Feature Service Integration', () => {
  let featureService: FeatureService;
  let deploymentService: DeploymentService;
  
  beforeEach(() => {
    featureService = new FeatureService(mockDb);
    deploymentService = new DeploymentService(mockDb);
  });
  
  it('should notify deployment service when feature created', async () => {
    const notifySpy = jest.spyOn(deploymentService, 'notifyFeatureCreated');
    
    const feature = await featureService.createFeature(
      { name: 'OAuth', priority: 10 },
      deploymentService
    );
    
    expect(notifySpy).toHaveBeenCalledWith(feature.id);
  });
  
  it('should handle service timeout', async () => {
    jest.spyOn(deploymentService, 'notifyFeatureCreated')
      .mockImplementation(() => 
        new Promise(resolve => setTimeout(resolve, 10000))
      );
    
    const promise = featureService.createFeature(
      { name: 'OAuth', priority: 10 },
      deploymentService
    );
    
    jest.advanceTimersByTime(5000);
    
    await expect(promise).rejects.toThrow('Timeout');
  });
});
```

### External API Integration

```typescript
// Testing with external APIs
describe('External API Integration', () => {
  let httpClient: HttpClient;
  
  beforeAll(() => {
    httpClient = new HttpClient({
      baseURL: process.env.API_URL,
      timeout: 5000
    });
  });
  
  it('should fetch data from external API', async () => {
    const data = await httpClient.get('/data');
    
    expect(data).toBeDefined();
    expect(data).toHaveProperty('results');
  });
  
  it('should handle API errors', async () => {
    await expect(
      httpClient.get('/invalid-endpoint')
    ).rejects.toThrow('404');
  });
  
  it('should retry on network failure', async () => {
    let attempts = 0;
    jest.spyOn(httpClient, 'get')
      .mockImplementation(async () => {
        attempts++;
        if (attempts < 3) throw new Error('Network error');
        return { success: true };
      });
    
    const result = await httpClient.get('/data');
    expect(attempts).toBe(3);
    expect(result.success).toBe(true);
  });
});
```

---

## 📨 Message Queue Integration

```typescript
// Testing message queue
describe('Message Queue Integration', () => {
  let messageQueue: MessageQueue;
  let consumer: MessageConsumer;
  
  beforeEach(async () => {
    messageQueue = new MessageQueue(process.env.KAFKA_BROKERS);
    await messageQueue.connect();
  });
  
  afterEach(async () => {
    await messageQueue.disconnect();
  });
  
  it('should publish and consume messages', async () => {
    const receivedMessages: any[] = [];
    
    consumer = await messageQueue.createConsumer('features-group');
    consumer.on('message', (msg) => {
      receivedMessages.push(JSON.parse(msg.value));
    });
    
    await messageQueue.publish('features', {
      event: 'feature.created',
      data: { id: '1', name: 'OAuth' }
    });
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    expect(receivedMessages).toHaveLength(1);
    expect(receivedMessages[0].event).toBe('feature.created');
  });
  
  it('should handle dead letter queue', async () => {
    const dlqConsumer = await messageQueue.createConsumer('dlq-group');
    const dlqMessages: any[] = [];
    
    dlqConsumer.on('message', (msg) => {
      dlqMessages.push(msg);
    });
    
    // Send message that will fail
    await messageQueue.publish('features', {
      event: 'invalid.event',
      data: null
    });
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    expect(dlqMessages.length).toBeGreaterThan(0);
  });
});
```

---

## 📊 Data Integration

### Database Transactions

```typescript
describe('Database Transactions', () => {
  let db: Database;
  
  beforeEach(async () => {
    db = new Database();
    await db.connect();
  });
  
  it('should rollback on error', async () => {
    try {
      await db.transaction(async (tx) => {
        await tx.features.save({ name: 'OAuth', priority: 10 });
        throw new Error('Something went wrong');
      });
    } catch (e) {
      // Expected
    }
    
    const features = await db.features.findAll();
    expect(features).toHaveLength(0);
  });
  
  it('should commit successfully', async () => {
    await db.transaction(async (tx) => {
      await tx.features.save({ name: 'OAuth', priority: 10 });
      await tx.features.save({ name: 'API', priority: 9 });
    });
    
    const features = await db.features.findAll();
    expect(features).toHaveLength(2);
  });
});
```

### Cache Integration

```typescript
describe('Cache Integration', () => {
  let cache: CacheClient;
  let db: Database;
  
  beforeEach(async () => {
    cache = new CacheClient();
    db = new Database();
  });
  
  it('should cache database queries', async () => {
    const spy = jest.spyOn(db, 'query');
    
    // First call hits database
    const result1 = await getFeatureWithCache(cache, db, '1');
    expect(spy).toHaveBeenCalledTimes(1);
    
    // Second call uses cache
    const result2 = await getFeatureWithCache(cache, db, '1');
    expect(spy).toHaveBeenCalledTimes(1);
    
    expect(result1).toEqual(result2);
  });
  
  it('should invalidate cache on update', async () => {
    const feature = await getFeatureWithCache(cache, db, '1');
    
    await db.features.update('1', { name: 'OAuth2' });
    await cache.invalidate('feature:1');
    
    const updated = await getFeatureWithCache(cache, db, '1');
    expect(updated.name).toBe('OAuth2');
  });
});
```

---

## 🔐 Auth Integration

```typescript
describe('Authentication Integration', () => {
  let app: Express.Application;
  let authService: AuthService;
  
  beforeEach(() => {
    app = createApp();
    authService = new AuthService();
  });
  
  it('should authenticate with token', async () => {
    const token = await authService.generateToken({ userId: '1' });
    
    const response = await request(app)
      .get('/api/profile')
      .set('Authorization', `Bearer ${token}`)
      .expect(200);
    
    expect(response.body.userId).toBe('1');
  });
  
  it('should reject expired token', async () => {
    const token = await authService.generateToken(
      { userId: '1' },
      { expiresIn: '-1h' }
    );
    
    await request(app)
      .get('/api/profile')
      .set('Authorization', `Bearer ${token}`)
      .expect(401);
  });
  
  it('should handle refresh token flow', async () => {
    const { accessToken, refreshToken } = await authService.login(
      'user@example.com',
      'password'
    );
    
    const newAccessToken = await authService.refreshToken(refreshToken);
    
    const response = await request(app)
      .get('/api/profile')
      .set('Authorization', `Bearer ${newAccessToken}`)
      .expect(200);
    
    expect(response.body).toBeDefined();
  });
});
```

---

## 🎯 Workflow Integration

```typescript
describe('Feature Workflow Integration', () => {
  let workflow: FeatureWorkflow;
  let db: Database;
  let messageQueue: MessageQueue;
  
  beforeEach(async () => {
    db = new Database();
    messageQueue = new MessageQueue();
    workflow = new FeatureWorkflow(db, messageQueue);
  });
  
  it('should complete full feature lifecycle', async () => {
    // Create
    const feature = await workflow.createFeature({
      name: 'OAuth',
      priority: 10
    });
    expect(feature.status).toBe('created');
    
    // Assign
    await workflow.assignFeature(feature.id, 'developer-1');
    let updated = await db.features.findById(feature.id);
    expect(updated.status).toBe('assigned');
    
    // Complete
    await workflow.completeFeature(feature.id);
    updated = await db.features.findById(feature.id);
    expect(updated.status).toBe('completed');
    
    // Verify events published
    const events = await messageQueue.getPublishedEvents('features');
    expect(events).toHaveLength(3);
  });
});
```

---

## 🧩 Fixture Management

```typescript
// Test fixtures
class FeatureFixtures {
  static validFeature() {
    return {
      name: 'OAuth',
      priority: 10,
      description: 'OAuth authentication'
    };
  }
  
  static invalidFeature() {
    return {
      name: '',
      priority: 20
    };
  }
}

describe('With fixtures', () => {
  it('should create with valid fixture', async () => {
    const feature = await service.create(FeatureFixtures.validFeature());
    expect(feature).toBeDefined();
  });
  
  it('should reject invalid fixture', async () => {
    expect(() => 
      service.create(FeatureFixtures.invalidFeature())
    ).toThrow();
  });
});
```

---

## 📚 Related Documents

- Testing Strategies (testing_strategies.md)
- Unit Testing (unit_testing.md)
- E2E Testing (e2e_testing.md)
- Performance Testing (performance_testing.md)

---

**END OF INTEGRATION TESTING DOCUMENT**
