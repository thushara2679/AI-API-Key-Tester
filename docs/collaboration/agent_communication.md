# Agent Communication Protocols

## Overview

Agent communication is the foundation of multi-agent system coordination. This document outlines comprehensive communication protocols, message formats, and best practices for agents within the Advanced AI Agent System for Enterprise Automation.

---

## 1. Communication Architecture

### 1.1 Message Bus Architecture

The agent communication system uses a central message bus pattern for asynchronous, decoupled communication.

```
┌─────────────────────────────────────────────────────┐
│         Central Message Bus (RabbitMQ/Kafka)        │
└────────────┬──────────────────────┬────────────────┘
             │                      │
      ┌──────▼──────┐      ┌────────▼──────┐
      │  Producer   │      │   Consumer    │
      │   Agents    │      │    Agents     │
      └─────────────┘      └───────────────┘
             ▲                      ▲
             └──────────────────────┘
         Bidirectional Communication
```

### 1.2 Communication Patterns

**Request-Reply Pattern**
```javascript
// Agent A sends request
const request = {
  id: 'req_12345',
  type: 'REQUEST',
  source: 'agent_a',
  target: 'agent_b',
  action: 'process_data',
  payload: { data: 'value' },
  timestamp: Date.now(),
  timeout: 5000
};

// Agent B receives and responds
const response = {
  id: 'req_12345',
  type: 'RESPONSE',
  source: 'agent_b',
  target: 'agent_a',
  status: 'SUCCESS',
  payload: { result: 'processed' },
  timestamp: Date.now()
};
```

**Publish-Subscribe Pattern**
```javascript
// Agent publishes event
const event = {
  id: 'evt_67890',
  type: 'EVENT',
  source: 'agent_a',
  channel: 'data_processing',
  event: 'data_processed',
  payload: { batch: 100, status: 'complete' },
  timestamp: Date.now()
};

// Multiple agents subscribe to channel
subscribers.forEach(agent => {
  agent.emit('data_processed', event);
});
```

**Broadcast Pattern**
```javascript
// Agent broadcasts to all agents
const broadcast = {
  id: 'bcast_11111',
  type: 'BROADCAST',
  source: 'agent_system',
  action: 'system_alert',
  severity: 'CRITICAL',
  message: 'System maintenance required',
  timestamp: Date.now(),
  requires_ack: true
};
```

---

## 2. Message Format Specification

### 2.1 Standard Message Schema

```javascript
{
  // Message identification
  id: string,                    // Unique message ID (UUID)
  correlationId: string,         // For tracking request chains
  
  // Message source and target
  source: string,                // Source agent ID
  target: string | string[],     // Target agent ID(s)
  
  // Message type and action
  type: 'REQUEST' | 'RESPONSE' | 'EVENT' | 'BROADCAST' | 'ERROR',
  action: string,                // Action to perform
  channel: string,               // Pub-sub channel (optional)
  
  // Message content
  payload: object,               // Message data
  metadata: {
    priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL',
    encrypted: boolean,
    compression: 'none' | 'gzip' | 'brotli',
    retryable: boolean,
    maxRetries: number
  },
  
  // Timing and lifecycle
  timestamp: number,             // Message creation time (ms)
  expireAt: number,              // Message expiration time
  timeout: number,               // Response timeout (ms)
  
  // Response tracking
  replyTo: string,               // Channel/queue for replies
  responseRequired: boolean,
  
  // Status tracking
  status: 'PENDING' | 'PROCESSING' | 'SUCCESS' | 'FAILED' | 'TIMEOUT',
  error: {                       // Error details if failed
    code: string,
    message: string,
    stack: string
  }
}
```

### 2.2 Message Type Details

**REQUEST Messages**
```javascript
{
  type: 'REQUEST',
  id: 'req_abc123',
  source: 'data_processor',
  target: 'data_validator',
  action: 'validate_dataset',
  payload: {
    datasetId: 'ds_001',
    rules: ['required_fields', 'data_types'],
    strictMode: true
  },
  metadata: {
    priority: 'HIGH',
    timeout: 10000,
    retryable: true,
    maxRetries: 3
  },
  replyTo: 'data_processor/results',
  responseRequired: true
}
```

