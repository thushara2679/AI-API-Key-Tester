# Python Techniques Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Last Updated:** October 26, 2024
**Document Type:** Python Implementation Guide
**Python Version:** 3.10+
**Focus:** Production-grade Python techniques for microservices

---

## 📖 Introduction

This document provides comprehensive Python techniques, patterns, and best practices for implementing the AI Agent System microservices. It covers async programming, dependency injection, testing, optimization, and production deployment.

---

## 🚀 Async Programming with FastAPI

### Async/Await Patterns

```python
# ✅ GOOD: Proper async implementation
import asyncio
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

app = FastAPI()

# Async engine for database
engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost/db",
    echo=False,
    pool_size=20,
    max_overflow=10
)

async def get_session():
    async with AsyncSession(engine) as session:
        yield session

@app.get("/features/{feature_id}")
async def get_feature(
    feature_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get feature with proper async handling"""
    
    # Proper async database query
    result = await session.execute(
        select(Feature).where(Feature.id == feature_id)
    )
    feature = result.scalar_one_or_none()
    
    if not feature:
        raise HTTPException(status_code=404)
    
    return feature

@app.post("/deployments")
async def create_deployment(
    deployment: DeploymentCreate,
    session: AsyncSession = Depends(get_session),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Create deployment with background processing"""
    
    # Create in database
    db_deployment = Deployment(**deployment.dict())
    session.add(db_deployment)
    await session.commit()
    
    # Add background task for actual deployment
    background_tasks.add_task(
        deploy_async,
        db_deployment.id
    )
    
    return db_deployment

async def deploy_async(deployment_id: str):
    """Background async deployment task"""
    try:
        deployment = await get_deployment(deployment_id)
        
        # Run deployment steps concurrently
        await asyncio.gather(
            run_pre_checks(deployment),
            build_artifacts(deployment),
            prepare_infrastructure(deployment)
        )
        
        await execute_deployment(deployment)
        
    except Exception as e:
        await handle_deployment_error(deployment_id, e)

# ❌ AVOID: Blocking operations in async context
@app.get("/bad-example")
async def bad_endpoint():
    # This blocks the event loop!
    time.sleep(5)  # ❌ NEVER DO THIS
    return {"status": "done"}

# ✅ DO THIS INSTEAD: Use async sleep
@app.get("/good-example")
async def good_endpoint():
    # This properly yields control
    await asyncio.sleep(5)  # ✅ CORRECT
    return {"status": "done"}
```

### Concurrent Operations

```python
# Properly manage multiple concurrent operations
from typing import List
import asyncio

class ConcurrentProcessor:
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_items(
        self,
        items: List[str],
        processor_func
    ) -> List:
        """Process items with concurrency limit"""
        
        tasks = [
            self._bounded_processor(item, processor_func)
            for item in items
        ]
        
        # Run all tasks, handling exceptions
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [r for r in results if not isinstance(r, Exception)]
    
    async def _bounded_processor(self, item: str, processor_func):
        """Process single item with semaphore"""
        async with self.semaphore:
            try:
                return await processor_func(item)
            except Exception as e:
                logger.error(f"Error processing {item}: {e}")
                raise

# Usage
processor = ConcurrentProcessor(max_concurrent=20)

async def test_concurrent_processing():
    items = [f"item-{i}" for i in range(100)]
    
    async def process_item(item):
        # Simulate async work
        await asyncio.sleep(random.uniform(0.1, 0.5))
        return {"item": item, "status": "processed"}
    
    results = await processor.process_items(items, process_item)
    print(f"Processed {len(results)} items")
```

---

## 🔌 Dependency Injection Pattern

### FastAPI Dependency Injection

