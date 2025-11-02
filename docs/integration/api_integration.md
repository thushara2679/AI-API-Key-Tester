# API Integration Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Last Updated:** October 26, 2024
**Document Type:** API Integration Guide
**Focus:** 150+ API integration techniques

---

## 🎯 REST API Integration

### Basic HTTP Client

```typescript
// Fetch API
async function fetchFeatures(): Promise<Feature[]> {
  const response = await fetch('/api/features', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return response.json();
}

// Axios
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.example.com',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

async function fetchFeatures() {
  const { data } = await api.get('/features');
  return data;
}

// HttpClient (Angular)
import { HttpClient } from '@angular/common/http';

@Injectable()
export class FeaturesService {
  constructor(private http: HttpClient) {}

  getFeatures(): Observable<Feature[]> {
    return this.http.get<Feature[]>('/api/features');
  }
}
```

### Request Interceptors

```typescript
// Axios interceptor
api.interceptors.request.use(
  config => {
    // Add auth token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Add request ID for tracing
    config.headers['X-Request-ID'] = generateUUID();
    
    return config;
  },
  error => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  response => response,
  async error => {
    // Refresh token if 401
    if (error.response?.status === 401) {
      const newToken = await refreshToken();
      error.config.headers.Authorization = `Bearer ${newToken}`;
      return api(error.config);
    }
    
    return Promise.reject(error);
  }
);

// Fetch API interceptor pattern
async function fetchWithInterceptor(url: string, options: any = {}) {
  // Request interceptor
  const headers = new Headers(options.headers || {});
  headers.set('Authorization', `Bearer ${getToken()}`);
  headers.set('X-Request-ID', generateUUID());
  
  const response = await fetch(url, { ...options, headers });
  
  // Response interceptor
  if (response.status === 401) {
    const newToken = await refreshToken();
    return fetchWithInterceptor(url, {
      ...options,
      headers: { Authorization: `Bearer ${newToken}` },
    });
  }
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  
  return response.json();
}
```

### Error Handling

```typescript
// Custom error class
class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code: string,
    public details?: any
  ) {
    super(message);
  }
}

// Error handler
async function handleAPIError(error: any): Promise<void> {
  if (error.response) {
    // Server error
    const { status, data } = error.response;
    
    switch (status) {
      case 400:
        throw new APIError('Bad request', 400, 'BAD_REQUEST', data.details);
      case 401:
        throw new APIError('Unauthorized', 401, 'UNAUTHORIZED');
      case 403:
        throw new APIError('Forbidden', 403, 'FORBIDDEN');
      case 404:
        throw new APIError('Not found', 404, 'NOT_FOUND');
      case 429:
        throw new APIError('Too many requests', 429, 'RATE_LIMIT');
      case 500:
        throw new APIError('Server error', 500, 'SERVER_ERROR');
      default:
        throw new APIError('Unknown error', status, 'UNKNOWN');
    }
  } else if (error.request) {
    // No response
    throw new APIError('No response', 0, 'NO_RESPONSE');
  } else {
    // Request setup error
    throw error;
  }
}

// Usage
try {
  const features = await fetchFeatures();
} catch (error) {
  if (error instanceof APIError) {
    console.error(`[${error.code}] ${error.message}`);
    logger.error('API error', { status: error.status, details: error.details });
  } else {
    console.error('Unknown error', error);
  }
}
```

### Request Retry Logic

```typescript
// Exponential backoff retry
async function retryRequest<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) throw error;
      
      // Only retry on specific status codes
      const retryable = [408, 429, 500, 502, 503, 504].includes(
        error.response?.status
      );
      
      if (!retryable) throw error;
      
      // Calculate delay with jitter
      const delay = baseDelay * Math.pow(2, attempt);
      const jitter = Math.random() * delay * 0.1;
      
      await new Promise(resolve => 
        setTimeout(resolve, delay + jitter)
      );
    }
  }
}

// Usage
const features = await retryRequest(() => fetchFeatures());
```

### Batch Requests

