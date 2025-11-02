# Monitoring Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Monitoring & Observability Guide
**Focus:** Comprehensive system monitoring strategies

---

## 📊 Metrics Collection

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['localhost:9093']

rule_files:
  - 'alert_rules.yml'

scrape_configs:
  - job_name: 'api'
    static_configs:
      - targets: ['localhost:3000']
    metrics_path: '/metrics'

  - job_name: 'database'
    static_configs:
      - targets: ['localhost:5432']
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
```

### Custom Metrics

```typescript
import { Counter, Histogram, Gauge, Register } from 'prom-client';

const register = new Register();

// Request counter
const httpRequests = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status'],
  registers: [register]
});

// Request duration
const httpDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method', 'route'],
  buckets: [0.1, 0.5, 1, 2, 5],
  registers: [register]
});

// Active connections
const activeConnections = new Gauge({
  name: 'active_connections',
  help: 'Number of active connections',
  registers: [register]
});

// Usage
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    httpRequests.inc({
      method: req.method,
      route: req.route?.path || 'unknown',
      status: res.statusCode
    });
    httpDuration.observe({
      method: req.method,
      route: req.route?.path || 'unknown'
    }, duration);
  });
  
  next();
});
```

---

## 🚨 Alerting

### Alert Rules

```yaml
# alert_rules.yml
groups:
  - name: api_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 2m
        annotations:
          summary: "High error rate"
          description: "Error rate is above 5%"

      - alert: HighLatency
        expr: histogram_quantile(0.95, http_request_duration_seconds_bucket) > 1
        for: 5m
        annotations:
          summary: "High latency detected"
          description: "p95 latency is above 1 second"

      - alert: DatabaseDown
        expr: up{job="database"} == 0
        for: 1m
        annotations:
          summary: "Database is down"

      - alert: HighMemoryUsage
        expr: container_memory_usage_bytes / container_spec_memory_limit_bytes > 0.9
        for: 3m
        annotations:
          summary: "High memory usage"

      - alert: DiskSpaceLow
        expr: node_filesystem_avail_bytes / node_filesystem_size_bytes < 0.1
        for: 5m
        annotations:
          summary: "Disk space running low"
```

### Alertmanager Configuration

```yaml
global:
  resolve_timeout: 5m

route:
  receiver: 'default'
  group_by: ['alertname', 'cluster']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  routes:
    - match:
        severity: critical
      receiver: 'critical'
      repeat_interval: 5m
    - match:
        severity: warning
      receiver: 'warning'
      repeat_interval: 1h

receivers:
  - name: 'default'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/...'
        channel: '#monitoring'

  - name: 'critical'
    pagerduty_configs:
      - service_key: '...'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/...'
        channel: '#critical-alerts'
    email_configs:
      - to: 'on-call@example.com'

  - name: 'warning'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/...'
        channel: '#warnings'
```

---

## 📈 Grafana Dashboards

### Dashboard JSON

```json
{
  "dashboard": {
    "title": "AI Agent System",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m])"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Latency (p95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, http_request_duration_seconds_bucket)"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Database Connections",
        "targets": [
          {
            "expr": "pg_stat_activity_count"
          }
        ],
        "type": "gauge"
      }
    ]
  }
}
```

---

## 🔍 Distributed Tracing

### OpenTelemetry Setup

```typescript
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { JaegerExporter } from '@opentelemetry/exporter-jaeger-basic';
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-node';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'ai-agent-system',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0'
  }),
  instrumentations: [getNodeAutoInstrumentations()],
  traceExporter: new JaegerExporter({
    host: 'localhost',
    port: 6831
  })
});

sdk.start();

// Usage in app
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('app-tracer');

async function createFeature(data) {
  const span = tracer.startSpan('createFeature');
  
  try {
    const feature = await db.features.create(data);
    span.setAttributes({
      'feature.id': feature.id,
      'feature.name': feature.name
    });
    return feature;
  } catch (error) {
    span.recordException(error);
    throw error;
  } finally {
    span.end();
  }
}
```

---

## 🐳 Container Monitoring

### Docker Stats

```bash
#!/bin/bash
# Monitor running containers

docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Log monitoring
docker logs -f ai-agent-system | grep -i error
```

### Kubernetes Monitoring

```bash
# Pod metrics
kubectl top pods -n default

# Node metrics
kubectl top nodes

# Watch pod status
kubectl get pods -w

# Describe pod for events
kubectl describe pod ai-agent-system-xyz
```

---

## 📚 Related Documents

- Logging (logging.md)
- Scaling (scaling.md)
- Disaster Recovery (disaster_recovery.md)

---

**END OF MONITORING DOCUMENT**
