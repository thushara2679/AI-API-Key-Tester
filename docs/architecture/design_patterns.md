# Design Patterns Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Last Updated:** October 26, 2024
**Document Type:** Design Patterns Reference
**Pattern Coverage:** GoF + Architectural + Cloud-Native patterns

---

## 📖 Introduction

This document describes the design patterns used throughout the AI Agent System. It includes architectural patterns, behavioral patterns, structural patterns, and cloud-native patterns with implementation examples and use cases.

---

## 🎯 Pattern Categories

1. **Architectural Patterns** - High-level system organization
2. **Behavioral Patterns** - Object interaction and responsibility
3. **Structural Patterns** - Object composition and relationships
4. **Cloud-Native Patterns** - Distributed system patterns
5. **Data Patterns** - Data management and persistence
6. **Concurrency Patterns** - Multi-threading and async patterns

---

## 🏗️ Architectural Patterns

### 1. Microservices Architecture

**Definition:** System composed of small, independent, loosely-coupled services that communicate via APIs.

**Implementation in AI Agent System:**
- 8 independent agent services
- Each service has own database
- Communication via REST APIs + Message Queue
- Independent deployment and scaling

**Benefits:**
- Scalability (scale each service independently)
- Resilience (failure isolated to one service)
- Technology flexibility (each service uses appropriate tech)
- Team independence (teams own their services)

**Challenges:**
- Operational complexity
- Network latency
- Data consistency across services
- Debugging distributed issues

**Example:**

```yaml
services:
  business-analyzer:
    image: registry/business-analyzer:latest
    ports:
      - "8001:8000"
    environment:
      - DATABASE_URL=postgresql://db:5432/analyzer
      - KAFKA_BROKERS=kafka:9092
    depends_on:
      - postgres
      - kafka

  backend-developer:
    image: registry/backend-developer:latest
    ports:
      - "8002:8000"
    environment:
      - DATABASE_URL=postgresql://db:5432/backend
      - KAFKA_BROKERS=kafka:9092
    depends_on:
      - postgres
      - kafka

  # ... other services ...
```

---

### 2. API Gateway Pattern

**Definition:** Single entry point for all client requests, handling routing, authentication, rate limiting.

**Implementation:**

```python
# api_gateway/main.py
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

# Route definitions
SERVICES = {
    "/api/requirements": "http://business-analyzer:8000",
    "/api/features": "http://backend-developer:8000",
    "/api/tests": "http://testing-engineer:8000",
    "/api/deployments": "http://deployment-engineer:8000"
}

@app.middleware("http")
async def gateway_middleware(request: Request, call_next):
    # Authentication
    token = request.headers.get("Authorization")
    if not token:
        return JSONResponse({"error": "Missing token"}, status_code=401)
    
    # Validate JWT
    try:
        payload = jwt.decode(token.replace("Bearer ", ""), SECRET_KEY)
        request.state.user = payload
    except:
        return JSONResponse({"error": "Invalid token"}, status_code=401)
    
    # Rate limiting
    user_id = payload.get("sub")
    if not check_rate_limit(user_id):
        return JSONResponse(
            {"error": "Rate limit exceeded"}, 
            status_code=429
        )
    
    # Request logging
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Response logging
    logger.info(f"Response: {response.status_code}")
    
    return response

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway_route(request: Request, path: str):
    """Route request to appropriate microservice"""
    
    # Find matching service
    service_url = None
    for route_prefix, url in SERVICES.items():
        if path.startswith(route_prefix):
            service_url = url + "/" + path.replace(route_prefix, "", 1)
            break
    
    if not service_url:
        return JSONResponse({"error": "Not found"}, status_code=404)
    
    # Forward request
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=service_url,
            headers=request.headers,
            content=await request.body()
        )
    
    return JSONResponse(
        response.json(),
        status_code=response.status_code
    )
```

---

### 3. Event-Driven Architecture

**Definition:** Services communicate asynchronously via events published to message queue.

**Implementation:**

