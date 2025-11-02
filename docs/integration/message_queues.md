# Message Queues Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Message Queue Patterns Guide
**Focus:** 150+ message queue techniques

---

## 🔄 Message Queue Patterns

### Producer Pattern

```typescript
// Kafka producer
import { Kafka } from 'kafkajs';

const kafka = new Kafka({
  clientId: 'app',
  brokers: ['localhost:9092']
});

const producer = kafka.producer({
  idempotent: true,
  maxInFlightRequests: 5,
  compression: 1 // Gzip
});

await producer.connect();

// Single message
await producer.send({
  topic: 'features',
  messages: [
    {
      key: 'feature-1',
      value: JSON.stringify({ id: '1', name: 'OAuth' }),
      headers: { 'content-type': 'application/json' }
    }
  ]
});

// Batch messages
await producer.sendBatch({
  topicMessages: [
    {
      topic: 'features',
      messages: [
        { key: '1', value: 'Feature 1' },
        { key: '2', value: 'Feature 2' }
      ]
    },
    {
      topic: 'deployments',
      messages: [
        { key: 'd1', value: 'Deployment 1' }
      ]
    }
  ]
});

// Partitioned messages
await producer.send({
  topic: 'features',
  messages: [
    {
      key: 'feature-1',
      value: JSON.stringify({ id: '1' }),
      partition: 0 // Send to specific partition
    }
  ]
});
```

### Consumer Pattern

```typescript
// Kafka consumer
const consumer = kafka.consumer({
  groupId: 'feature-service',
  allowAutoTopicCreation: false
});

await consumer.connect();

// Subscribe to topic
await consumer.subscribe({
  topic: 'features',
  fromBeginning: false,
  options: { sessionTimeout: 30000 }
});

// Consume messages
await consumer.run({
  eachMessage: async ({ topic, partition, message }) => {
    try {
      const data = JSON.parse(message.value.toString());
      
      logger.info(`Processing message from ${topic}`, {
        partition,
        offset: message.offset,
        data
      });

      await handleFeatureEvent(data);

      // Offset is committed automatically
    } catch (error) {
      logger.error('Message processing error', error);
      
      // Dead letter queue
      await producer.send({
        topic: 'features.dead-letter',
        messages: [{
          value: message.value,
          headers: {
            'error': error.message,
            'original-topic': topic
          }
        }]
      });
    }
  }
});

// Consumer groups
await consumer.subscribe({
  topics: ['features', 'deployments'],
  groupId: 'feature-service'
});

// Manual offset management
await consumer.run({
  eachMessage: async ({ message }) => {
    await processMessage(message);
  },
  partitionsConsumedConcurrently: 3
});
```

---

## 🚀 RabbitMQ Patterns

### Publisher-Subscriber

```typescript
import amqplib from 'amqplib';

// Publisher
async function publishEvent(exchangeName: string, routingKey: string, message: any) {
  const connection = await amqplib.connect('amqp://localhost');
  const channel = await connection.createChannel();

  await channel.assertExchange(exchangeName, 'topic', { durable: true });

  channel.publish(
    exchangeName,
    routingKey,
    Buffer.from(JSON.stringify(message))
  );

  await channel.close();
  await connection.close();
}

// Subscriber
async function subscribeToEvents(exchangeName: string, pattern: string) {
  const connection = await amqplib.connect('amqp://localhost');
  const channel = await connection.createChannel();

  await channel.assertExchange(exchangeName, 'topic', { durable: true });

  const queue = await channel.assertQueue('', { exclusive: true });
  await channel.bindQueue(queue.queue, exchangeName, pattern);

  channel.consume(queue.queue, (msg) => {
    if (msg) {
      const data = JSON.parse(msg.content.toString());
      handleEvent(data);
      channel.ack(msg);
    }
  });
}

// Usage
await publishEvent('features', 'feature.created', { id: '1', name: 'OAuth' });
await subscribeToEvents('features', 'feature.*');
```

### Work Queue

