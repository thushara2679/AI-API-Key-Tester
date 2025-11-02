# Performance Testing Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Performance Testing Guide
**Focus:** 50+ performance testing techniques

---

## 📊 Performance Metrics

### Key Metrics to Track

```typescript
interface PerformanceMetrics {
  responseTime: number;      // ms
  throughput: number;        // requests/sec
  cpuUsage: number;          // %
  memoryUsage: number;       // MB
  diskIO: number;            // MB/s
  errorRate: number;         // %
  p50Latency: number;        // ms
  p95Latency: number;        // ms
  p99Latency: number;        // ms
}

class PerformanceMonitor {
  async measureResponseTime(url: string): Promise<number> {
    const start = performance.now();
    const response = await fetch(url);
    const end = performance.now();
    return end - start;
  }

  async measureThroughput(
    url: string,
    concurrentRequests: number,
    duration: number
  ): Promise<number> {
    let totalRequests = 0;
    const promises = [];

    for (let i = 0; i < concurrentRequests; i++) {
      promises.push(
        (async () => {
          const start = Date.now();
          while (Date.now() - start < duration) {
            await fetch(url);
            totalRequests++;
          }
        })()
      );
    }

    await Promise.all(promises);
    return totalRequests / (duration / 1000);
  }
}
```

---

## 🔫 Load Testing

### Artillery Load Testing

```yaml
# load-test.yml
config:
  target: "http://localhost:3000"
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 300
      arrivalRate: 50
      name: "Ramp up"
    - duration: 600
      arrivalRate: 100
      name: "Sustained"
    - duration: 60
      arrivalRate: 0
      name: "Ramp down"

scenarios:
  - name: "Feature Management Workflow"
    flow:
      - get:
          url: "/api/features"
      - post:
          url: "/api/features"
          json:
            name: "OAuth"
            priority: 10
      - get:
          url: "/api/features/{{ featureId }}"
      - patch:
          url: "/api/features/{{ featureId }}"
          json:
            priority: 12
      - delete:
          url: "/api/features/{{ featureId }}"
```

### K6 Load Testing

```typescript
// load-test.js
import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend, Counter, Gauge } from 'k6/metrics';

export const options = {
  vus: 100,
  duration: '5m',
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.1'],
  },
};

// Custom metrics
const errorRate = new Rate('errors');
const createLatency = new Trend('create_latency');
const getLatency = new Trend('get_latency');
const requestCounter = new Counter('requests');

export default () => {
  group('Create Feature', () => {
    const res = http.post('http://localhost:3000/api/features', {
      name: 'OAuth',
      priority: 10
    });

    createLatency.add(res.timings.duration);
    errorRate.add(res.status === 201 ? 0 : 1);
    requestCounter.add(1);

    check(res, {
      'status is 201': (r) => r.status === 201,
      'response time < 500ms': (r) => r.timings.duration < 500,
    });
  });

  group('Get Feature', () => {
    const res = http.get('http://localhost:3000/api/features/1');

    getLatency.add(res.timings.duration);
    errorRate.add(res.status === 200 ? 0 : 1);
    requestCounter.add(1);

    check(res, {
      'status is 200': (r) => r.status === 200,
      'response time < 300ms': (r) => r.timings.duration < 300,
    });
  });

  sleep(1);
};
```

---

## 🔍 Profiling & Monitoring

### Node.js Profiling

```typescript
import * as profiler from '@node-clinic/doctor';

// Clinic.js profiling
async function profileApp() {
  const startProfiler = profiler.start();

  // Run your app
  const app = express();
  app.get('/api/features', (req, res) => {
    // endpoint code
    res.json([]);
  });

  app.listen(3000);

  // Simulate load
  for (let i = 0; i < 1000; i++) {
    await fetch('http://localhost:3000/api/features');
  }

  const report = await startProfiler.stop();
  console.log('Profile report:', report);
}

// Built-in profiler
import { performance } from 'perf_hooks';

function measureMemory(fn: () => void) {
  const before = process.memoryUsage();
  fn();
  const after = process.memoryUsage();

  return {
    heapUsed: after.heapUsed - before.heapUsed,
    external: after.external - before.external,
    rss: after.rss - before.rss
  };
}
```

### Chrome DevTools Profiling

```typescript
// Browser performance profiling
describe('Browser Performance', () => {
  it('should have acceptable performance metrics', async () => {
    const page = await browser.newPage();

    // Start performance monitoring
    const startMetrics = await page.metrics();

    await page.goto('http://localhost:3000/features');
    await page.waitForSelector('[data-testid="feature-list"]');

    const endMetrics = await page.metrics();

    const layout = endMetrics.LayoutCount - startMetrics.LayoutCount;
    const recalc = endMetrics.RecalcStyleCount - startMetrics.RecalcStyleCount;

    expect(layout).toBeLessThan(10);
    expect(recalc).toBeLessThan(20);
  });
});
```