```python
from abc import ABC, abstractmethod
from typing import AsyncGenerator
from fastapi import Depends, HTTPException

# Interfaces
class DatabaseService(ABC):
    @abstractmethod
    async def get_feature(self, feature_id: str):
        pass
    
    @abstractmethod
    async def create_feature(self, feature: FeatureCreate):
        pass

class CacheService(ABC):
    @abstractmethod
    async def get(self, key: str):
        pass
    
    @abstractmethod
    async def set(self, key: str, value, ttl: int):
        pass

# Implementations
class PostgreSQLDatabaseService(DatabaseService):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_feature(self, feature_id: str):
        result = await self.session.execute(
            select(Feature).where(Feature.id == feature_id)
        )
        return result.scalar_one_or_none()
    
    async def create_feature(self, feature: FeatureCreate):
        db_feature = Feature(**feature.dict())
        self.session.add(db_feature)
        await self.session.commit()
        return db_feature

class RedisCacheService(CacheService):
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def get(self, key: str):
        value = await self.redis.get(key)
        return json.loads(value) if value else None
    
    async def set(self, key: str, value, ttl: int):
        await self.redis.setex(
            key,
            ttl,
            json.dumps(value)
        )

# Dependencies
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session

async def get_cache_service() -> CacheService:
    redis_client = await aioredis.create_redis_pool('redis://localhost')
    return RedisCacheService(redis_client)

async def get_database_service(
    session: AsyncSession = Depends(get_db_session)
) -> DatabaseService:
    return PostgreSQLDatabaseService(session)

# Usage in routes
@app.get("/features/{feature_id}")
async def get_feature(
    feature_id: str,
    cache: CacheService = Depends(get_cache_service),
    db: DatabaseService = Depends(get_database_service)
):
    """Get feature with caching"""
    
    # Try cache first
    cached = await cache.get(f"feature:{feature_id}")
    if cached:
        return cached
    
    # Get from database
    feature = await db.get_feature(feature_id)
    
    if not feature:
        raise HTTPException(status_code=404)
    
    # Update cache
    await cache.set(f"feature:{feature_id}", feature.dict(), ttl=3600)
    
    return feature
```

---

## 🧪 Testing Patterns

### Unit Testing with Pytest

```python
# tests/test_features.py
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
async def mock_db():
    """Mock database service"""
    db = AsyncMock()
    db.get_feature = AsyncMock()
    db.create_feature = AsyncMock()
    return db

@pytest.fixture
async def mock_cache():
    """Mock cache service"""
    cache = AsyncMock()
    cache.get = AsyncMock(return_value=None)
    cache.set = AsyncMock()
    return cache

@pytest.mark.asyncio
async def test_get_feature_from_cache(mock_cache, mock_db):
    """Test feature retrieval from cache"""
    
    # Setup
    feature_data = {"id": "feat-1", "name": "OAuth"}
    mock_cache.get.return_value = feature_data
    
    # Execute
    result = await get_feature_with_cache("feat-1", mock_cache, mock_db)
    
    # Assert
    assert result == feature_data
    mock_cache.get.assert_called_once_with("feature:feat-1")
    mock_db.get_feature.assert_not_called()  # DB not called

@pytest.mark.asyncio
async def test_get_feature_from_db(mock_cache, mock_db):
    """Test feature retrieval from database"""
    
    # Setup
    feature = Feature(id="feat-1", name="OAuth")
    mock_cache.get.return_value = None
    mock_db.get_feature.return_value = feature
    
    # Execute
    result = await get_feature_with_cache("feat-1", mock_cache, mock_db)
    
    # Assert
    assert result.id == "feat-1"
    mock_db.get_feature.assert_called_once_with("feat-1")
    mock_cache.set.assert_called_once()

@pytest.mark.asyncio
async def test_create_feature_validation():
    """Test feature creation validation"""
    
    invalid_features = [
        {},  # Missing required fields
        {"name": ""},  # Empty name
        {"name": "x"},  # Too short
    ]
    
    for invalid in invalid_features:
        with pytest.raises(ValueError):
            FeatureCreate(**invalid)

class TestFeatureService:
    """Test suite for FeatureService"""
    
    @pytest.fixture
    def service(self, mock_db, mock_cache):
        return FeatureService(db=mock_db, cache=mock_cache)
    
    @pytest.mark.asyncio
    async def test_create_feature(self, service):
        feature_create = FeatureCreate(
            name="New Feature",
            complexity_points=5
        )
        
        result = await service.create_feature(feature_create)
        
        assert result.name == "New Feature"
        assert result.complexity_points == 5
    
    @pytest.mark.asyncio
    async def test_concurrent_feature_processing(self, service):
        """Test concurrent feature processing"""
        
        features = [
            FeatureCreate(name=f"Feature {i}", complexity_points=i)
            for i in range(10)
        ]
        
        results = await asyncio.gather(*[
            service.create_feature(f)
            for f in features
        ])
        
        assert len(results) == 10
        assert all(r.name for r in results)
```

