# Database Patterns Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Database Patterns Guide
**Primary Database:** PostgreSQL (with MongoDB alternatives for some patterns)

---

## 🎯 Core Database Patterns

### 1. Indexing Strategies

```sql
-- B-tree index (default)
CREATE INDEX idx_features_status ON features(status);

-- Composite index for common queries
CREATE INDEX idx_features_project_status ON features(project_id, status);

-- Partial index (index only active records)
CREATE INDEX idx_features_active ON features(project_id) 
WHERE deleted_at IS NULL;

-- Full-text search index
CREATE INDEX idx_features_search ON features USING GIN(
  to_tsvector('english', name || ' ' || description)
);

-- BRIN index (Block Range INdex, good for time-series)
CREATE INDEX idx_deployments_time ON deployments USING BRIN(created_at);

-- Hash index (for equality only)
CREATE INDEX idx_builds_hash ON builds USING HASH(version_tag);

-- Covering index (includes additional columns)
CREATE INDEX idx_test_results_coverage ON test_results(feature_id, status)
INCLUDE (code_coverage_percent, duration_ms);
```

### 2. Query Optimization

```sql
-- ❌ BAD: N+1 query problem
SELECT * FROM features;
-- Then loop and: SELECT * FROM test_cases WHERE feature_id = ?

-- ✅ GOOD: Use JOIN
SELECT f.*, tc.* 
FROM features f
LEFT JOIN test_cases tc ON f.id = tc.feature_id
ORDER BY f.created_at DESC;

-- ✅ BETTER: Use window functions
SELECT 
  f.id,
  f.name,
  COUNT(tc.id) OVER (PARTITION BY f.id) as test_count,
  AVG(tr.duration_ms) OVER (PARTITION BY f.id) as avg_test_duration
FROM features f
LEFT JOIN test_cases tc ON f.id = tc.feature_id
LEFT JOIN test_results tr ON tc.id = tr.test_case_id;

-- Use EXPLAIN to analyze queries
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM features WHERE status = 'in_progress';

-- Avoid SELECT *
SELECT id, name, complexity_points FROM features;  -- ✅ GOOD

-- Use LIMIT for pagination
SELECT * FROM features LIMIT 20 OFFSET 40;
```

### 3. Data Partitioning

```sql
-- Partition by range (time)
CREATE TABLE deployments_2024 PARTITION OF deployments
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE deployments_2025 PARTITION OF deployments
FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- Partition by organization (for multi-tenancy)
CREATE TABLE features_org1 PARTITION OF features
FOR VALUES IN ('org-uuid-1');

CREATE TABLE features_org2 PARTITION OF features
FOR VALUES IN ('org-uuid-2');

-- Query automatically uses correct partition
SELECT * FROM features WHERE organization_id = 'org-uuid-1';
```

### 4. Sharding Strategy

```python
# Simple hash-based sharding
class ShardingService:
    SHARD_COUNT = 4
    
    def get_shard(self, key: str) -> int:
        """Determine shard for key"""
        return hash(key) % self.SHARD_COUNT
    
    async def query_all_shards(self, query: str, params: list):
        """Execute query across all shards"""
        results = []
        for shard_id in range(self.SHARD_COUNT):
            db = self.get_shard_connection(shard_id)
            result = await db.execute(query, params)
            results.extend(result)
        return results

# Sharding by organization (recommended)
def get_org_shard(org_id: str) -> int:
    return hash(org_id) % 4

# Range-based sharding (by timestamp)
def get_deployment_shard(timestamp: datetime) -> int:
    month = timestamp.strftime("%Y%m")
    return hash(month) % 4
```

---

## 💾 Data Consistency Patterns

### 1. ACID Transactions

```python
# Ensure ACID properties
async def transfer_feature_ownership(
    feature_id: str,
    new_owner_id: str,
    session: AsyncSession
):
    """Transfer feature with ACID guarantees"""
    
    try:
        # Start transaction (implicit)
        feature = await session.get(Feature, feature_id)
        
        old_owner_id = feature.owner_id
        feature.owner_id = new_owner_id
        
        # Log change
        audit_log = AuditLog(
            action="feature_ownership_transferred",
            old_value=old_owner_id,
            new_value=new_owner_id
        )
        session.add(audit_log)
        
        # Commit (ACID guaranteed)
        await session.commit()
        
        return feature
    
    except Exception as e:
        # Automatic rollback
        await session.rollback()
        raise
```

### 2. Optimistic Locking

```python
# Add version column
class Feature(Base):
    __tablename__ = "features"
    
    id: Mapped[str]
    name: Mapped[str]
    version: Mapped[int] = mapped_column(default=1)

# Check version before update
async def update_feature_safe(
    feature_id: str,
    updates: dict,
    expected_version: int,
    session: AsyncSession
):
    """Update with version check"""
    
    feature = await session.get(Feature, feature_id)
    
    if feature.version != expected_version:
        raise ConflictError("Feature has been modified")
    
    # Update fields
    for key, value in updates.items():
        setattr(feature, key, value)
    
    # Increment version
    feature.version += 1
    
    await session.commit()
    
    return feature
```

### 3. Eventual Consistency

```python
# Primary database write
async def create_deployment(deployment: DeploymentCreate):
    deployment = Deployment(**deployment.dict())
    db.add(deployment)
    await db.commit()
    
    # Publish event for eventual consistency
    await event_bus.publish({
        "event": "deployment.created",
        "deployment_id": deployment.id,
        "timestamp": datetime.utcnow()
    })
    
    return deployment

# Replicate to read-only database
async def handle_deployment_created_event(event: dict):
    """Replicate to read replica"""
    deployment_id = event["deployment_id"]
    
    # Get from primary
    primary_deployment = await primary_db.get(Deployment, deployment_id)
    
    # Write to read replica
    await replica_db.insert(Deployment, primary_deployment.dict())
```