---

## 🎯 Stress Testing

### Stress Scenarios

```typescript
// Stress test with increasing load
class StressTest {
  async runStressTest() {
    const baseUrl = 'http://localhost:3000/api/features';
    const maxConcurrency = 1000;
    const incrementStep = 100;
    let failures = 0;

    for (let concurrent = 100; concurrent <= maxConcurrency; concurrent += incrementStep) {
      const requests = Array(concurrent)
        .fill(null)
        .map(() => fetch(baseUrl).catch(() => failures++));

      await Promise.all(requests);

      console.log(`Concurrent: ${concurrent}, Failures: ${failures}`);

      if (failures / concurrent > 0.1) {
        console.log(`Stress limit reached at ${concurrent} concurrent requests`);
        break;
      }
    }
  }
}

// Spike testing
class SpikeTest {
  async runSpikeTest() {
    const baseUrl = 'http://localhost:3000/api/features';

    // Normal load
    await this.sendRequests(10, 60000); // 10 req/s for 60s

    // Sudden spike
    console.log('Sending spike...');
    await this.sendRequests(500, 10000); // 500 req/s for 10s

    // Recovery
    await this.sendRequests(10, 60000); // 10 req/s for 60s
  }

  private async sendRequests(rps: number, duration: number) {
    const interval = 1000 / rps;
    const end = Date.now() + duration;

    while (Date.now() < end) {
      fetch('http://localhost:3000/api/features');
      await new Promise(resolve => setTimeout(resolve, interval));
    }
  }
}
```

---

## 💾 Memory & Resource Testing

### Memory Leak Detection

```typescript
// Test for memory leaks
class MemoryLeakTest {
  async detectLeaks() {
    const iterations = 10000;
    const baseline = process.memoryUsage();

    for (let i = 0; i < iterations; i++) {
      const obj = {
        data: new Array(1000).fill('test'),
        nested: {
          deep: {
            value: Math.random()
          }
        }
      };
      // If this object isn't garbage collected, memory will leak
    }

    global.gc?.();
    const final = process.memoryUsage();

    const leaked = final.heapUsed - baseline.heapUsed;
    console.log(`Memory change: ${leaked / 1024 / 1024} MB`);

    if (leaked > 10 * 1024 * 1024) { // > 10MB
      throw new Error('Potential memory leak detected');
    }
  }
}

// Connection pool exhaustion
class ConnectionPoolTest {
  async testPoolExhaustion() {
    const pool = createPool({ max: 10 });
    const connections = [];

    try {
      for (let i = 0; i < 100; i++) {
        const conn = await pool.acquire();
        connections.push(conn);
      }
    } catch (e) {
      console.log(`Pool exhausted at ${connections.length} connections`);
    } finally {
      connections.forEach(conn => pool.release(conn));
    }
  }
}
```

---

## 📈 Database Performance

### Query Performance Testing

```typescript
describe('Database Query Performance', () => {
  it('should fetch features in < 100ms', async () => {
    const start = performance.now();
    const features = await db.features.findAll();
    const duration = performance.now() - start;

    expect(duration).toBeLessThan(100);
    expect(features).toHaveLength(10000);
  });

  it('should index queries properly', async () => {
    const start = performance.now();
    const feature = await db.features.findById('123');
    const duration = performance.now() - start;

    // Indexed query should be < 10ms
    expect(duration).toBeLessThan(10);
  });

  it('should handle bulk operations efficiently', async () => {
    const features = Array(1000)
      .fill(null)
      .map((_, i) => ({ name: `Feature ${i}`, priority: Math.random() * 13 }));

    const start = performance.now();
    await db.features.insertMany(features);
    const duration = performance.now() - start;

    expect(duration).toBeLessThan(1000); // < 1 second for 1000 rows
  });
});
```

---

## 🔄 Continuous Performance Testing

### Automated Performance Checks

```yaml
# .github/workflows/performance.yml
name: Performance Tests

on:
  push:
    branches: [main]
  pull_request:

jobs:
  performance:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Start app
        run: npm start &
      
      - name: Run load tests
        run: |
          npx k6 run load-test.js --vus 50 --duration 5m \
            --summary-export=results.json
      
      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: performance-results
          path: results.json
      
      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const results = require('./results.json');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `Performance: ${results.metrics.http_req_duration.p95} ms (p95)`
            });
```

---

## 📚 Related Documents

- Testing Strategies (testing_strategies.md)
- Security Testing (security_testing.md)
- Integration Testing (integration_testing.md)

---

**END OF PERFORMANCE TESTING DOCUMENT**