```typescript
// Producer (task)
async function addTask(taskQueue: string, taskData: any) {
  const connection = await amqplib.connect('amqp://localhost');
  const channel = await connection.createChannel();

  await channel.assertQueue(taskQueue, { durable: true });

  channel.sendToQueue(
    taskQueue,
    Buffer.from(JSON.stringify(taskData)),
    { persistent: true }
  );

  await channel.close();
  await connection.close();
}

// Consumer (worker)
async function startWorker(taskQueue: string) {
  const connection = await amqplib.connect('amqp://localhost');
  const channel = await connection.createChannel();

  await channel.assertQueue(taskQueue, { durable: true });
  channel.prefetch(1); // Process one message at a time

  channel.consume(taskQueue, async (msg) => {
    if (msg) {
      const task = JSON.parse(msg.content.toString());

      try {
        logger.info(`Processing task: ${task.id}`);
        await processTask(task);
        channel.ack(msg);
      } catch (error) {
        logger.error(`Task failed: ${task.id}`, error);
        
        // Requeue or send to dead letter
        channel.nack(msg, false, true);
      }
    }
  });
}

// Usage
await addTask('build-queue', { buildId: 'b1', features: ['f1', 'f2'] });
await startWorker('build-queue');
```

---

## 🔄 RPC Pattern

### Request-Reply

```typescript
// RPC Server
async function startRPCServer(rpcQueue: string) {
  const connection = await amqplib.connect('amqp://localhost');
  const channel = await connection.createChannel();

  await channel.assertQueue(rpcQueue, { durable: true });

  channel.consume(rpcQueue, async (msg) => {
    if (msg) {
      const request = JSON.parse(msg.content.toString());

      try {
        const result = await handleRPCRequest(request);

        channel.sendToQueue(
          msg.properties.replyTo,
          Buffer.from(JSON.stringify({ success: true, result })),
          { correlationId: msg.properties.correlationId }
        );
      } catch (error) {
        channel.sendToQueue(
          msg.properties.replyTo,
          Buffer.from(JSON.stringify({ success: false, error: error.message })),
          { correlationId: msg.properties.correlationId }
        );
      }

      channel.ack(msg);
    }
  });
}

// RPC Client
async function callRPC(rpcQueue: string, request: any): Promise<any> {
  const connection = await amqplib.connect('amqp://localhost');
  const channel = await connection.createChannel();

  const replyQueue = await channel.assertQueue('', { exclusive: true });
  const correlationId = generateUUID();

  const result = await new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      reject(new Error('RPC timeout'));
      channel.cancel(consumerTag);
    }, 10000);

    channel.consume(replyQueue.queue, (msg) => {
      if (msg?.properties.correlationId === correlationId) {
        clearTimeout(timeout);
        const response = JSON.parse(msg.content.toString());
        resolve(response);
      }
    }, { noAck: true });

    channel.sendToQueue(
      rpcQueue,
      Buffer.from(JSON.stringify(request)),
      {
        replyTo: replyQueue.queue,
        correlationId
      }
    );
  });

  await channel.close();
  await connection.close();

  return result;
}
```

---

## 📊 Dead Letter Handling

```typescript
// Setup dead letter exchange
async function setupDLQ(channel: any, originalQueue: string) {
  const dlxExchange = `${originalQueue}.dlx`;
  const dlQueue = `${originalQueue}.dl`;

  // Create DLX
  await channel.assertExchange(dlxExchange, 'direct', { durable: true });
  
  // Create DL queue
  const dlq = await channel.assertQueue(dlQueue, { durable: true });
  await channel.bindQueue(dlQueue, dlxExchange, originalQueue);

  // Bind original queue to DLX
  await channel.assertQueue(originalQueue, {
    durable: true,
    arguments: {
      'x-dead-letter-exchange': dlxExchange,
      'x-dead-letter-routing-key': originalQueue,
      'x-message-ttl': 86400000 // 24 hours
    }
  });

  return { dlxExchange, dlQueue };
}

// Process dead letters
async function processDeadLetters(dlQueue: string) {
  const connection = await amqplib.connect('amqp://localhost');
  const channel = await connection.createChannel();

  channel.consume(dlQueue, async (msg) => {
    if (msg) {
      const failedMessage = JSON.parse(msg.content.toString());

      logger.error('Processing dead letter', {
        message: failedMessage,
        headers: msg.properties.headers
      });

      // Store for manual review
      await storeFailedMessage(failedMessage);

      channel.ack(msg);
    }
  });
}
```