**RESPONSE Messages**
```javascript
{
  type: 'RESPONSE',
  id: 'res_abc123',
  correlationId: 'req_abc123',
  source: 'data_validator',
  target: 'data_processor',
  status: 'SUCCESS',
  payload: {
    validationResults: {
      passed: true,
      errors: [],
      warnings: ['field_abc_null_values'],
      statistics: { total: 1000, valid: 995, invalid: 5 }
    }
  },
  timestamp: Date.now()
}
```

**EVENT Messages**
```javascript
{
  type: 'EVENT',
  id: 'evt_xyz789',
  source: 'data_processor',
  action: 'processing_complete',
  channel: 'data_events',
  payload: {
    processId: 'proc_001',
    recordsProcessed: 10000,
    duration: 5432,
    status: 'completed'
  },
  timestamp: Date.now()
}
```

---

## 3. Communication Protocols

### 3.1 RabbitMQ Protocol

**Queue Setup**
```javascript
const amqp = require('amqplib');

async function setupRabbitMQ() {
  const connection = await amqp.connect('amqp://localhost');
  const channel = await connection.createChannel();
  
  // Declare exchanges
  await channel.assertExchange('agent_events', 'topic', { durable: true });
  await channel.assertExchange('agent_requests', 'direct', { durable: true });
  
  // Declare queues
  await channel.assertQueue('agent_a_queue', { durable: true });
  await channel.assertQueue('agent_b_queue', { durable: true });
  
  // Bind queues to exchanges
  await channel.bindQueue('agent_a_queue', 'agent_events', 'data.*');
  await channel.bindQueue('agent_b_queue', 'agent_requests', 'validation');
  
  return { connection, channel };
}
```

**Message Publishing**
```javascript
async function publishMessage(channel, message) {
  const exchange = message.type === 'EVENT' ? 'agent_events' : 'agent_requests';
  const routingKey = message.type === 'EVENT' ? message.channel : message.action;
  
  const published = channel.publish(
    exchange,
    routingKey,
    Buffer.from(JSON.stringify(message)),
    {
      persistent: true,
      contentType: 'application/json',
      contentEncoding: 'utf-8',
      timestamp: Date.now()
    }
  );
  
  return published;
}
```

**Message Consumption**
```javascript
async function consumeMessages(channel, queue) {
  await channel.consume(queue, async (msg) => {
    if (msg === null) return;
    
    try {
      const message = JSON.parse(msg.content.toString());
      await handleMessage(message);
      channel.ack(msg);
    } catch (error) {
      console.error('Message processing error:', error);
      channel.nack(msg, false, true); // Requeue
    }
  });
}
```

### 3.2 Apache Kafka Protocol

**Topic Configuration**
```bash
# Create topics with replication
kafka-topics.sh --create \
  --topic agent-events \
  --partitions 3 \
  --replication-factor 2 \
  --config retention.ms=86400000

kafka-topics.sh --create \
  --topic agent-requests \
  --partitions 2 \
  --replication-factor 2 \
  --config compression.type=snappy
```

**Producer Implementation**
```javascript
const kafka = require('kafkajs').Kafka;

const client = new kafka.Kafka({
  clientId: 'agent_system',
  brokers: ['localhost:9092'],
  retry: { initialRetryTime: 100, retries: 8 }
});

const producer = client.producer();

async function publishToKafka(message) {
  await producer.connect();
  
  await producer.send({
    topic: message.type === 'EVENT' ? 'agent-events' : 'agent-requests',
    messages: [{
      key: message.source,
      value: JSON.stringify(message),
      timestamp: Date.now().toString()
    }],
    compression: 1 // Gzip
  });
}
```

**Consumer Implementation**
```javascript
const consumer = client.consumer({ groupId: 'agent_group' });

async function consumeFromKafka() {
  await consumer.connect();
  await consumer.subscribe({ 
    topic: 'agent-events', 
    fromBeginning: false 
  });
  
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const data = JSON.parse(message.value.toString());
      await handleMessage(data);
    }
  });
}
```

### 3.3 gRPC Protocol (Synchronous Communication)