```python
# Event Producer (Backend Developer Agent)
import asyncio
import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

async def create_feature(requirement: Requirement):
    feature = Feature.create(requirement)
    
    # Publish event
    event = {
        "event_type": "feature.created",
        "timestamp": datetime.utcnow().isoformat(),
        "data": {
            "feature_id": feature.id,
            "requirement_id": requirement.id,
            "name": feature.name
        }
    }
    
    producer.send('feature-events', value=event)
    return feature

# Event Consumer (Testing Engineer Agent)
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'feature-events',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='testing-engineer-group'
)

async def consume_events():
    for message in consumer:
        event = message.value
        
        if event['event_type'] == 'feature.created':
            feature_id = event['data']['feature_id']
            await generate_test_cases(feature_id)
            
            # Publish event for next service
            test_event = {
                "event_type": "tests.generated",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "feature_id": feature_id,
                    "test_count": 10
                }
            }
            producer.send('test-events', value=test_event)
```

---

## 🔄 Behavioral Patterns

### 1. Command Pattern

**Definition:** Encapsulate a request as an object, allowing parameterization of actions.

**Implementation:**

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

# Abstract Command
class Command(ABC):
    @abstractmethod
    async def execute(self):
        pass
    
    @abstractmethod
    async def undo(self):
        pass

# Concrete Commands
@dataclass
class CreateFeatureCommand(Command):
    requirement_id: str
    feature_name: str
    developer: str
    
    async def execute(self):
        self.feature = Feature.create(
            requirement_id=self.requirement_id,
            name=self.feature_name,
            developer=self.developer
        )
        logger.info(f"Feature created: {self.feature.id}")
        return self.feature
    
    async def undo(self):
        self.feature.delete()
        logger.info(f"Feature deleted: {self.feature.id}")

@dataclass
class DeployFeatureCommand(Command):
    build_id: str
    environment: str
    
    async def execute(self):
        self.deployment = Deployment.create(
            build_id=self.build_id,
            environment=self.environment
        )
        logger.info(f"Deployment created: {self.deployment.id}")
        return self.deployment
    
    async def undo(self):
        self.deployment.rollback()
        logger.info(f"Deployment rolled back: {self.deployment.id}")

# Command Invoker
class CommandQueue:
    def __init__(self):
        self.commands = []
        self.history = []
    
    async def execute_command(self, command: Command):
        result = await command.execute()
        self.history.append(command)
        return result
    
    async def undo_last(self):
        if self.history:
            command = self.history.pop()
            await command.undo()

# Usage
async def main():
    queue = CommandQueue()
    
    cmd1 = CreateFeatureCommand(
        requirement_id="req-1",
        feature_name="OAuth Integration",
        developer="alice"
    )
    feature = await queue.execute_command(cmd1)
    
    cmd2 = DeployFeatureCommand(
        build_id="build-1",
        environment="staging"
    )
    deployment = await queue.execute_command(cmd2)
    
    # Undo if needed
    await queue.undo_last()  # Rollback deployment
```

---

### 2. Observer Pattern

**Definition:** Define a one-to-many dependency where when one object changes state, all dependents are notified automatically.

**Implementation:**

```python
from typing import List, Callable
from abc import ABC, abstractmethod

class Observable:
    def __init__(self):
        self._observers: List[Callable] = []
    
    def subscribe(self, observer: Callable):
        """Subscribe to events"""
        self._observers.append(observer)
    
    def unsubscribe(self, observer: Callable):
        """Unsubscribe from events"""
        self._observers.remove(observer)
    
    async def notify(self, event: dict):
        """Notify all observers"""
        for observer in self._observers:
            await observer(event)

class DeploymentService(Observable):
    async def deploy(self, build_id: str, environment: str):
        deployment = Deployment.create(build_id, environment)
        
        # Notify observers of deployment started
        await self.notify({
            "event": "deployment.started",
            "deployment_id": deployment.id,
            "environment": environment
        })
        
        try:
            # Deploy
            result = await self._do_deploy(deployment)
            
            # Notify observers of deployment succeeded
            await self.notify({
                "event": "deployment.succeeded",
                "deployment_id": deployment.id,
                "result": result
            })
        except Exception as e:
            # Notify observers of deployment failed
            await self.notify({
                "event": "deployment.failed",
                "deployment_id": deployment.id,
                "error": str(e)
            })
            raise

# Observers
class MonitoringObserver:
    async def __call__(self, event: dict):
        logger.info(f"Monitoring: {event['event']}")
        # Update metrics, dashboards, etc.