### Integration Testing

```python
# tests/integration/test_feature_api.py
import pytest
from httpx import AsyncClient

@pytest.fixture
async def client():
    """Create test client"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(autouse=True)
async def setup_test_db():
    """Setup test database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
class TestFeatureAPI:
    async def test_create_feature(self, client):
        """Test feature creation endpoint"""
        
        response = await client.post(
            "/api/features",
            json={
                "name": "OAuth Integration",
                "complexity_points": 8
            }
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "OAuth Integration"
        assert data["id"] is not None
    
    async def test_get_feature(self, client):
        """Test feature retrieval endpoint"""
        
        # Create feature
        create_response = await client.post(
            "/api/features",
            json={"name": "Feature", "complexity_points": 5}
        )
        feature_id = create_response.json()["id"]
        
        # Get feature
        response = await client.get(f"/api/features/{feature_id}")
        
        assert response.status_code == 200
        assert response.json()["id"] == feature_id
    
    async def test_list_features_pagination(self, client):
        """Test feature list pagination"""
        
        # Create multiple features
        for i in range(25):
            await client.post(
                "/api/features",
                json={"name": f"Feature {i}", "complexity_points": i % 13}
            )
        
        # Get first page
        response = await client.get("/api/features?page=1&page_size=10")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 10
        assert data["pagination"]["total"] == 25
```

---

## 📦 Package Management & Dependencies

### Poetry Configuration

```yaml
# pyproject.toml
[tool.poetry]
name = "ai-agents"
version = "1.0.0"
description = "AI Agent System for Enterprise Automation"
authors = ["Dev Team"]

[tool.poetry.dependencies]
python = "^3.10"

# Web Framework
fastapi = "^0.109.0"
uvicorn = "^0.27.0"
pydantic = "^2.0"

# Database
sqlalchemy = "^2.0"
asyncpg = "^0.29.0"
alembic = "^1.13.0"

# Caching
redis = "^5.0"
aioredis = "^2.0"

# Message Queue
kafka-python = "^2.0"
pika = "^1.3"

# Logging & Monitoring
python-json-logger = "^2.0"
opentelemetry-api = "^1.20"
opentelemetry-sdk = "^1.20"

# Testing
pytest = "^7.4"
pytest-asyncio = "^0.21"
httpx = "^0.25"

[tool.poetry.dev-dependencies]
black = "^23.12"
isort = "^5.13"
pylint = "^3.0"
mypy = "^1.7"

[tool.black]
line-length = 100
target-version = ['py310']

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
```

---

## 🔒 Security Best Practices

### Secrets Management

```python
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """Application settings with secrets management"""
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "")
    database_ssl: bool = True
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # JWT
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600
    
    # AWS
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    
    # API Keys
    github_api_key: str = os.getenv("GITHUB_API_KEY", "")
    gitlab_api_key: str = os.getenv("GITLAB_API_KEY", "")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def database_url_safe(self) -> str:
        """Return database URL with sensitive info masked"""
        return self.database_url.replace(
            self.database_url.split("@")[0],
            "***:***"
        )

settings = Settings()

# ✅ CORRECT: Use settings
def get_db_connection():
    return create_engine(settings.database_url)

# ❌ WRONG: Hardcode secrets
# DATABASE_URL = "postgresql://user:password@localhost/db"
```

### Input Validation & Sanitization

