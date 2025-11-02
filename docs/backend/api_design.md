# API Design Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Last Updated:** October 26, 2024
**Document Type:** API Design Guide
**API Style:** REST + GraphQL

---

## 🎯 API Design Principles

1. **RESTful Architecture** - Standard HTTP methods and status codes
2. **Resource-Oriented** - URIs represent resources, not actions
3. **Stateless** - Each request contains all information needed
4. **Cacheable** - Responses designed for caching where appropriate
5. **Versioning** - API versions in URL path
6. **Documentation** - OpenAPI/Swagger specification
7. **Consistency** - Uniform response formats
8. **Security** - Authentication on all endpoints

---

## 🔗 REST API Design

### Resource Naming Conventions

```yaml
# Good REST URLs
GET    /api/v1/projects                          # List projects
POST   /api/v1/projects                          # Create project
GET    /api/v1/projects/{projectId}              # Get project
PATCH  /api/v1/projects/{projectId}              # Update project
DELETE /api/v1/projects/{projectId}              # Delete project

GET    /api/v1/projects/{projectId}/features     # List features in project
POST   /api/v1/projects/{projectId}/features     # Create feature
GET    /api/v1/projects/{projectId}/features/{featureId}  # Get feature
PATCH  /api/v1/projects/{projectId}/features/{featureId}  # Update feature

GET    /api/v1/deployments?environment=production&status=success  # Filter

# Bad REST URLs (action-based, not resource-based)
GET    /api/v1/getProjects              # ❌ Don't do this
POST   /api/v1/createProject            # ❌ Use POST to /projects instead
GET    /api/v1/getFeaturesByProject     # ❌ Use GET /projects/{id}/features
```

### Request/Response Examples

```json
// POST /api/v1/features - Create Feature
Request:
{
  "name": "OAuth Integration",
  "description": "Implement OAuth 2.0 authentication",
  "complexity_points": 8,
  "requirements": {
    "authentication": "OAuth 2.0",
    "protocols": ["http/2", "tls1.3"]
  }
}

Response (201 Created):
{
  "id": "feat-uuid-123",
  "name": "OAuth Integration",
  "description": "Implement OAuth 2.0 authentication",
  "complexity_points": 8,
  "status": "not_started",
  "created_at": "2024-10-26T10:30:00Z",
  "created_by": "user-uuid-1",
  "_links": {
    "self": { "href": "/api/v1/features/feat-uuid-123" },
    "update": { "href": "/api/v1/features/feat-uuid-123", "method": "PATCH" },
    "delete": { "href": "/api/v1/features/feat-uuid-123", "method": "DELETE" }
  }
}

// GET /api/v1/features?page=1&page_size=20&status=in_progress
Response (200 OK):
{
  "data": [
    {
      "id": "feat-1",
      "name": "Feature 1",
      "status": "in_progress"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 150,
    "pages": 8,
    "has_next": true,
    "has_prev": false
  },
  "_links": {
    "self": { "href": "/api/v1/features?page=1" },
    "next": { "href": "/api/v1/features?page=2" },
    "last": { "href": "/api/v1/features?page=8" }
  }
}

// PATCH /api/v1/features/feat-1 - Partial Update
Request:
{
  "status": "completed",
  "complexity_points": 13
}

Response (200 OK):
{
  "id": "feat-1",
  "name": "Feature 1",
  "status": "completed",
  "complexity_points": 13,
  "updated_at": "2024-10-26T11:00:00Z"
}

// Error Response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request",
    "details": [
      {
        "field": "complexity_points",
        "message": "Must be between 1 and 13"
      }
    ]
  },
  "status": 400,
  "timestamp": "2024-10-26T10:30:00Z",
  "request_id": "req-uuid-123"
}
```

---

## 📊 Query Parameter Patterns

### Filtering

```yaml
# Simple filters
GET /api/v1/features?status=in_progress
GET /api/v1/features?priority=high&environment=production

# Complex filters
GET /api/v1/features?filter=status:in_progress,priority:high
GET /api/v1/features?complexity__gte=5&complexity__lte=10

# Free-text search
GET /api/v1/features?search=oauth&search_fields=name,description
```