class NotificationObserver:
    async def __call__(self, event: dict):
        logger.info(f"Notification: {event['event']}")
        # Send Slack/email notifications

class IncidentManagementObserver:
    async def __call__(self, event: dict):
        if "failed" in event['event']:
            logger.critical(f"Incident: {event}")
            # Create incident, page on-call engineer

# Usage
deployment_service = DeploymentService()
deployment_service.subscribe(MonitoringObserver())
deployment_service.subscribe(NotificationObserver())
deployment_service.subscribe(IncidentManagementObserver())

await deployment_service.deploy("build-1", "production")
```

---

### 3. Strategy Pattern

**Definition:** Define a family of algorithms, encapsulate each one, and make them interchangeable.

**Implementation:**

```python
from abc import ABC, abstractmethod
from enum import Enum

class DeploymentStrategy(ABC):
    """Abstract deployment strategy"""
    
    @abstractmethod
    async def deploy(self, deployment: Deployment):
        pass
    
    @abstractmethod
    async def rollback(self, deployment: Deployment):
        pass

class BlueGreenDeployment(DeploymentStrategy):
    """Deploy to inactive environment, switch traffic"""
    
    async def deploy(self, deployment: Deployment):
        logger.info("Blue-green deployment starting")
        
        # Deploy to green environment
        await self._deploy_to_environment(deployment, "green")
        
        # Health checks
        if not await self._health_checks(deployment, "green"):
            await self.rollback(deployment)
            raise Exception("Health checks failed")
        
        # Route traffic: 10% → 50% → 100%
        for percentage in [10, 50, 100]:
            await self._route_traffic(deployment, percentage)
            await asyncio.sleep(300)  # 5 minutes
            
            # Check metrics
            if await self._metrics_degraded(deployment):
                await self.rollback(deployment)
                raise Exception("Metrics degraded")
        
        logger.info("Blue-green deployment succeeded")
    
    async def rollback(self, deployment: Deployment):
        logger.info("Blue-green rollback starting")
        await self._route_traffic(deployment, 0)  # Route all to blue
        await self._destroy_environment(deployment, "green")

class CanaryDeployment(DeploymentStrategy):
    """Deploy to fraction of users, gradually increase"""
    
    async def deploy(self, deployment: Deployment):
        logger.info("Canary deployment starting")
        
        # Deploy to all infrastructure
        await self._deploy_to_all(deployment)
        
        # Start with 5% traffic
        for percentage in [5, 25, 50, 100]:
            await self._route_traffic(deployment, percentage)
            
            # Monitor metrics for this percentage
            await asyncio.sleep(600)  # 10 minutes per stage
            
            if await self._metrics_degraded(deployment):
                await self.rollback(deployment)
                raise Exception("Metrics degraded at {percentage}%")
        
        logger.info("Canary deployment succeeded")
    
    async def rollback(self, deployment: Deployment):
        logger.info("Canary rollback starting")
        await self._route_traffic(deployment, 0)

class RollingDeployment(DeploymentStrategy):
    """Update instances one at a time"""
    
    async def deploy(self, deployment: Deployment):
        logger.info("Rolling deployment starting")
        
        instances = await self._get_instances(deployment)
        
        for i, instance in enumerate(instances):
            logger.info(f"Updating instance {i+1}/{len(instances)}")
            
            # Take instance out of load balancer
            await self._deregister_instance(instance)
            
            # Update instance
            await self._update_instance(instance, deployment)
            
            # Health checks
            if not await self._health_check_instance(instance):
                await self.rollback(deployment)
                raise Exception(f"Health check failed on instance {i}")
            
            # Return to load balancer
            await self._register_instance(instance)
            
            # Wait before next instance
            await asyncio.sleep(300)
        
        logger.info("Rolling deployment succeeded")
    
    async def rollback(self, deployment: Deployment):
        logger.info("Rolling rollback starting")
        # Redeploy previous version

# Deployment service using strategies
class DeploymentService:
    STRATEGIES = {
        "blue_green": BlueGreenDeployment(),
        "canary": CanaryDeployment(),
        "rolling": RollingDeployment()
    }
    
    async def deploy(self, build_id: str, strategy: str = "blue_green"):
        deployment = Deployment.create(build_id)
        strategy_impl = self.STRATEGIES[strategy]
        await strategy_impl.deploy(deployment)