**Service Definition (Protocol Buffers)**
```protobuf
syntax = "proto3";

package agent;

service AgentCommunication {
  rpc SendRequest(RequestMessage) returns (ResponseMessage) {}
  rpc SendEvent(EventMessage) returns (AckMessage) {}
  rpc HealthCheck(Empty) returns (HealthStatus) {}
}

message RequestMessage {
  string id = 1;
  string source = 2;
  string target = 3;
  string action = 4;
  bytes payload = 5;
  int64 timeout = 6;
}

message ResponseMessage {
  string id = 1;
  string status = 2;
  bytes payload = 3;
  string error = 4;
}

message EventMessage {
  string id = 1;
  string source = 2;
  string channel = 3;
  bytes payload = 4;
}

message AckMessage {
  string id = 1;
  bool acknowledged = 2;
}

message Empty {}

message HealthStatus {
  enum Status {
    UNKNOWN = 0;
    SERVING = 1;
    NOT_SERVING = 2;
  }
  Status status = 1;
}
```

**gRPC Server Implementation**
```javascript
const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const packageDefinition = protoLoader.loadSync('agent.proto');
const agentProto = grpc.loadPackageDefinition(packageDefinition).agent;

const server = new grpc.Server();

server.addService(agentProto.AgentCommunication.service, {
  SendRequest: async (call, callback) => {
    try {
      const response = await handleRequest(call.request);
      callback(null, response);
    } catch (error) {
      callback(error);
    }
  },
  
  SendEvent: async (call, callback) => {
    try {
      await handleEvent(call.request);
      callback(null, { id: call.request.id, acknowledged: true });
    } catch (error) {
      callback(error);
    }
  },
  
  HealthCheck: (call, callback) => {
    callback(null, { status: 'SERVING' });
  }
});

server.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => {
  server.start();
});
```

---

## 4. Message Routing and Delivery

### 4.1 Routing Strategy

```javascript
class MessageRouter {
  constructor() {
    this.routes = new Map();
    this.brokers = [];
  }
  
  registerAgent(agentId, config) {
    this.routes.set(agentId, {
      id: agentId,
      protocol: config.protocol,     // 'rabbitmq', 'kafka', 'grpc'
      endpoint: config.endpoint,
      queue: config.queue,
      filters: config.filters || [],
      priority: config.priority || 'MEDIUM'
    });
  }
  
  async routeMessage(message) {
    const route = this.routes.get(message.target);
    
    if (!route) {
      throw new Error(`No route found for agent: ${message.target}`);
    }
    
    // Apply message filters
    if (!this.applyFilters(message, route.filters)) {
      return { status: 'FILTERED' };
    }
    
    // Route based on protocol
    switch (route.protocol) {
      case 'rabbitmq':
        return this.routeViaRabbitMQ(message, route);
      case 'kafka':
        return this.routeViaKafka(message, route);
      case 'grpc':
        return this.routeViaGRPC(message, route);
      default:
        throw new Error(`Unknown protocol: ${route.protocol}`);
    }
  }
  
  applyFilters(message, filters) {
    return filters.every(filter => {
      switch (filter.type) {
        case 'priority':
          return this.getPriorityLevel(message.metadata.priority) >= filter.value;
        case 'action':
          return filter.actions.includes(message.action);
        case 'source':
          return filter.sources.includes(message.source);
        default:
          return true;
      }
    });
  }
  
  getPriorityLevel(priority) {
    const levels = { LOW: 1, MEDIUM: 2, HIGH: 3, CRITICAL: 4 };
    return levels[priority] || 0;
  }
}
```

### 4.2 Load Balancing

```javascript
class LoadBalancer {
  constructor(strategy = 'round-robin') {
    this.strategy = strategy;
    this.brokers = [];
    this.currentIndex = 0;
  }
  
  // Round-robin strategy
  selectBrokerRoundRobin() {
    const broker = this.brokers[this.currentIndex];
    this.currentIndex = (this.currentIndex + 1) % this.brokers.length;
    return broker;
  }
  
  // Least connections strategy
  selectBrokerLeastConnections() {
    return this.brokers.reduce((least, broker) => 
      broker.activeConnections < least.activeConnections ? broker : least
    );
  }
  
  // Weighted strategy
  selectBrokerWeighted() {
    const totalWeight = this.brokers.reduce((sum, b) => sum + b.weight, 0);
    let random = Math.random() * totalWeight;
    
    for (const broker of this.brokers) {
      random -= broker.weight;
      if (random <= 0) return broker;
    }
  }
  
  selectBroker(message) {
    switch (this.strategy) {
      case 'round-robin':
        return this.selectBrokerRoundRobin();
      case 'least-connections':
        return this.selectBrokerLeastConnections();
      case 'weighted':
        return this.selectBrokerWeighted();
      default:
        return this.selectBrokerRoundRobin();
    }
  }
}
```

