# Database Integration Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Database Integration Guide
**Focus:** 200+ integration techniques
**Primary Database:** PostgreSQL with MongoDB alternatives

---

## 🔌 Database Connection

### Connection Pooling

```typescript
// PostgreSQL with pg-pool
import Pool from 'pg-pool';

const pool = new Pool({
  host: process.env.DB_HOST,
  port: 5432,
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,           // Max connections
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

pool.on('error', (err) => {
  console.error('Unexpected error on idle client', err);
});

// SQLAlchemy async
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine(
    'postgresql+asyncpg://user:password@localhost/db',
    pool_size=20,
    max_overflow=10,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo_pool=False
)

# Mongoose
import mongoose from 'mongoose';

mongoose.connect('mongodb://localhost:27017/db', {
  maxPoolSize: 10,
  minPoolSize: 5,
  socketTimeoutMS: 45000,
});
```

### Connection Timeout Handling

```typescript
async function queryWithTimeout<T>(
  query: () => Promise<T>,
  timeoutMs: number = 30000
): Promise<T> {
  const timeoutPromise = new Promise<T>((_, reject) =>
    setTimeout(() => reject(new Error('Query timeout')), timeoutMs)
  );

  return Promise.race([query(), timeoutPromise]);
}

// Usage
const result = await queryWithTimeout(
  () => db.query('SELECT * FROM features'),
  5000
);
```

---

## 🔄 CRUD Operations

### Create with Transaction

```typescript
// PostgreSQL transaction
async function createFeatureWithLogs(
  feature: Feature,
  userId: string
): Promise<Feature> {
  const client = await pool.connect();

  try {
    await client.query('BEGIN');

    // Insert feature
    const featureResult = await client.query(
      'INSERT INTO features (name, priority) VALUES ($1, $2) RETURNING *',
      [feature.name, feature.priority]
    );

    const createdFeature = featureResult.rows[0];

    // Insert audit log
    await client.query(
      'INSERT INTO audit_logs (action, entity_id, user_id) VALUES ($1, $2, $3)',
      ['CREATE', createdFeature.id, userId]
    );

    await client.query('COMMIT');
    return createdFeature;
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}

// SQLAlchemy async transaction
async def create_feature_with_logs(
    session: AsyncSession,
    feature: FeatureCreate,
    user_id: str
) -> Feature:
    async with session.begin():
        db_feature = Feature(**feature.dict())
        session.add(db_feature)
        await session.flush()

        log = AuditLog(
            action='CREATE',
            entity_id=db_feature.id,
            user_id=user_id
        )
        session.add(log)

    await session.commit()
    return db_feature
```

### Bulk Operations

```typescript
// Bulk insert
async function bulkInsertFeatures(features: Feature[]) {
  const values = features
    .map((f, i) => `($${i * 2 + 1}, $${i * 2 + 2})`)
    .join(',');

  const params = features.flatMap(f => [f.name, f.priority]);

  return pool.query(
    `INSERT INTO features (name, priority) VALUES ${values} RETURNING *`,
    params
  );
}

// Bulk update with CASE
async function bulkUpdatePriorities(
  updates: Array<{ id: string; priority: number }>
) {
  const ids = updates.map(u => u.id);
  const cases = updates
    .map((u, i) => `WHEN '${u.id}' THEN ${u.priority}`)
    .join(' ');

  return pool.query(
    `UPDATE features SET priority = CASE id ${cases} END WHERE id = ANY($1)`,
    [ids]
  );
}

// Bulk delete
async function bulkDelete(ids: string[]) {
  return pool.query('DELETE FROM features WHERE id = ANY($1)', [ids]);
}

// MongoDB bulk operations
const bulk = db.collection('features').initializeUnorderedBulkOp();
bulk.insert({ name: 'Feature 1' });
bulk.insert({ name: 'Feature 2' });
await bulk.execute();
```

---

## 🔍 Query Optimization

### Indexes

