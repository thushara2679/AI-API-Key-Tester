# Real-time Communication Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Real-time Communication Guide
**Focus:** WebSocket & SSE patterns (200+ techniques)

---

## 🔌 WebSocket

### Server Setup

```typescript
// Express + Socket.io
import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: { origin: '*' },
  pingInterval: 25000,
  pingTimeout: 20000,
  transports: ['websocket', 'polling'],
});

httpServer.listen(3000);

// Connection handler
io.on('connection', (socket) => {
  console.log(`Client connected: ${socket.id}`);

  // Join room
  socket.on('join:room', (roomId) => {
    socket.join(roomId);
    socket.broadcast.to(roomId).emit('user:joined', socket.id);
  });

  // Message handler
  socket.on('message', (data) => {
    io.to(data.roomId).emit('message:new', {
      from: socket.id,
      message: data.message,
      timestamp: new Date()
    });
  });

  // Disconnect
  socket.on('disconnect', () => {
    console.log(`Client disconnected: ${socket.id}`);
  });
});
```

### Client Setup

```typescript
// React component
import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

function ChatRoom({ roomId }: { roomId: string }) {
  const [messages, setMessages] = useState<any[]>([]);
  const [socket, setSocket] = useState<any>(null);

  useEffect(() => {
    const newSocket = io('http://localhost:3000', {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5,
    });

    newSocket.on('connect', () => {
      console.log('Connected');
      newSocket.emit('join:room', roomId);
    });

    newSocket.on('message:new', (data) => {
      setMessages(prev => [...prev, data]);
    });

    setSocket(newSocket);

    return () => newSocket.close();
  }, [roomId]);

  const sendMessage = (message: string) => {
    socket?.emit('message', { roomId, message });
  };

  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i}>{msg.message}</div>
      ))}
      <input onKeyPress={(e) => {
        if (e.key === 'Enter') {
          sendMessage(e.currentTarget.value);
          e.currentTarget.value = '';
        }
      }} />
    </div>
  );
}
```

### Broadcasting

```typescript
// Broadcast to all clients
io.emit('notification', { message: 'Server update' });

// Broadcast to room
io.to('room1').emit('room:update', data);

// Broadcast except sender
socket.broadcast.emit('user:connected', socket.id);

// Targeted message
io.to(userId).emit('direct:message', message);

// Rooms and namespaces
io.of('/admin').to('room1').emit('admin:notification', data);
```

### Advanced Patterns

```typescript
// Acknowledgment
socket.emit('request', (response) => {
  console.log('Response:', response);
});

socket.on('request', (data, callback) => {
  callback({ status: 'received' });
});

// Binary data
socket.emit('binary', Buffer.from('hello'));

socket.on('binary', (data) => {
  console.log('Received binary:', data);
});

// Middleware
io.use((socket, next) => {
  const token = socket.handshake.auth.token;
  
  if (!token) {
    return next(new Error('Authentication error'));
  }

  try {
    const user = verifyToken(token);
    socket.userId = user.id;
    next();
  } catch (error) {
    next(error);
  }
});

// Error handling
socket.on('error', (error) => {
  console.error('Socket error:', error);
});

socket.on_error_default((error) => {
  console.error('Default error handler:', error);
});
```

---

## 📡 Server-Sent Events (SSE)

### Server Setup

```typescript
// Express SSE endpoint
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.setHeader('Access-Control-Allow-Origin', '*');

  // Send keep-alive ping every 30s
  const keepAlive = setInterval(() => {
    res.write(': keep-alive\n\n');
  }, 30000);

  // Send deployment status updates
  const deployment = startDeployment();

  deployment.on('status', (status) => {
    res.write(`data: ${JSON.stringify(status)}\n\n`);
  });

  deployment.on('error', (error) => {
    res.write(`event: error\n`);
    res.write(`data: ${JSON.stringify(error)}\n\n`);
  });

  deployment.on('complete', (result) => {
    res.write(`event: complete\n`);
    res.write(`data: ${JSON.stringify(result)}\n\n`);
    res.end();
  });

  // Cleanup
  req.on('close', () => {
    clearInterval(keepAlive);
    deployment.cancel();
  });
});
```

### Client Setup

```typescript
// Vanilla JavaScript
const eventSource = new EventSource('/events');

eventSource.addEventListener('open', () => {
  console.log('Connection opened');
});

eventSource.addEventListener('message', (event) => {
  const data = JSON.parse(event.data);
  console.log('Update:', data);
});

eventSource.addEventListener('error', (event) => {
  const error = JSON.parse(event.data);
  console.error('Error:', error);
});

eventSource.addEventListener('complete', (event) => {
  console.log('Deployment complete');
  eventSource.close();
});

// React hook
function useSSE<T>(url: string): T | null {
  const [data, setData] = useState<T | null>(null);

  useEffect(() => {
    const eventSource = new EventSource(url);

    eventSource.addEventListener('message', (event) => {
      setData(JSON.parse(event.data));
    });

    eventSource.addEventListener('error', () => {
      eventSource.close();
    });

    return () => eventSource.close();
  }, [url]);

  return data;
}
```

---

## 🔄 Reconnection Strategies

### Exponential Backoff