---

## 5. Error Handling and Resilience

### 5.1 Retry Mechanism

```javascript
class MessageRetry {
  constructor(config = {}) {
    this.maxRetries = config.maxRetries || 3;
    this.backoffStrategy = config.backoffStrategy || 'exponential';
    this.initialDelay = config.initialDelay || 1000;
    this.maxDelay = config.maxDelay || 30000;
  }
  
  async sendWithRetry(message, sender) {
    let lastError;
    
    for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
      try {
        return await sender(message);
      } catch (error) {
        lastError = error;
        
        if (attempt < this.maxRetries && message.metadata.retryable) {
          const delay = this.calculateDelay(attempt);
          console.log(`Retry attempt ${attempt + 1} after ${delay}ms`);
          await this.sleep(delay);
        } else {
          break;
        }
      }
    }
    
    throw lastError;
  }
  
  calculateDelay(attempt) {
    switch (this.backoffStrategy) {
      case 'exponential':
        return Math.min(
          this.initialDelay * Math.pow(2, attempt),
          this.maxDelay
        );
      case 'linear':
        return Math.min(
          this.initialDelay * (attempt + 1),
          this.maxDelay
        );
      case 'random':
        return Math.floor(Math.random() * this.maxDelay);
      default:
        return this.initialDelay;
    }
  }
  
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

### 5.2 Timeout and Deadletter Handling

```javascript
class TimeoutManager {
  constructor() {
    this.pendingMessages = new Map();
    this.timeoutInterval = 60000;
  }
  
  trackMessage(messageId, timeout, onTimeout) {
    const timeoutId = setTimeout(() => {
      this.pendingMessages.delete(messageId);
      onTimeout(messageId);
    }, timeout);
    
    this.pendingMessages.set(messageId, {
      timeoutId,
      createdAt: Date.now(),
      timeout
    });
  }
  
  clearMessage(messageId) {
    const tracked = this.pendingMessages.get(messageId);
    if (tracked) {
      clearTimeout(tracked.timeoutId);
      this.pendingMessages.delete(messageId);
    }
  }
  
  // Dead letter queue for failed messages
  async sendToDeadLetter(message, reason, error) {
    const deadLetterMessage = {
      ...message,
      originalId: message.id,
      id: `dlq_${message.id}`,
      type: 'DEADLETTER',
      deadLetterReason: reason,
      error: {
        message: error.message,
        stack: error.stack
      },
      retryCount: message.retryCount || 0,
      deadLetteredAt: Date.now()
    };
    
    await this.publishToDeadLetterQueue(deadLetterMessage);
  }
}
```

---

## 6. Message Monitoring and Debugging

### 6.1 Message Tracing

```javascript
class MessageTracer {
  constructor() {
    this.traces = new Map();
  }
  
  startTrace(message) {
    const trace = {
      messageId: message.id,
      correlationId: message.correlationId,
      source: message.source,
      target: message.target,
      startTime: Date.now(),
      events: [{
        type: 'CREATED',
        timestamp: Date.now(),
        agent: message.source
      }]
    };
    
    this.traces.set(message.id, trace);
    return trace;
  }
  
  recordEvent(messageId, event) {
    const trace = this.traces.get(messageId);
    if (trace) {
      trace.events.push({
        ...event,
        timestamp: Date.now()
      });
    }
  }
  
  endTrace(messageId) {
    const trace = this.traces.get(messageId);
    if (trace) {
      trace.endTime = Date.now();
      trace.duration = trace.endTime - trace.startTime;
      return trace;
    }
  }
  
  getTraceReport(messageId) {
    return this.traces.get(messageId);
  }
}
```

### 6.2 Communication Metrics

```javascript
class CommunicationMetrics {
  constructor() {
    this.metrics = {
      messagesSent: 0,
      messagesReceived: 0,
      failedMessages: 0,
      averageLatency: 0,
      latencies: [],
      agentMetrics: new Map()
    };
  }
  