```sql
-- Simple index
CREATE INDEX idx_features_status ON features(status);

-- Composite index
CREATE INDEX idx_features_project_status ON features(project_id, status);

-- Partial index (conditional)
CREATE INDEX idx_active_features ON features(id) WHERE deleted_at IS NULL;

-- Expression index
CREATE INDEX idx_features_lower_name ON features(LOWER(name));

-- Full-text search index
CREATE INDEX idx_features_search ON features USING GIN(
  to_tsvector('english', name || ' ' || description)
);

-- BRIN index (range)
CREATE INDEX idx_deployments_time ON deployments USING BRIN(created_at);
```

### Query Plans

```typescript
async function analyzeQuery(sql: string, params: any[] = []) {
  const explainQuery = `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) ${sql}`;
  const result = await pool.query(explainQuery, params);
  
  const plan = result.rows[0][0]['Plan'];
  console.log(`
    Rows: ${plan['Actual Rows']}
    Cost: ${plan['Total Cost']}
    Buffers: ${plan['Shared Hit Blocks']}
  `);
  
  return plan;
}
```

### N+1 Query Prevention

```typescript
// ❌ BAD: N+1 queries
async function getFeatures() {
  const features = await Feature.find();
  
  for (const feature of features) {
    feature.tests = await Test.find({ featureId: feature.id }); // N queries!
  }
  
  return features;
}

// ✅ GOOD: Join or batch
async function getFeatures() {
  // Method 1: Join
  return Feature.find()
    .populate('tests')
    .exec();

  // Method 2: Batch load
  const features = await Feature.find();
  const testsByFeature = await Test.find({
    featureId: { $in: features.map(f => f.id) }
  }).lean();

  const testMap = new Map();
  testsByFeature.forEach(test => {
    if (!testMap.has(test.featureId)) {
      testMap.set(test.featureId, []);
    }
    testMap.get(test.featureId).push(test);
  });

  return features.map(f => ({
    ...f,
    tests: testMap.get(f.id) || []
  }));
}
```

---

## 🔐 Data Integrity

### Foreign Keys

```sql
CREATE TABLE features (
  id UUID PRIMARY KEY,
  project_id UUID NOT NULL,
  name VARCHAR(255) NOT NULL,
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

CREATE TABLE tests (
  id UUID PRIMARY KEY,
  feature_id UUID NOT NULL,
  FOREIGN KEY (feature_id) REFERENCES features(id) ON DELETE CASCADE
);
```

### Constraints

```sql
-- Unique constraint
ALTER TABLE features ADD CONSTRAINT unique_project_name 
  UNIQUE(project_id, name);

-- Check constraint
ALTER TABLE features ADD CONSTRAINT check_priority 
  CHECK (priority >= 1 AND priority <= 13);

-- Not null with default
ALTER TABLE features ADD COLUMN status VARCHAR(50) 
  NOT NULL DEFAULT 'not_started';
```

---

## 📊 Data Migration

### Alembic Migrations

```python
# migration script
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'features',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('priority', sa.Integer, nullable=False)
    )

def downgrade():
    op.drop_table('features')
```

### Zero-Downtime Migration

```typescript
// Strategy: Add column with default, then migrate

// Step 1: Add new column with default (no downtime)
ALTER TABLE features ADD COLUMN new_status VARCHAR(50) DEFAULT 'active';

// Step 2: Migrate data in batches
UPDATE features SET new_status = status WHERE new_status IS NULL LIMIT 1000;

// Step 3: Add constraint
ALTER TABLE features ALTER COLUMN new_status SET NOT NULL;

// Step 4: Rename (requires brief lock, but much faster now)
ALTER TABLE features RENAME COLUMN status TO old_status;
ALTER TABLE features RENAME COLUMN new_status TO status;

// Step 5: Drop old column
ALTER TABLE features DROP COLUMN old_status;
```

---

## 📈 Replication & Backup

### Streaming Replication