---

## ⏱️ Scheduled Messages

```typescript
// Delayed message
async function scheduleMessage(
  topic: string,
  message: any,
  delayMs: number
) {
  await producer.send({
    topic,
    messages: [
      {
        value: JSON.stringify(message),
        headers: {
          'x-scheduled-time': (Date.now() + delayMs).toString()
        }
      }
    ]
  });
}

// Message scheduler consumer
async function startScheduler() {
  await consumer.subscribe({ topic: 'scheduled-messages' });

  await consumer.run({
    eachMessage: async ({ message }) => {
      const scheduledTime = parseInt(
        message.headers['x-scheduled-time'].toString()
      );

      if (Date.now() < scheduledTime) {
        // Not ready yet, requeue
        await producer.send({
          topic: 'scheduled-messages',
          messages: [{ value: message.value, headers: message.headers }]
        });
      } else {
        // Process now
        const data = JSON.parse(message.value.toString());
        await processScheduledMessage(data);
      }
    }
  });
}
```

---

## 🔄 Circuit Breaker for Queues

```typescript
class QueueCircuitBreaker {
  private failureCount = 0;
  private lastFailureTime: number | null = null;
  private state: 'closed' | 'open' | 'half-open' = 'closed';

  constructor(
    private failureThreshold: number = 5,
    private resetTimeout: number = 60000
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      if (Date.now() - this.lastFailureTime! > this.resetTimeout) {
        this.state = 'half-open';
      } else {
        throw new Error('Circuit breaker is open');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failureCount = 0;
    this.state = 'closed';
  }

  private onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();

    if (this.failureCount >= this.failureThreshold) {
      this.state = 'open';
      logger.warn('Circuit breaker opened');
    }
  }
}

// Usage
const breaker = new QueueCircuitBreaker();

async function sendWithCircuitBreaker(message: any) {
  return breaker.execute(() => producer.send({
    topic: 'events',
    messages: [{ value: JSON.stringify(message) }]
  }));
}
```

---

## 📊 Monitoring

```typescript
// Message lag monitoring
async function monitorLag(consumerGroup: string) {
  const admin = kafka.admin();
  await admin.connect();

  const groupOffsets = await admin.fetchOffsets(consumerGroup);

  for (const { topic, partition, offset } of groupOffsets) {
    const { topicOffsets } = await admin.fetchTopicOffsets(topic);
    const latestOffset = topicOffsets[partition][0];

    const lag = latestOffset - offset;
    console.log(`Topic: ${topic}, Partition: ${partition}, Lag: ${lag}`);
  }

  await admin.disconnect();
}

// Message metrics
class QueueMetrics {
  private metrics = {
    messagesProduced: 0,
    messagesConsumed: 0,
    messagesFailed: 0,
    avgProcessingTime: 0,
  };

  recordProduced() {
    this.metrics.messagesProduced++;
  }

  recordConsumed(processingTime: number) {
    this.metrics.messagesConsumed++;
    this.metrics.avgProcessingTime = (
      this.metrics.avgProcessingTime * (this.metrics.messagesConsumed - 1) +
      processingTime
    ) / this.metrics.messagesConsumed;
  }

  recordFailed() {
    this.metrics.messagesFailed++;
  }

  getMetrics() {
    return { ...this.metrics };
  }
}
```

---

## 📚 Related Documents

- API Integration (api_integration.md)
- Backend-Frontend Integration (backend_frontend.md)
- Real-time Communication (real_time_communication.md)

---

**END OF MESSAGE QUEUES DOCUMENT**