# Usage
service = DeploymentService()
await service.deploy("build-1", strategy="canary")
await service.deploy("build-2", strategy="blue_green")
```

---

## 🏛️ Structural Patterns

### 1. Adapter Pattern

**Definition:** Convert the interface of a class into another interface clients expect.

**Implementation:**

```python
from abc import ABC, abstractmethod

# External system interface
class ExternalBuildSystem:
    def trigger_build(self, project_name):
        return f"Building {project_name}..."

# Our internal interface
class BuildService(ABC):
    @abstractmethod
    async def build(self, feature_id: str):
        pass

# Adapter
class ExternalBuildAdapter(BuildService):
    def __init__(self, external_system: ExternalBuildSystem):
        self.external_system = external_system
    
    async def build(self, feature_id: str):
        # Get feature details
        feature = await Feature.get(feature_id)
        
        # Call external system
        result = self.external_system.trigger_build(feature.project_name)
        
        # Create our Build object
        build = Build.create(
            feature_id=feature_id,
            external_build_id=result
        )
        
        return build

# Usage
external_system = ExternalBuildSystem()
adapter = ExternalBuildAdapter(external_system)
build = await adapter.build("feat-1")
```

---

### 2. Facade Pattern

**Definition:** Provide a unified, simplified interface to a set of interfaces in a subsystem.

**Implementation:**

```python
from dataclasses import dataclass

@dataclass
class DeploymentRequest:
    feature_id: str
    environment: str
    strategy: str = "blue_green"

class DeploymentFacade:
    """Simplified interface for complex deployment process"""
    
    def __init__(self):
        self.build_service = BuildService()
        self.test_service = TestService()
        self.security_service = SecurityService()
        self.deployment_service = DeploymentService()
        self.monitoring_service = MonitoringService()
    
    async def deploy_feature(self, request: DeploymentRequest):
        """Orchestrate complete deployment"""
        
        logger.info(f"Starting deployment: {request.feature_id}")
        
        try:
            # Step 1: Build
            build = await self.build_service.build(request.feature_id)
            logger.info(f"Build succeeded: {build.id}")
            
            # Step 2: Test
            test_results = await self.test_service.run_all_tests(build.id)
            if not test_results.passed:
                raise Exception("Tests failed")
            logger.info(f"Tests passed: {test_results.coverage}% coverage")
            
            # Step 3: Security
            security_check = await self.security_service.scan(build.id)
            if security_check.vulnerabilities:
                raise Exception("Vulnerabilities found")
            logger.info("Security check passed")
            
            # Step 4: Deploy
            deployment = await self.deployment_service.deploy(
                build.id,
                request.environment,
                request.strategy
            )
            logger.info(f"Deployment succeeded: {deployment.id}")
            
            # Step 5: Monitor
            await self.monitoring_service.setup_monitoring(deployment.id)
            logger.info("Monitoring configured")
            
            return {
                "success": True,
                "build_id": build.id,
                "deployment_id": deployment.id,
                "metrics": {
                    "test_coverage": test_results.coverage,
                    "build_time": build.duration,
                    "deployment_time": deployment.duration
                }
            }
        
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            await self.deployment_service.rollback()
            raise

# Usage
facade = DeploymentFacade()
result = await facade.deploy_feature(
    DeploymentRequest(
        feature_id="feat-1",
        environment="production",
        strategy="canary"
    )
)
```

---

## ☁️ Cloud-Native Patterns

### 1. Circuit Breaker Pattern

**Definition:** Prevent cascading failures by breaking calls to failing services.

**Implementation:**

```python
from enum import Enum
import asyncio
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Fail fast
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout_seconds: int = 60
    ):
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout_seconds = timeout_seconds
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
    
    async def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                logger.info("Circuit breaker CLOSED (recovered)")
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning("Circuit breaker OPEN (threshold exceeded)")
    
    def _should_attempt_reset(self):
        return (
            datetime.now() - self.last_failure_time
        ).seconds >= self.timeout_seconds