  recordSent(message) {
    this.metrics.messagesSent++;
    this.ensureAgentMetrics(message.source).sent++;
  }
  
  recordReceived(message, latency) {
    this.metrics.messagesReceived++;
    this.metrics.latencies.push(latency);
    this.metrics.averageLatency = this.calculateAverage();
    this.ensureAgentMetrics(message.target).received++;
  }
  
  recordFailure(message) {
    this.metrics.failedMessages++;
    this.ensureAgentMetrics(message.source).failed++;
  }
  
  ensureAgentMetrics(agentId) {
    if (!this.metrics.agentMetrics.has(agentId)) {
      this.metrics.agentMetrics.set(agentId, {
        sent: 0,
        received: 0,
        failed: 0,
        averageLatency: 0
      });
    }
    return this.metrics.agentMetrics.get(agentId);
  }
  
  calculateAverage() {
    if (this.metrics.latencies.length === 0) return 0;
    const sum = this.metrics.latencies.reduce((a, b) => a + b, 0);
    return sum / this.metrics.latencies.length;
  }
  
  getMetrics() {
    return {
      ...this.metrics,
      agentMetrics: Object.fromEntries(this.metrics.agentMetrics)
    };
  }
}
```

---

## 7. Security in Communication

### 7.1 Message Encryption

```javascript
const crypto = require('crypto');

class MessageEncryption {
  constructor(encryptionKey) {
    this.algorithm = 'aes-256-gcm';
    this.encryptionKey = crypto.scryptSync(encryptionKey, 'salt', 32);
  }
  
  encryptMessage(message) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(this.algorithm, this.encryptionKey, iv);
    
    const serialized = JSON.stringify(message);
    let encrypted = cipher.update(serialized, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    const authTag = cipher.getAuthTag();
    
    return {
      iv: iv.toString('hex'),
      encryptedData: encrypted,
      authTag: authTag.toString('hex'),
      algorithm: this.algorithm
    };
  }
  
  decryptMessage(encryptedMessage) {
    const decipher = crypto.createDecipheriv(
      this.algorithm,
      this.encryptionKey,
      Buffer.from(encryptedMessage.iv, 'hex')
    );
    
    decipher.setAuthTag(Buffer.from(encryptedMessage.authTag, 'hex'));
    
    let decrypted = decipher.update(encryptedMessage.encryptedData, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return JSON.parse(decrypted);
  }
}
```

### 7.2 Message Authentication

```javascript
class MessageAuthenticator {
  constructor(privateKey) {
    this.privateKey = privateKey;
  }
  
  signMessage(message) {
    const signer = crypto.createSign('sha256');
    const serialized = JSON.stringify(message, null, 0);
    signer.update(serialized);
    
    const signature = signer.sign(this.privateKey, 'hex');
    
    return {
      ...message,
      signature,
      signedAt: Date.now()
    };
  }
  
  verifyMessage(signedMessage, publicKey) {
    const signature = signedMessage.signature;
    const verifier = crypto.createVerify('sha256');
    
    const messageCopy = { ...signedMessage };
    delete messageCopy.signature;
    delete messageCopy.signedAt;
    
    const serialized = JSON.stringify(messageCopy, null, 0);
    verifier.update(serialized);
    
    return verifier.verify(publicKey, signature, 'hex');
  }
}
```

---

## 8. Best Practices

### Message Design
- Keep messages lightweight and focused
- Use consistent naming conventions
- Include correlation IDs for tracing
- Set appropriate timeout values
- Mark retryable operations clearly

### Protocol Selection
- Use async (RabbitMQ/Kafka) for non-blocking operations
- Use gRPC for latency-sensitive operations
- Consider network topology and latency
- Implement fallback protocols

### Error Handling
- Always include error details in responses
- Implement circuit breaker patterns
- Use exponential backoff for retries
- Monitor dead letter queues

### Monitoring
- Track message latency and throughput
- Monitor queue depths
- Alert on failed messages
- Trace message journeys across agents

### Security
- Encrypt sensitive payloads
- Authenticate and authorize agents
- Use TLS for network communication
- Implement rate limiting

---

## Conclusion

Effective agent communication is critical for system reliability and performance. This document provides comprehensive patterns, protocols, and implementations for building robust multi-agent communication systems.