```typescript
// Batch multiple requests
async function batchRequests<T>(
  requests: (() => Promise<T>)[]
): Promise<T[]> {
  const BATCH_SIZE = 5;
  const results: T[] = [];
  
  for (let i = 0; i < requests.length; i += BATCH_SIZE) {
    const batch = requests.slice(i, i + BATCH_SIZE);
    const batchResults = await Promise.allSettled(
      batch.map(req => req())
    );
    
    for (const result of batchResults) {
      if (result.status === 'fulfilled') {
        results.push(result.value);
      } else {
        console.error('Request failed:', result.reason);
      }
    }
  }
  
  return results;
}

// GraphQL batching
const batchQuery = gql`
  query GetMultiple($ids: [String!]!) {
    features: featuresByIds(ids: $ids) { id name }
    deployments: deploymentsByIds(ids: $ids) { id status }
    tests: testsByIds(ids: $ids) { id passed }
  }
`;
```

---

## 🔌 GraphQL Integration

### Apollo Client Setup

```typescript
import { ApolloClient, InMemoryCache, HttpLink } from '@apollo/client';

const client = new ApolloClient({
  link: new HttpLink({
    uri: 'https://api.example.com/graphql',
    credentials: 'include',
  }),
  cache: new InMemoryCache(),
});

// Queries
const GET_FEATURES = gql`
  query GetFeatures($first: Int!, $after: String) {
    features(first: $first, after: $after) {
      edges {
        node { id name priority }
        cursor
      }
      pageInfo { hasNextPage endCursor }
    }
  }
`;

// Mutations
const CREATE_FEATURE = gql`
  mutation CreateFeature($input: CreateFeatureInput!) {
    createFeature(input: $input) {
      feature { id name }
      errors { field message }
    }
  }
`;

// React hook
function useFeatures() {
  const { data, loading, error, fetchMore } = useQuery(GET_FEATURES, {
    variables: { first: 20 },
  });

  return {
    features: data?.features?.edges.map(e => e.node),
    loading,
    error,
    hasMore: data?.features?.pageInfo.hasNextPage,
    loadMore: () => fetchMore({
      variables: {
        after: data?.features?.pageInfo.endCursor,
      },
    }),
  };
}
```

---

## 🔐 Authentication

### Token Management

```typescript
// JWT token storage
class TokenManager {
  private readonly STORAGE_KEY = 'auth_token';
  private readonly REFRESH_KEY = 'refresh_token';

  setTokens(accessToken: string, refreshToken: string): void {
    localStorage.setItem(this.STORAGE_KEY, accessToken);
    localStorage.setItem(this.REFRESH_KEY, refreshToken);
  }

  getAccessToken(): string | null {
    return localStorage.getItem(this.STORAGE_KEY);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_KEY);
  }

  clearTokens(): void {
    localStorage.removeItem(this.STORAGE_KEY);
    localStorage.removeItem(this.REFRESH_KEY);
  }

  isTokenExpired(token: string): boolean {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.exp * 1000 < Date.now();
  }
}

// OAuth 2.0 flow
async function loginWithOAuth(provider: 'google' | 'github'): Promise<void> {
  const clientId = process.env.REACT_APP_OAUTH_CLIENT_ID;
  const redirectUri = `${window.location.origin}/auth/callback`;
  
  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    response_type: 'code',
    scope: 'openid profile email',
  });

  window.location.href = `https://${provider}.com/oauth/authorize?${params}`;
}

// Handle callback
async function handleOAuthCallback(code: string): Promise<void> {
  const response = await fetch('/api/auth/callback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code }),
  });

  const { accessToken, refreshToken } = await response.json();
  tokenManager.setTokens(accessToken, refreshToken);
}
```

### API Key Management

```typescript
// API key rotation
class APIKeyManager {
  private keys: Map<string, { key: string; rotatedAt: Date }> = new Map();

  async rotateKey(serviceName: string): Promise<string> {
    const response = await fetch(`/api/keys/${serviceName}/rotate`, {
      method: 'POST',
    });

    const { key } = await response.json();
    this.keys.set(serviceName, { key, rotatedAt: new Date() });

    return key;
  }

  getKey(serviceName: string): string | undefined {
    return this.keys.get(serviceName)?.key;
  }

  shouldRotate(serviceName: string): boolean {
    const stored = this.keys.get(serviceName);
    if (!stored) return true;

    // Rotate if older than 30 days
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    return stored.rotatedAt < thirtyDaysAgo;
  }
}
```

---

## 🔄 Pagination

### Cursor-based Pagination

```typescript
interface PaginationCursor {
  cursor: string | null;
  limit: number;
}

