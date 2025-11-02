# Unit Testing Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Unit Testing Guide
**Focus:** 50+ unit testing techniques

---

## 🧪 Unit Testing Fundamentals

### Jest Setup

```typescript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  rootDir: './src',
  testMatch: ['**/__tests__/**/*.test.ts', '**/*.test.ts'],
  collectCoverageFrom: ['**/*.ts', '!**/*.d.ts'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  setupFilesAfterEnv: ['<rootDir>/../jest.setup.ts']
};

// jest.setup.ts
jest.mock('axios');
jest.mock('./database');
```

### Basic Test Structure

```typescript
describe('FeatureValidator', () => {
  let validator: FeatureValidator;
  
  beforeAll(() => {
    console.log('Setup once for all tests');
  });
  
  beforeEach(() => {
    validator = new FeatureValidator();
  });
  
  afterEach(() => {
    jest.clearAllMocks();
  });
  
  afterAll(() => {
    console.log('Cleanup after all tests');
  });
  
  describe('validateName', () => {
    it('should accept valid names', () => {
      expect(validator.validateName('OAuth')).toBe(true);
      expect(validator.validateName('API Gateway')).toBe(true);
    });
    
    it('should reject invalid names', () => {
      expect(validator.validateName('')).toBe(false);
      expect(validator.validateName(null as any)).toBe(false);
    });
  });
});
```

---

## 📝 Test Patterns

### Testing Pure Functions

```typescript
// Function under test
function calculatePriority(impact: number, effort: number): number {
  if (impact < 0 || effort <= 0) {
    throw new Error('Invalid inputs');
  }
  return impact / effort;
}

// Tests
describe('calculatePriority', () => {
  it('should calculate priority correctly', () => {
    expect(calculatePriority(10, 2)).toBe(5);
    expect(calculatePriority(15, 3)).toBe(5);
  });
  
  it('should handle zero effort', () => {
    expect(() => calculatePriority(10, 0)).toThrow('Invalid inputs');
  });
  
  it('should handle negative impact', () => {
    expect(() => calculatePriority(-10, 2)).toThrow('Invalid inputs');
  });
});
```

### Testing Classes

```typescript
class Feature {
  private id: string;
  private name: string;
  private priority: number;
  
  constructor(name: string, priority: number) {
    this.id = generateId();
    this.name = name;
    this.priority = priority;
  }
  
  getName(): string {
    return this.name;
  }
  
  getPriority(): number {
    return this.priority;
  }
  
  setPriority(priority: number): void {
    if (priority < 1 || priority > 13) {
      throw new Error('Invalid priority');
    }
    this.priority = priority;
  }
}

describe('Feature', () => {
  let feature: Feature;
  
  beforeEach(() => {
    feature = new Feature('OAuth', 10);
  });
  
  it('should create feature with name and priority', () => {
    expect(feature.getName()).toBe('OAuth');
    expect(feature.getPriority()).toBe(10);
  });
  
  it('should update priority', () => {
    feature.setPriority(12);
    expect(feature.getPriority()).toBe(12);
  });
  
  it('should reject invalid priority', () => {
    expect(() => feature.setPriority(0)).toThrow('Invalid priority');
    expect(() => feature.setPriority(14)).toThrow('Invalid priority');
  });
});
```

### Testing Async Functions

```typescript
describe('AsyncFeatureService', () => {
  let service: AsyncFeatureService;
  
  beforeEach(() => {
    service = new AsyncFeatureService();
  });
  
  // Using async/await
  it('should fetch features', async () => {
    const features = await service.fetchFeatures();
    expect(features).toHaveLength(3);
  });
  
  // Using .then()
  it('should handle fetch error', () => {
    return service.fetchFeatures()
      .then(() => {
        throw new Error('Should have failed');
      })
      .catch(error => {
        expect(error.message).toBe('Network error');
      });
  });
  
  // Using done callback
  it('should process features', (done) => {
    service.processFeatures().then(result => {
      expect(result).toBe('processed');
      done();
    }).catch(done);
  });
  
  // Using jest.useFakeTimers()
  it('should handle delayed response', async () => {
    jest.useFakeTimers();
    const promise = service.delayedFetch(1000);
    
    jest.runAllTimers();
    
    await promise;
    expect(service.isFetched()).toBe(true);
    
    jest.useRealTimers();
  });
});
```