---

## 📊 MongoDB Patterns (for Logs & Events)

### Document Design

```javascript
// Time-series collection for metrics
{
  _id: ObjectId(),
  deployment_id: "deploy-1",
  timestamp: ISODate("2024-10-26T10:30:00Z"),
  metrics: {
    cpu_percent: 45.2,
    memory_percent: 62.1,
    response_time_ms: 245,
    error_rate: 0.0001
  }
}

// Event collection with TTL
db.events.createIndex(
  { created_at: 1 },
  { expireAfterSeconds: 604800 } // 7 days
);

db.events.insertOne({
  _id: ObjectId(),
  type: "deployment.started",
  data: {
    deployment_id: "deploy-1",
    environment: "production",
    version: "1.2.0"
  },
  created_at: new Date(),
  ttl: true
});
```

### Aggregation Pipeline

```javascript
// Complex aggregation
db.deployments.aggregate([
  { $match: { created_at: { $gte: ISODate("2024-01-01") } } },
  { $group: {
      _id: { $dateToString: { format: "%Y-%m-%d", date: "$created_at" } },
      success_count: { $sum: { $cond: ["$success", 1, 0] } },
      failure_count: { $sum: { $cond: ["$success", 0, 1] } }
    }
  },
  { $sort: { _id: 1 } }
]);
```

---

## 🔄 Caching Patterns

### Cache-Aside

```python
async def get_feature_with_cache(feature_id: str):
    # Check cache
    cached = await cache.get(f"feature:{feature_id}")
    if cached:
        return cached
    
    # Load from DB
    feature = await db.get(Feature, feature_id)
    
    # Update cache
    await cache.set(f"feature:{feature_id}", feature, ttl=3600)
    
    return feature
```

### Write-Through Cache

```python
async def update_feature(feature_id: str, updates: dict):
    # Update database
    feature = await db.update(Feature, feature_id, updates)
    
    # Update cache
    await cache.set(f"feature:{feature_id}", feature)
    
    return feature
```

### Cache Invalidation

```python
async def delete_feature(feature_id: str):
    # Delete from DB
    await db.delete(Feature, feature_id)
    
    # Invalidate cache
    await cache.delete(f"feature:{feature_id}")
    
    # Invalidate related caches
    await cache.delete(f"features:list:*")  # Pattern invalidation
```

---

## ⚡ Performance Optimization

### Connection Pooling

```python
# PostgreSQL connection pool
engine = create_async_engine(
    "postgresql+asyncpg://...",
    pool_size=20,           # Min connections
    max_overflow=10,        # Additional when needed
    pool_recycle=3600,      # Recycle after 1 hour
    pool_pre_ping=True      # Test before use
)
```

### Query Batching

```python
# ❌ BAD: Multiple queries
for feature_id in feature_ids:
    feature = await db.get(Feature, feature_id)
    process(feature)

# ✅ GOOD: Single query
features = await db.execute(
    select(Feature).where(Feature.id.in_(feature_ids))
)
for feature in features:
    process(feature)
```

### EXPLAIN Analysis

```sql
-- Analyze query plan
EXPLAIN ANALYZE
SELECT f.*, tc.* FROM features f
LEFT JOIN test_cases tc ON f.id = tc.feature_id
WHERE f.status = 'in_progress';

-- Output shows:
-- - Seq Scan vs Index Scan
-- - Cost estimates
-- - Actual rows vs estimates
-- - Heap blocks accessed
```

---

## 🔒 Data Security

### Encryption

```python
# Encrypt sensitive fields
from cryptography.fernet import Fernet

cipher = Fernet(settings.encryption_key)

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[str]
    email: Mapped[str]
    
    @property
    def phone_encrypted(self) -> str:
        return cipher.encrypt(self._phone.encode()).decode()
    
    @phone_encrypted.setter
    def phone_encrypted(self, value: str):
        self._phone = cipher.decrypt(value.encode()).decode()
```

### Row-Level Security

```sql
-- PostgreSQL RLS
ALTER TABLE features ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see features in their org
CREATE POLICY feature_org_policy ON features
FOR SELECT
USING (
  organization_id = (
    SELECT organization_id FROM users 
    WHERE id = current_user_id()
  )
);

-- Users can only update their own features
CREATE POLICY feature_update_policy ON features
FOR UPDATE
USING (owner_id = current_user_id());
```

---

## 📈 Scaling Strategies

### Read Replicas

```python
# Primary database for writes
primary_db = create_engine("postgresql://primary-host/db")

# Read replicas for queries
replica_db_1 = create_engine("postgresql://replica-1/db")
replica_db_2 = create_engine("postgresql://replica-2/db")

async def get_features():
    # Balance across replicas
    replica = random.choice([replica_db_1, replica_db_2])
    return await replica.execute(select(Feature))
```

### Database Replication

```yaml
# Synchronous replication
primary -> sync_replica (waits for confirmation)
        -> async_replica (doesn't wait)

# WAL shipping
Primary writes WAL -> Replicas apply WAL

# Physical replication (bit-for-bit copy)
```

---

## 📚 Related Documents

- Data Modeling (data_modeling.md)
- Performance Optimization (performance_optimization.md)
- Design Patterns (design_patterns.md)

---

**END OF DATABASE PATTERNS DOCUMENT**