# Service with circuit breaker
class ResilientDeploymentService:
    def __init__(self):
        self.circuit_breaker = CircuitBreaker()
    
    async def notify_monitoring(self, deployment_id: str):
        """Call monitoring service with circuit breaker"""
        try:
            await self.circuit_breaker.call(
                self._call_monitoring_service,
                deployment_id
            )
        except Exception as e:
            logger.error(f"Monitoring service unavailable: {e}")
            # Continue without monitoring (degraded mode)
    
    async def _call_monitoring_service(self, deployment_id: str):
        # Call external monitoring service
        response = await httpx.get(
            f"http://monitoring:8000/deployments/{deployment_id}",
            timeout=5
        )
        response.raise_for_status()
```

---

### 2. Retry Pattern with Exponential Backoff

**Definition:** Retry failed operations with exponentially increasing delays.

**Implementation:**

```python
import asyncio
from typing import Callable

async def retry_with_backoff(
    func: Callable,
    *args,
    max_retries: int = 3,
    base_delay: int = 1,
    max_delay: int = 60,
    **kwargs
):
    """Retry function with exponential backoff"""
    
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            logger.info(f"Attempt {attempt + 1}/{max_retries + 1}")
            result = await func(*args, **kwargs)
            logger.info(f"Success on attempt {attempt + 1}")
            return result
        
        except Exception as e:
            last_exception = e
            
            if attempt < max_retries:
                # Calculate delay with exponential backoff
                delay = min(
                    base_delay * (2 ** attempt),
                    max_delay
                )
                
                # Add jitter to prevent thundering herd
                jitter = random.uniform(0, delay * 0.1)
                actual_delay = delay + jitter
                
                logger.warning(
                    f"Attempt {attempt + 1} failed: {e}. "
                    f"Retrying in {actual_delay:.1f}s"
                )
                
                await asyncio.sleep(actual_delay)
    
    logger.error(f"Failed after {max_retries + 1} attempts")
    raise last_exception

# Decorator version
def retry(max_retries=3, base_delay=1, max_delay=60):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            return await retry_with_backoff(
                func,
                *args,
                max_retries=max_retries,
                base_delay=base_delay,
                max_delay=max_delay,
                **kwargs
            )
        return wrapper
    return decorator

# Usage
@retry(max_retries=3, base_delay=1, max_delay=10)
async def deploy_to_kubernetes(deployment: Deployment):
    # Call Kubernetes API
    return await kubectl.apply(deployment)

# Or with function call
result = await retry_with_backoff(
    deploy_to_kubernetes,
    deployment,
    max_retries=3
)
```

---

### 3. Bulkhead Pattern

**Definition:** Isolate elements into pools so that if one fails, others are not affected.

**Implementation:**

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class Bulkhead:
    """Isolate resources into independent thread pools"""
    
    def __init__(self, name: str, max_concurrent: int):
        self.name = name
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.active_count = 0
    
    async def execute(self, func, *args, **kwargs):
        async with self.semaphore:
            self.active_count += 1
            logger.info(
                f"{self.name}: {self.active_count} active requests"
            )
            
            try:
                return await func(*args, **kwargs)
            finally:
                self.active_count -= 1

# Service with bulkheads
class BulkheadedDeploymentService:
    def __init__(self):
        # Isolate different operations
        self.build_bulkhead = Bulkhead("build", max_concurrent=5)
        self.test_bulkhead = Bulkhead("test", max_concurrent=10)
        self.deploy_bulkhead = Bulkhead("deploy", max_concurrent=2)
    
    async def build(self, feature_id: str):
        return await self.build_bulkhead.execute(
            self._build_impl,
            feature_id
        )
    
    async def test(self, build_id: str):
        return await self.test_bulkhead.execute(
            self._test_impl,
            build_id
        )
    
    async def deploy(self, build_id: str, environment: str):
        return await self.deploy_bulkhead.execute(
            self._deploy_impl,
            build_id,
            environment
        )

# Usage
service = BulkheadedDeploymentService()

# These will run concurrently but limited by bulkheads
tasks = [
    service.build("feat-1"),
    service.build("feat-2"),
    service.build("feat-3"),
    service.test("build-1"),
    service.deploy("build-1", "staging")
]

results = await asyncio.gather(*tasks)
```

---

## 📊 Data Patterns

### 1. Repository Pattern

**Definition:** Encapsulate data access logic and provide object-oriented interface.

**Implementation:**