### Sorting

```yaml
GET /api/v1/features?sort=created_at:desc,name:asc
GET /api/v1/features?sort=-created_at,+name  # Alternative syntax
```

### Pagination

```yaml
# Offset-based (good for database)
GET /api/v1/features?page=1&page_size=20
GET /api/v1/features?offset=0&limit=20

# Cursor-based (good for large datasets)
GET /api/v1/features?cursor=abc123&page_size=20
```

### Field Selection

```yaml
# Return only specified fields
GET /api/v1/features?fields=id,name,status
GET /api/v1/features?exclude_fields=description,logs

# Sparse fieldsets
GET /api/v1/deployments?include=build,tests
```

---

## 🔀 GraphQL Alternative

```graphql
# query.graphql
query GetFeatures($first: Int!, $after: String, $filter: FeatureFilter) {
  features(first: $first, after: $after, filter: $filter) {
    edges {
      node {
        id
        name
        complexityPoints
        status
        createdAt
        testCases(first: 5) {
          edges {
            node {
              id
              name
              type
            }
          }
        }
      }
      cursor
    }
    pageInfo {
      hasNextPage
      endCursor
    }
    totalCount
  }
}

# Variables
{
  "first": 20,
  "filter": {
    "status": "IN_PROGRESS"
    "complexityPoints": { "gte": 5, "lte": 13 }
  }
}

# Mutation
mutation CreateFeature($input: CreateFeatureInput!) {
  createFeature(input: $input) {
    feature {
      id
      name
      complexity Points
    }
    errors {
      field
      message
    }
  }
}
```

---

## 🔄 Pagination Patterns

### Offset-Based Pagination

```python
# Backend implementation
@app.get("/api/v1/features")
async def list_features(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    # Calculate offset
    offset = (page - 1) * page_size
    
    # Get total
    total = await db.scalar(select(func.count(Feature.id)))
    
    # Get page
    features = await db.execute(
        select(Feature)
        .offset(offset)
        .limit(page_size)
        .order_by(Feature.created_at.desc())
    )
    
    return {
        "data": features.scalars().all(),
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "pages": (total + page_size - 1) // page_size
        }
    }
```

### Cursor-Based Pagination

```python
# Better for real-time data and large datasets
import base64

def encode_cursor(feature_id: str, timestamp: datetime) -> str:
    """Encode cursor for pagination"""
    cursor_str = f"{timestamp.isoformat()}:{feature_id}"
    return base64.b64encode(cursor_str.encode()).decode()

def decode_cursor(cursor: str) -> tuple[datetime, str]:
    """Decode cursor"""
    cursor_str = base64.b64decode(cursor.encode()).decode()
    timestamp_str, feature_id = cursor_str.split(":")
    return datetime.fromisoformat(timestamp_str), feature_id

@app.get("/api/v1/features")
async def list_features_cursor(
    first: int = Query(20, ge=1, le=100),
    after: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(Feature).order_by(Feature.created_at.desc())
    
    if after:
        timestamp, feature_id = decode_cursor(after)
        query = query.where(Feature.created_at < timestamp)
    
    # Fetch one extra to know if there's a next page
    features = (await db.execute(query.limit(first + 1))).scalars().all()
    
    has_next = len(features) > first
    edges = features[:first]
    
    return {
        "edges": [
            {
                "node": f.to_dict(),
                "cursor": encode_cursor(f.id, f.created_at)
            }
            for f in edges
        ],
        "pageInfo": {
            "hasNextPage": has_next,
            "endCursor": encode_cursor(edges[-1].id, edges[-1].created_at) if edges else None
        }
    }
```

---

## 🔐 API Security

### API Key Management