```typescript
class ReconnectingWebSocket {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;
  private baseDelay = 1000;
  private maxDelay = 30000;

  constructor(private url: string) {
    this.connect();
  }

  private connect() {
    this.ws = new WebSocket(this.url);

    this.ws.addEventListener('open', () => {
      this.reconnectAttempts = 0;
      this.onOpen?.();
    });

    this.ws.addEventListener('message', (event) => {
      this.onMessage?.(event.data);
    });

    this.ws.addEventListener('close', () => {
      this.scheduleReconnect();
    });

    this.ws.addEventListener('error', (event) => {
      this.onError?.(event);
    });
  }

  private scheduleReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      this.onFatalError?.();
      return;
    }

    const delay = Math.min(
      this.baseDelay * Math.pow(2, this.reconnectAttempts),
      this.maxDelay
    ) + Math.random() * 1000;

    this.reconnectAttempts++;
    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);

    setTimeout(() => this.connect(), delay);
  }

  send(data: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  close() {
    this.ws?.close();
  }

  onOpen?: () => void;
  onMessage?: (data: string) => void;
  onError?: (event: Event) => void;
  onFatalError?: () => void;
}
```

---

## 🎯 Message Patterns

### Request-Response

```typescript
// Server
socket.on('request:deploy', async (data, callback) => {
  try {
    const result = await deployFeature(data);
    callback({ success: true, result });
  } catch (error) {
    callback({ success: false, error: error.message });
  }
});

// Client
socket.emit('request:deploy', { featureId: '1' }, (response) => {
  if (response.success) {
    console.log('Deployment started:', response.result);
  } else {
    console.error('Deployment failed:', response.error);
  }
});
```

### Pub-Sub Pattern

```typescript
class PubSubManager {
  private subscribers: Map<string, Set<Function>> = new Map();

  subscribe(topic: string, handler: Function): () => void {
    if (!this.subscribers.has(topic)) {
      this.subscribers.set(topic, new Set());
    }

    this.subscribers.get(topic)!.add(handler);

    // Return unsubscribe function
    return () => {
      this.subscribers.get(topic)?.delete(handler);
    };
  }

  publish(topic: string, data: any) {
    this.subscribers.get(topic)?.forEach(handler => {
      try {
        handler(data);
      } catch (error) {
        console.error('Handler error:', error);
      }
    });
  }

  async publishAsync(topic: string, data: any) {
    const handlers = Array.from(this.subscribers.get(topic) || []);
    
    await Promise.all(
      handlers.map(handler =>
        Promise.resolve(handler(data)).catch(error =>
          console.error('Handler error:', error)
        )
      )
    );
  }
}
```

---

## 🔐 Authentication & Security

### Token-based Auth

```typescript
// Server
io.use((socket, next) => {
  const token = socket.handshake.auth.token;

  try {
    const user = jwt.verify(token, process.env.JWT_SECRET);
    socket.userId = user.id;
    socket.userRole = user.role;
    next();
  } catch (error) {
    next(new Error('Authentication failed'));
  }
});

// Client
const socket = io('http://localhost:3000', {
  auth: {
    token: localStorage.getItem('token')
  }
});

// Re-authenticate on token refresh
socket.on('connect_error', async (error) => {
  if (error.message === 'Authentication failed') {
    const newToken = await refreshToken();
    localStorage.setItem('token', newToken);
    socket.auth.token = newToken;
    socket.connect();
  }
});
```

### Message Encryption

```typescript
import { encrypt, decrypt } from 'tweetnacl-util';

class EncryptedSocket {
  constructor(private socket: Socket, private publicKey: string) {
    this.socket.on('message', (data) => {
      const decrypted = decrypt(data.encrypted, this.publicKey);
      this.onMessage?.(JSON.parse(Buffer.from(decrypted).toString()));
    });
  }

  send(data: any) {
    const encrypted = encrypt(JSON.stringify(data), this.publicKey);
    this.socket.emit('message', { encrypted });
  }

  onMessage?: (data: any) => void;
}
```

---

## 📊 Monitoring & Metrics

### Connection Metrics

```typescript
class MetricsCollector {
  private metrics = {
    connections: 0,
    disconnections: 0,
    messagesSent: 0,
    messagesReceived: 0,
    errors: 0,
    avgLatency: 0,
  };

  onConnect() {
    this.metrics.connections++;
  }

  onDisconnect() {
    this.metrics.disconnections++;
  }

  onMessageSent() {
    this.metrics.messagesSent++;
  }

  onMessageReceived() {
    this.metrics.messagesReceived++;
  }

  recordLatency(latency: number) {
    this.metrics.avgLatency = (
      this.metrics.avgLatency * (this.metrics.messagesSent - 1) +
      latency
    ) / this.metrics.messagesSent;
  }

  getMetrics() {
    return { ...this.metrics };
  }
}

// Server metrics
app.get('/metrics', (req, res) => {
  res.json({
    connectedClients: io.engine.clientsCount,
    metrics: collector.getMetrics()
  });
});
```

---

## 📚 Related Documents

- API Integration (api_integration.md)
- Backend-Frontend Integration (backend_frontend.md)
- Message Queues (message_queues.md)

---

**END OF REAL-TIME COMMUNICATION DOCUMENT**