async function fetchWithCursor(
  url: string,
  cursor: PaginationCursor
): Promise<{ items: any[]; nextCursor: string | null }> {
  const params = new URLSearchParams({
    limit: cursor.limit.toString(),
  });

  if (cursor.cursor) {
    params.append('cursor', cursor.cursor);
  }

  const response = await fetch(`${url}?${params}`);
  const data = await response.json();

  return {
    items: data.items,
    nextCursor: data.pageInfo?.endCursor || null,
  };
}

// Infinite scroll implementation
async function* paginate(
  url: string,
  pageSize: number = 20
): AsyncGenerator<any[]> {
  let cursor: string | null = null;

  while (true) {
    const { items, nextCursor } = await fetchWithCursor(url, {
      cursor,
      limit: pageSize,
    });

    yield items;

    if (!nextCursor) break;
    cursor = nextCursor;
  }
}

// Usage
for await (const items of paginate('/api/features')) {
  console.log('Loaded items:', items);
}
```

### Offset-based Pagination

```typescript
async function fetchPage(
  url: string,
  page: number,
  pageSize: number = 20
): Promise<{ items: any[]; total: number; pages: number }> {
  const offset = (page - 1) * pageSize;

  const response = await fetch(
    `${url}?offset=${offset}&limit=${pageSize}`
  );
  const data = await response.json();

  return {
    items: data.items,
    total: data.total,
    pages: Math.ceil(data.total / pageSize),
  };
}
```

---

## 📊 Rate Limiting

```typescript
class RateLimiter {
  private requests: Map<string, number[]> = new Map();
  private readonly limit: number;
  private readonly windowMs: number;

  constructor(limit: number = 100, windowMs: number = 60000) {
    this.limit = limit;
    this.windowMs = windowMs;
  }

  async checkLimit(key: string): Promise<{ allowed: boolean; remaining: number }> {
    const now = Date.now();
    const timestamps = this.requests.get(key) || [];

    // Remove old requests outside window
    const recent = timestamps.filter(ts => now - ts < this.windowMs);

    if (recent.length >= this.limit) {
      return { allowed: false, remaining: 0 };
    }

    recent.push(now);
    this.requests.set(key, recent);

    return { allowed: true, remaining: this.limit - recent.length };
  }
}

// Usage in API client
const limiter = new RateLimiter(100, 60000); // 100 per minute

async function apiCall(endpoint: string) {
  const { allowed, remaining } = await limiter.checkLimit('api');

  if (!allowed) {
    throw new Error('Rate limit exceeded');
  }

  console.log(`Requests remaining: ${remaining}`);
  return fetch(endpoint);
}
```

---

## 🔄 Webhook Handling

```typescript
// Express webhook handler
app.post('/webhooks/features', express.json(), async (req, res) => {
  const signature = req.headers['x-webhook-signature'];
  const timestamp = req.headers['x-webhook-timestamp'];

  // Verify signature
  const isValid = verifyWebhookSignature(
    req.body,
    signature,
    timestamp,
    process.env.WEBHOOK_SECRET
  );

  if (!isValid) {
    return res.status(401).json({ error: 'Invalid signature' });
  }

  try {
    const { event, data } = req.body;

    switch (event) {
      case 'feature.created':
        await handleFeatureCreated(data);
        break;
      case 'feature.updated':
        await handleFeatureUpdated(data);
        break;
      case 'feature.deleted':
        await handleFeatureDeleted(data);
        break;
    }

    res.json({ success: true });
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).json({ error: 'Processing failed' });
  }
});

function verifyWebhookSignature(
  body: any,
  signature: string,
  timestamp: string,
  secret: string
): boolean {
  const message = `${timestamp}.${JSON.stringify(body)}`;
  const hash = crypto
    .createHmac('sha256', secret)
    .update(message)
    .digest('hex');

  return crypto.timingSafeEqual(hash, signature);
}
```

---

## 📚 Related Documents

- Backend-Frontend Integration (backend_frontend.md)
- Database Integration (database_integration.md)
- Real-time Communication (real_time_communication.md)

---

**END OF API INTEGRATION DOCUMENT**