```python
from abc import ABC, abstractmethod
from typing import List, Optional

class Repository(ABC):
    """Abstract repository"""
    
    @abstractmethod
    async def get(self, id: str) -> Optional[object]:
        pass
    
    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 10) -> List[object]:
        pass
    
    @abstractmethod
    async def create(self, obj: object) -> object:
        pass
    
    @abstractmethod
    async def update(self, id: str, obj: object) -> object:
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass

class FeatureRepository(Repository):
    """Repository for Feature entities"""
    
    async def get(self, id: str) -> Optional[Feature]:
        async with get_db() as db:
            result = await db.query(
                "SELECT * FROM features WHERE id = %s",
                [id]
            )
            return Feature(**result) if result else None
    
    async def list(self, skip: int = 0, limit: int = 10) -> List[Feature]:
        async with get_db() as db:
            results = await db.query(
                "SELECT * FROM features ORDER BY created_at DESC "
                "LIMIT %s OFFSET %s",
                [limit, skip]
            )
            return [Feature(**row) for row in results]
    
    async def create(self, feature: Feature) -> Feature:
        async with get_db() as db:
            await db.execute(
                """INSERT INTO features 
                   (id, requirement_id, name, complexity_points) 
                   VALUES (%s, %s, %s, %s)""",
                [feature.id, feature.requirement_id, 
                 feature.name, feature.complexity_points]
            )
        return feature
    
    async def update(self, id: str, feature: Feature) -> Feature:
        async with get_db() as db:
            await db.execute(
                """UPDATE features SET 
                   name = %s, 
                   complexity_points = %s,
                   updated_at = NOW()
                   WHERE id = %s""",
                [feature.name, feature.complexity_points, id]
            )
        return feature
    
    async def delete(self, id: str) -> bool:
        async with get_db() as db:
            result = await db.execute(
                "DELETE FROM features WHERE id = %s",
                [id]
            )
            return result.rowcount > 0

# Usage
repository = FeatureRepository()

feature = await repository.get("feat-1")
features = await repository.list(skip=0, limit=10)

new_feature = Feature(id="feat-new", name="New Feature", ...)
await repository.create(new_feature)

await repository.update("feat-1", updated_feature)
await repository.delete("feat-1")
```

---

### 2. Cache-Aside Pattern

**Definition:** Load data from cache if available, otherwise load from database and update cache.

**Implementation:**

```python
import redis
import json
from typing import Optional

class CacheAsideRepository(Repository):
    def __init__(self, cache: redis.Redis, cache_ttl: int = 3600):
        self.cache = cache
        self.cache_ttl = cache_ttl
    
    async def get(self, id: str) -> Optional[Feature]:
        # Try cache first
        cache_key = f"feature:{id}"
        cached = self.cache.get(cache_key)
        
        if cached:
            logger.info(f"Cache hit: {cache_key}")
            return Feature(**json.loads(cached))
        
        logger.info(f"Cache miss: {cache_key}")
        
        # Load from database
        feature = await super().get(id)
        
        if feature:
            # Update cache
            self.cache.setex(
                cache_key,
                self.cache_ttl,
                json.dumps(feature.dict())
            )
        
        return feature
    
    async def update(self, id: str, feature: Feature) -> Feature:
        # Update database
        updated = await super().update(id, feature)
        
        # Invalidate cache
        cache_key = f"feature:{id}"
        self.cache.delete(cache_key)
        
        logger.info(f"Cache invalidated: {cache_key}")
        
        return updated
    
    async def list(self, skip: int = 0, limit: int = 10) -> List[Feature]:
        cache_key = f"features:list:{skip}:{limit}"
        
        # Try cache
        cached = self.cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit: {cache_key}")
            data = json.loads(cached)
            return [Feature(**item) for item in data]
        
        # Load from database
        features = await super().list(skip, limit)
        
        # Update cache
        self.cache.setex(
            cache_key,
            self.cache_ttl,
            json.dumps([f.dict() for f in features])
        )
        
        return features
```

---

## 📚 Related Documents

- System Design (system_design.md)
- API Contracts (api_contracts.md)
- Data Modeling (data_modeling.md)
- Implementation Guide
- Code Examples

---

## 📝 Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Oct 26, 2024 | Architecture Team | Initial version |
| 1.1 | [TBD] | [Author] | Pattern additions |

---

**END OF DESIGN PATTERNS DOCUMENT**