### Testing Promises

```typescript
describe('Promise handling', () => {
  it('should resolve with value', () => {
    return expect(
      Promise.resolve('success')
    ).resolves.toBe('success');
  });
  
  it('should reject with error', () => {
    return expect(
      Promise.reject(new Error('failed'))
    ).rejects.toThrow('failed');
  });
  
  it('should handle multiple promises', () => {
    const promise1 = Promise.resolve('first');
    const promise2 = Promise.resolve('second');
    
    return expect(
      Promise.all([promise1, promise2])
    ).resolves.toEqual(['first', 'second']);
  });
});
```

---

## 🎭 Mocking Techniques

### Jest Mocks

```typescript
// Mock module
jest.mock('./database', () => ({
  Database: jest.fn().mockImplementation(() => ({
    save: jest.fn().mockResolvedValue({ id: '1' }),
    find: jest.fn().mockResolvedValue(null),
    delete: jest.fn().mockResolvedValue(true)
  }))
}));

// Mock function
const mockFetch = jest.fn();
mockFetch.mockResolvedValue({ ok: true, json: () => ({ id: '1' }) });

// Mock implementation
jest.spyOn(console, 'log').mockImplementation(() => {});

// Testing with mocks
describe('FeatureService', () => {
  let service: FeatureService;
  
  beforeEach(() => {
    service = new FeatureService();
  });
  
  it('should call database on create', async () => {
    const { Database } = require('./database');
    const db = new Database();
    
    await service.createFeature(db, { name: 'OAuth' });
    
    expect(db.save).toHaveBeenCalled();
    expect(db.save).toHaveBeenCalledWith(
      expect.objectContaining({ name: 'OAuth' })
    );
  });
});
```

### Spy Functions

```typescript
describe('Spy functions', () => {
  const obj = {
    getValue: () => 42
  };
  
  it('should track function calls', () => {
    const spy = jest.spyOn(obj, 'getValue');
    
    obj.getValue();
    obj.getValue();
    
    expect(spy).toHaveBeenCalledTimes(2);
    expect(spy).toHaveReturnedWith(42);
    
    spy.mockRestore();
  });
  
  it('should override implementation', () => {
    const spy = jest.spyOn(obj, 'getValue')
      .mockImplementation(() => 100);
    
    expect(obj.getValue()).toBe(100);
    
    spy.mockRestore();
  });
});
```

### Partial Mocks

```typescript
describe('Partial mocking', () => {
  it('should mock only specific method', () => {
    const service = new FeatureService();
    
    jest.spyOn(service, 'createFeature')
      .mockResolvedValue({ id: '1', name: 'OAuth' });
    
    jest.spyOn(service, 'getFeatures')
      .mockImplementation(async () => {
        return service.createFeature({ name: 'OAuth' });
      });
    
    expect(service.getFeatures).toBeDefined();
  });
});
```

---

## 🔍 Assertions

### Common Assertions

```typescript
describe('Assertions', () => {
  it('should test equality', () => {
    expect(5 + 5).toBe(10);
    expect({ name: 'OAuth' }).toEqual({ name: 'OAuth' });
    expect(null).toBeNull();
    expect(undefined).toBeUndefined();
  });
  
  it('should test truthiness', () => {
    expect(true).toBeTruthy();
    expect(false).toBeFalsy();
    expect('text').toBeTruthy();
    expect('').toBeFalsy();
  });
  
  it('should test arrays', () => {
    const arr = [1, 2, 3];
    expect(arr).toContain(2);
    expect(arr).toHaveLength(3);
    expect(arr).toEqual([1, 2, 3]);
  });
  
  it('should test objects', () => {
    const obj = { name: 'OAuth', priority: 10 };
    expect(obj).toHaveProperty('name');
    expect(obj).toMatchObject({ name: 'OAuth' });
  });
  
  it('should test strings', () => {
    expect('OAuth').toMatch('Auth');
    expect('OAuth').toHaveLength(5);
  });
  
  it('should test functions', () => {
    const fn = jest.fn();
    fn('test');
    
    expect(fn).toHaveBeenCalled();
    expect(fn).toHaveBeenCalledWith('test');
    expect(fn).toHaveBeenCalledTimes(1);
  });
});
```