```python
# Generate API key
import secrets

def generate_api_key() -> str:
    return f"sk-{secrets.token_urlsafe(32)}"

# Store hashed key
import hashlib

def hash_api_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()

# Validate API key
@app.middleware("http")
async def api_key_middleware(request: Request, call_next):
    if request.url.path.startswith("/api/v1"):
        api_key = request.headers.get("X-API-Key")
        
        if not api_key:
            return JSONResponse({"error": "Missing API key"}, status_code=401)
        
        # Verify key
        hashed = hash_api_key(api_key)
        user = await db.execute(
            select(User).where(User.api_key_hash == hashed)
        )
        
        if not user:
            return JSONResponse({"error": "Invalid API key"}, status_code=401)
        
        request.state.user = user
    
    return await call_next(request)
```

### Rate Limiting by Tier

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Different limits by tier
RATE_LIMITS = {
    "free": "100/minute",
    "pro": "1000/minute",
    "enterprise": "unlimited"
}

@app.get("/api/v1/features")
@limiter.limit(RATE_LIMITS["pro"])
async def list_features(request: Request):
    # Get user tier from JWT
    tier = request.state.user.get("tier", "free")
    # Limiter automatically applies correct limit
    pass
```

---

## 🔗 Webhooks

### Webhook Configuration

```python
# Register webhook
@app.post("/api/v1/webhooks")
async def register_webhook(
    webhook: WebhookCreate,
    user: User = Depends(get_current_user)
):
    # Validate URL
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(webhook.url, timeout=5)
    except:
        raise HTTPException(400, "Invalid webhook URL")
    
    # Store webhook
    db_webhook = Webhook(
        url=webhook.url,
        events=webhook.events,
        user_id=user.id
    )
    db.add(db_webhook)
    await db.commit()
    
    return db_webhook

# Trigger webhook
async def trigger_webhook(event_type: str, data: dict):
    webhooks = await db.execute(
        select(Webhook).where(
            Webhook.events.contains([event_type])
        )
    )
    
    for webhook in webhooks.scalars():
        # Sign request
        timestamp = int(time.time())
        signature = hmac.new(
            webhook.secret.encode(),
            f"{timestamp}.{json.dumps(data)}".encode(),
            hashlib.sha256
        ).hexdigest()
        
        # Send async
        asyncio.create_task(
            send_webhook(
                webhook.url,
                data,
                signature,
                timestamp
            )
        )

async def send_webhook(url: str, data: dict, signature: str, timestamp: int):
    async with httpx.AsyncClient() as client:
        try:
            await client.post(
                url,
                json=data,
                headers={
                    "X-Webhook-Signature": signature,
                    "X-Webhook-Timestamp": str(timestamp)
                },
                timeout=30,
                retries=3
            )
        except Exception as e:
            logger.error(f"Webhook delivery failed: {e}")
```

---

## 🔄 Versioning Strategy

### Semantic Versioning

```yaml
Version Format: MAJOR.MINOR.PATCH

MAJOR: Breaking changes
  - Removed endpoints
  - Changed response format
  - Changed behavior significantly

MINOR: Non-breaking additions
  - New endpoints
  - New optional parameters
  - New response fields (backward compatible)

PATCH: Bug fixes
  - Bug fixes
  - Security updates
  - Documentation updates

Examples:
  1.0.0 - Initial release
  1.1.0 - New endpoint added
  1.1.1 - Bug fix
  2.0.0 - Breaking change, removed deprecated endpoint
```

### API Versioning in URL

```yaml
# Version in URL path (recommended)
GET /api/v1/features
GET /api/v2/features

# Deprecation timeline
- v1 released: 2024-01-01
- v2 released: 2024-06-01 (v1 still supported)
- v1 deprecated: 2025-01-01 (warnings in headers)
- v1 sunset: 2025-06-01 (returns 410 Gone)

# Deprecation headers
HTTP/1.1 200 OK
Deprecation: true
Sunset: 2025-06-01T00:00:00Z
Link: <https://api.example.com/docs/migration-v1-to-v2>; rel="deprecation"
X-API-Warn: "API v1 deprecated, migrate to v2"
```

---

## 📚 Related Documents

- API Contracts (api_contracts.md)
- System Design (system_design.md)
- Performance Optimization (performance_optimization.md)

---

**END OF API DESIGN DOCUMENT**
