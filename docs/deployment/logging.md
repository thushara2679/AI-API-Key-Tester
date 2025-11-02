# Logging Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Logging Strategies Guide
**Focus:** Comprehensive logging and log analysis

---

## 📝 Structured Logging

### Winston Logger Setup

```typescript
import winston from 'winston';
import ElasticsearchTransport from 'winston-elasticsearch';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: {
    service: 'ai-agent-system',
    environment: process.env.NODE_ENV,
    version: '1.0.0'
  },
  transports: [
    // Console
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    }),
    
    // File
    new winston.transports.File({
      filename: 'logs/error.log',
      level: 'error'
    }),
    new winston.transports.File({
      filename: 'logs/combined.log'
    }),
    
    // Elasticsearch
    new ElasticsearchTransport({
      level: 'info',
      clientOpts: {
        node: process.env.ELASTICSEARCH_URL || 'http://localhost:9200'
      },
      index: 'logs-ai-agent'
    })
  ]
});

// Usage
logger.info('Application started', {
  port: 3000,
  timestamp: new Date()
});

logger.error('Database connection failed', {
  error: err.message,
  stack: err.stack
});
```

### Pino Logger (High Performance)

```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: {
    target: 'pino-pretty',
    options: {
      colorize: true,
      translateTime: 'SYS:standard',
      ignore: 'pid,hostname'
    }
  }
});

// Usage with request middleware
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    const duration = Date.now() - start;
    logger.info({
      method: req.method,
      path: req.path,
      status: res.statusCode,
      duration,
      userAgent: req.get('user-agent')
    });
  });
  
  next();
});
```

---

## 🔍 Log Aggregation

### ELK Stack (Elasticsearch, Logstash, Kibana)

```yaml
# docker-compose.yml - ELK Stack

version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"

  logstash:
    image: docker.elastic.co/logstash/logstash:8.0.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "5000:5000"
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.0.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  elasticsearch_data:
```

### Logstash Configuration

```
# logstash.conf

input {
  tcp {
    port => 5000
    codec => json
  }
}

filter {
  if [type] == "nodejs" {
    mutate {
      add_field => { "[@metadata][index_name]" => "logs-nodejs-%{+YYYY.MM.dd}" }
    }
  }
  
  if [level] == "ERROR" {
    mutate {
      add_field => { "alert_required" => true }
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "%{[@metadata][index_name]}"
  }
  
  if [alert_required] {
    email {
      to => "team@example.com"
      subject => "Error Alert"
    }
  }
}
```

---

## ☁️ Cloud Logging

### AWS CloudWatch

```typescript
import AWS from 'aws-sdk';

const cloudwatch = new AWS.CloudWatchLogs({
  region: process.env.AWS_REGION
});

const params = {
  logGroupName: '/aws/lambda/ai-agent-system',
  logStreamName: 'execution-logs'
};

// Create log group and stream
await cloudwatch.createLogGroup({ logGroupName: params.logGroupName }).promise();
await cloudwatch.createLogStream(params).promise();

// Log events
await cloudwatch.putLogEvents({
  ...params,
  logEvents: [{
    message: JSON.stringify({
      level: 'info',
      timestamp: new Date(),
      message: 'Application started'
    }),
    timestamp: Date.now()
  }]
}).promise();
```

### Google Cloud Logging

```typescript
import { Logging } from '@google-cloud/logging';

const logging = new Logging({
  projectId: process.env.GOOGLE_CLOUD_PROJECT
});

const log = logging.log('ai-agent-system');

const entry = log.entry({
  severity: 'INFO',
  labels: {
    environment: 'production',
    service: 'api'
  },
  jsonPayload: {
    message: 'Application started',
    version: '1.0.0'
  }
});

await log.write(entry);
```

### Azure Application Insights

```typescript
import appInsights from 'applicationinsights';

appInsights.setup(process.env.APPINSIGHTS_INSTRUMENTATION_KEY)
  .setAutoCollectConsole(true)
  .setAutoCollectExceptions(true)
  .setAutoCollectDependencies(true)
  .setAutoCollectPerformance(true)
  .start();

const client = appInsights.defaultClient;

// Log custom event
client.trackEvent({
  name: 'feature_created',
  properties: {
    featureName: 'OAuth',
    priority: 10
  }
});

// Log custom metric
client.trackMetric({
  name: 'api_response_time',
  value: 234
});
```

---

## 📊 Log Analysis

### Log Queries in ELK

```
# Find errors by service
GET /logs-*/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "level": "ERROR" } },
        { "match": { "service": "ai-agent-system" } }
      ],
      "filter": [
        { "range": { "timestamp": { "gte": "now-1h" } } }
      ]
    }
  }
}

# Group by error type
GET /logs-*/_search
{
  "aggs": {
    "error_types": {
      "terms": {
        "field": "error.type",
        "size": 10
      }
    }
  }
}
```

### Log Parsing

```bash
#!/bin/bash
# Parse and analyze logs

# Extract error messages
grep -i "error" combined.log | jq '.message'

# Count requests by status
cat combined.log | jq '.status' | sort | uniq -c

# Find slow requests
cat combined.log | jq 'select(.duration > 1000) | {path, duration}' | head -10

# Time-based analysis
cat combined.log | jq '.timestamp' | head -100 | tail -100 | sort | uniq -c
```

---

## 🔐 Log Security

### Sensitive Data Masking

```typescript
function maskSensitiveData(log: any) {
  const sensitiveFields = ['password', 'token', 'apiKey', 'secret'];
  
  const masked = { ...log };
  
  sensitiveFields.forEach(field => {
    if (masked[field]) {
      masked[field] = '***REDACTED***';
    }
  });
  
  return masked;
}

// Usage
logger.info(maskSensitiveData({
  username: 'user@example.com',
  password: 'secretpassword'  // Will be redacted
}));
```

### Log Retention

```yaml
# Elasticsearch Index Lifecycle Policy

PUT _ilm/policy/logs-policy
{
  "policy": "logs-policy",
  "phases": {
    "hot": {
      "min_age": "0d",
      "actions": {
        "rollover": {
          "max_primary_shard_size": "50GB",
          "max_age": "1d"
        }
      }
    },
    "warm": {
      "min_age": "7d",
      "actions": {
        "set_priority": {
          "priority": 50
        }
      }
    },
    "cold": {
      "min_age": "30d",
      "actions": {
        "set_priority": {
          "priority": 0
        }
      }
    },
    "delete": {
      "min_age": "90d",
      "actions": {
        "delete": {}
      }
    }
  }
}
```

---

## 📚 Related Documents

- Monitoring (monitoring.md)
- Scaling (scaling.md)
- Disaster Recovery (disaster_recovery.md)

---

**END OF LOGGING DOCUMENT**