### Custom Matchers

```typescript
expect.extend({
  toBeValidFeature(received) {
    const isValid = received.id && received.name && 
                   received.priority >= 1 && received.priority <= 13;
    
    return {
      message: () => `expected ${JSON.stringify(received)} to be valid feature`,
      pass: isValid
    };
  }
});

describe('Custom matchers', () => {
  it('should validate feature', () => {
    const feature = { id: '1', name: 'OAuth', priority: 10 };
    expect(feature).toBeValidFeature();
  });
});
```

---

## 📊 Parameterized Tests

```typescript
describe('Parameterized tests', () => {
  // Test multiple inputs
  test.each([
    [1, 1, 2],
    [2, 3, 5],
    [0, 0, 0],
    [-1, 1, 0]
  ])('add(%i, %i) = %i', (a, b, expected) => {
    expect(add(a, b)).toBe(expected);
  });
  
  // Test with object data
  test.each([
    { name: 'OAuth', priority: 10, valid: true },
    { name: '', priority: 10, valid: false },
    { name: 'API', priority: 20, valid: false }
  ])('validate($name, $priority) should be $valid', ({ name, priority, valid }) => {
    expect(validate({ name, priority })).toBe(valid);
  });
});
```

---

## 🐛 Debugging Tests

```typescript
describe('Debugging tests', () => {
  it('should debug with console', () => {
    const data = { name: 'OAuth' };
    console.log('Data:', data);
    console.table(data);
    
    expect(data.name).toBe('OAuth');
  });
  
  it.only('should run only this test', () => {
    expect(1 + 1).toBe(2);
  });
  
  it.skip('should skip this test', () => {
    expect(1 + 1).toBe(3);
  });
  
  it.todo('should test this later', () => {
    // TODO: implement
  });
});
```

---

## 🎯 Testing Best Practices

### Do's and Don'ts

```typescript
// ✅ DO: Keep tests simple and focused
it('should create feature', async () => {
  const feature = await service.create({ name: 'OAuth' });
  expect(feature.name).toBe('OAuth');
});

// ❌ AVOID: Complex test setup
it('should create feature', async () => {
  const config = await loadConfig();
  const db = await initDb();
  const service = new Service(db, config);
  const middleware = new Middleware();
  const feature = await service.create({ name: 'OAuth' });
  expect(feature.name).toBe('OAuth');
});

// ✅ DO: Use descriptive names
it('should reject feature with priority > 13', () => {
  expect(() => create({ name: 'OAuth', priority: 20 }))
    .toThrow('Invalid priority');
});

// ✅ DO: Test boundaries
describe('Priority validation', () => {
  it('should accept priority 1', () => {
    expect(validate({ priority: 1 })).toBe(true);
  });
  it('should accept priority 13', () => {
    expect(validate({ priority: 13 })).toBe(true);
  });
  it('should reject priority 0', () => {
    expect(validate({ priority: 0 })).toBe(false);
  });
});

// ✅ DO: Isolate tests
describe('Independent tests', () => {
  let service: Service;
  
  beforeEach(() => {
    service = new Service();
  });
  
  // Each test is independent
});
```

---

## 📚 Related Documents

- Testing Strategies (testing_strategies.md)
- Integration Testing (integration_testing.md)
- E2E Testing (e2e_testing.md)
- Performance Testing (performance_testing.md)
- Security Testing (security_testing.md)

---

**END OF UNIT TESTING DOCUMENT**