```sql
-- Primary database setup
wal_level = 'replica'
max_wal_senders = 10
wal_keep_size = '1GB'

-- Create replication user
CREATE USER replication WITH REPLICATION ENCRYPTED PASSWORD 'password';

-- Replica setup
PRIMARY_CONNINFO='host=primary_host port=5432 user=replication password=password'
```

### Backup Strategy

```bash
#!/bin/bash

# Full backup
pg_dump -Fc -h localhost -U postgres db > backup_$(date +%Y%m%d).dump

# Point-in-time recovery
pg_basebackup -h primary -D /data/replica -U replication -Xstream -P

# Restore from backup
pg_restore -d db backup_20241026.dump
```

---

## 🔄 Event Sourcing

### Event Store

```typescript
interface Event {
  id: string;
  aggregateId: string;
  type: string;
  data: any;
  timestamp: Date;
  version: number;
}

async function appendEvent(
  aggregateId: string,
  type: string,
  data: any
): Promise<Event> {
  const version = await getLatestVersion(aggregateId);

  const event: Event = {
    id: generateUUID(),
    aggregateId,
    type,
    data,
    timestamp: new Date(),
    version: version + 1
  };

  await db.query(
    `INSERT INTO events (id, aggregate_id, type, data, timestamp, version)
     VALUES ($1, $2, $3, $4, $5, $6)`,
    [event.id, event.aggregateId, event.type, 
     JSON.stringify(event.data), event.timestamp, event.version]
  );

  return event;
}

// Replay events to reconstruct state
async function getAggregateState(aggregateId: string) {
  const events = await db.query(
    'SELECT * FROM events WHERE aggregate_id = $1 ORDER BY version',
    [aggregateId]
  );

  let state = {};
  for (const event of events.rows) {
    state = applyEvent(state, event);
  }

  return state;
}
```

---

## 🔄 CQRS Pattern

### Command Handler

```typescript
class CreateFeatureCommand {
  constructor(
    public name: string,
    public priority: number,
    public projectId: string
  ) {}
}

async function handleCreateFeatureCommand(command: CreateFeatureCommand) {
  // Validate
  if (command.priority < 1 || command.priority > 13) {
    throw new ValidationError('Invalid priority');
  }

  // Execute
  const feature = await Feature.create({
    name: command.name,
    priority: command.priority,
    projectId: command.projectId
  });

  // Publish event
  await eventBus.publish(
    new FeatureCreatedEvent(feature.id, feature.name)
  );

  return feature;
}
```

### Query Handler

```typescript
async function getFeaturesByProject(projectId: string) {
  // Query read model (optimized for reads)
  return db.query(
    `SELECT id, name, priority, test_count, deployment_status
     FROM features_view WHERE project_id = $1`,
    [projectId]
  );
}

// Read model kept in sync via events
async function handleFeatureCreatedEvent(event: FeatureCreatedEvent) {
  await db.query(
    `INSERT INTO features_view (id, name, project_id)
     VALUES ($1, $2, $3)`,
    [event.featureId, event.name, event.projectId]
  );
}
```

---

## 🔐 Encryption

### Column Encryption

```python
from cryptography.fernet import Fernet

class EncryptedFeature:
    cipher = Fernet(os.getenv('ENCRYPTION_KEY'))

    @classmethod
    def encrypt_field(cls, value: str) -> str:
        return cls.cipher.encrypt(value.encode()).decode()

    @classmethod
    def decrypt_field(cls, encrypted: str) -> str:
        return cls.cipher.decrypt(encrypted.encode()).decode()

# Store encrypted
encrypted_description = EncryptedFeature.encrypt_field(feature.description)

# Retrieve encrypted
feature.description = EncryptedFeature.decrypt_field(row.encrypted_description)
```

---

## 📚 Related Documents

- API Integration (api_integration.md)
- Backend-Frontend Integration (backend_frontend.md)
- Real-time Communication (real_time_communication.md)

---

**END OF DATABASE INTEGRATION DOCUMENT**