```python
from pydantic import BaseModel, Field, validator
import html

class FeatureCreate(BaseModel):
    """Feature creation request with validation"""
    
    name: str = Field(
        min_length=2,
        max_length=255,
        description="Feature name"
    )
    description: str = Field(
        max_length=2000,
        description="Feature description"
    )
    complexity_points: int = Field(
        ge=1,
        le=13,
        description="Story points (1-13)"
    )
    
    @validator('name')
    def sanitize_name(cls, v):
        """Sanitize HTML in name"""
        return html.escape(v.strip())
    
    @validator('description')
    def sanitize_description(cls, v):
        """Sanitize HTML in description"""
        return html.escape(v.strip())
    
    class Config:
        schema_extra = {
            "example": {
                "name": "OAuth Integration",
                "description": "Implement OAuth 2.0",
                "complexity_points": 8
            }
        }

@app.post("/features")
async def create_feature(
    feature: FeatureCreate,
    session: AsyncSession = Depends(get_db_session)
):
    """Create feature with validated input"""
    
    # Validation happens automatically with Pydantic
    # SQL injection prevention: use parameterized queries
    db_feature = Feature(**feature.dict())
    session.add(db_feature)
    await session.commit()
    
    return db_feature
```

---

## 📊 Performance Optimization

### Connection Pooling

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# ✅ CORRECT: Proper connection pooling
engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost/db",
    echo=False,
    pool_size=20,           # Connection pool size
    max_overflow=10,        # Additional connections when pool exhausted
    pool_recycle=3600,      # Recycle connections after 1 hour
    pool_pre_ping=True,     # Test connection before using
    echo_pool=False
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ❌ WRONG: Creating new engine per request
@app.get("/bad")
async def bad_endpoint():
    # This creates new connection each time!
    engine = create_async_engine("postgresql://...")
    # Very inefficient
    return {"status": "done"}

# ✅ CORRECT: Reuse session
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/good")
async def good_endpoint(session: AsyncSession = Depends(get_session)):
    # Uses pooled connection
    return {"status": "done"}
```

### Query Optimization

```python
from sqlalchemy import select, joinedload
from sqlalchemy.orm import selectinload

@app.get("/features/{feature_id}")
async def get_feature(
    feature_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get feature with optimized queries"""
    
    # ✅ GOOD: Use eager loading to prevent N+1 queries
    stmt = select(Feature).where(
        Feature.id == feature_id
    ).options(
        selectinload(Feature.test_cases),
        selectinload(Feature.builds)
    )
    
    result = await session.execute(stmt)
    feature = result.unique().scalar_one_or_none()
    
    return feature

# ❌ BAD: N+1 query problem
@app.get("/features-bad")
async def get_features_bad(session: AsyncSession = Depends(get_session)):
    features = await session.execute(select(Feature))
    
    result = []
    for feature in features:
        # This causes N additional queries!
        test_cases = await session.execute(
            select(TestCase).where(TestCase.feature_id == feature.id)
        )
        result.append({
            "feature": feature,
            "test_cases": test_cases
        })
    
    return result

# ✅ GOOD: Use joins or selectinload
@app.get("/features-good")
async def get_features_good(session: AsyncSession = Depends(get_session)):
    stmt = select(Feature).options(
        selectinload(Feature.test_cases)
    )
    
    result = await session.execute(stmt)
    features = result.unique().scalars()
    
    return features
```

---

## 🔍 Logging & Monitoring

### Structured Logging

```python
import logging
import json
from pythonjsonlogger import jsonlogger

# Configure structured logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Usage
logger.info("Feature created", extra={
    "feature_id": "feat-1",
    "user_id": "user-123",
    "complexity_points": 8,
    "duration_ms": 125
})

# Middleware for request logging
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    import time
    
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": process_time * 1000,
            "user_id": request.state.user.get("sub") if hasattr(request.state, "user") else None
        }
    )
    
    return response
```

### OpenTelemetry Integration

```python
from opentelemetry import trace, metrics
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

# Setup tracing
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(jaeger_exporter)
)

# Instrument libraries
FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine)

# Custom spans
tracer = trace.get_tracer(__name__)

@app.post("/features")
async def create_feature(feature: FeatureCreate):
    with tracer.start_as_current_span("create_feature") as span:
        span.set_attribute("feature.name", feature.name)
        span.set_attribute("feature.complexity", feature.complexity_points)
        
        # Business logic here
        
        span.set_attribute("feature.created", True)
```

---

## 📚 Related Documents

- API Design (api_design.md)
- Design Patterns (design_patterns.md)
- Database Patterns (database_patterns.md)
- Performance Optimization (performance_optimization.md)

---

## 📝 Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Oct 26, 2024 | Python Team | Initial version |

---

**END OF PYTHON TECHNIQUES DOCUMENT**
