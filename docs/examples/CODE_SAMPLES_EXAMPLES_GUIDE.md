# Code Samples & Examples Management Guide

## Overview

This guide explains the process for adding code samples and examples from successfully completed projects to the `code_samples/` and `examples/` folders within the `docs/examples/` directory structure.

---

## 📁 Directory Structure

```
docs/examples/
├── complete_projects/          # Full project examples (3-5 complete projects)
│   ├── ai_chat_application/    # Example 1: Chat app with streaming
│   ├── ecommerce_platform/     # Example 2: Full e-commerce system
│   └── task_management_system/ # Example 3: Task management app
│
└── code_samples/               # Reusable code snippets by category
    ├── python/                 # Python code samples
    │   ├── backend/           # Backend patterns
    │   ├── streaming/         # Streaming implementations
    │   ├── database/          # Database operations
    │   └── utilities/         # Helper utilities
    ├── nodejs/                # Node.js/TypeScript samples
    │   ├── backend/           # Express, NestJS patterns
    │   ├── websocket/         # WebSocket implementations
    │   ├── queues/            # Queue processing
    │   └── middleware/        # Express/middleware patterns
    ├── react/                 # React code samples
    │   ├── hooks/             # Custom React hooks
    │   ├── streaming/         # Streaming response handling
    │   ├── state_management/  # Redux, Zustand patterns
    │   └── optimization/      # Performance optimization
    ├── mobile/                # Mobile development samples
    │   ├── react_native/      # React Native examples
    │   └── flutter/           # Flutter examples
    └── desktop/               # Desktop development samples
        ├── electron/          # Electron examples
        └── dotnet/            # .NET/WinForms examples
```

---

## 🔄 Process for Adding Code Samples

### Phase 1: Code Extraction & Preparation

#### Step 1.1: Identify Reusable Code
From completed projects, identify code that meets these criteria:

**Selection Criteria**:
- ✅ Solves a common problem
- ✅ Follows best practices
- ✅ Is well-commented and clear
- ✅ Can work independently
- ✅ Is 50-500 lines of code
- ✅ Has been tested in production

**Example Candidates**:
- Authentication implementations
- Streaming response handlers
- State management solutions
- Error handling patterns
- API integration methods
- Database query optimizations
- Performance optimizations

#### Step 1.2: Create Sample Metadata File

For each code sample, create a `{sample_name}.metadata.json`:

```json
{
  "name": "Streaming Response Handler",
  "filename": "streaming_response.py",
  "language": "Python",
  "category": "Backend/Streaming",
  "difficulty": "intermediate",
  "complexity_score": 3.5,
  "lines_of_code": 45,
  "estimated_read_time_minutes": 5,
  "estimated_implementation_time_minutes": 15,
  
  "description": "Handles streaming responses from AI models with proper error handling and timeout management",
  
  "use_cases": [
    "LLM streaming responses",
    "Server-sent events (SSE)",
    "Long-running API calls",
    "Real-time data feeds"
  ],
  
  "prerequisites": [
    "Python 3.8+",
    "async/await knowledge",
    "HTTP basics"
  ],
  
  "dependencies": [
    "aiohttp",
    "asyncio",
    "typing"
  ],
  
  "learning_outcomes": [
    "How to handle streaming responses",
    "Error handling in async contexts",
    "Timeout management",
    "Generator patterns in Python"
  ],
  
  "project_source": "AI Chat Application v2.1",
  "source_url": "https://github.com/company/ai-chat-app/blob/main/backend/streaming.py",
  "date_extracted": "2025-01-15",
  "extracted_by": "backend-team",
  
  "compatibility": {
    "frameworks": ["FastAPI", "Flask", "Django"],
    "python_versions": ["3.8", "3.9", "3.10", "3.11", "3.12"],
    "os": ["Linux", "macOS", "Windows"]
  },
  
  "performance_metrics": {
    "latency_ms": 2,
    "throughput_requests_per_second": 500,
    "memory_overhead_mb": 0.5
  },
  
  "related_samples": [
    "error_handling.py",
    "timeout_management.py",
    "async_patterns.py"
  ],
  
  "tags": [
    "streaming",
    "async",
    "error-handling",
    "production-ready",
    "tested"
  ]
}
```

#### Step 1.3: Code Preparation

Clean and refactor the code:

**Checklist**:
- ✅ Remove project-specific imports/configurations
- ✅ Replace hardcoded values with parameters
- ✅ Add comprehensive comments and docstrings
- ✅ Add type hints (where applicable)
- ✅ Include error handling
- ✅ Add example usage section
- ✅ Ensure consistent formatting
- ✅ Add license header

**Example Python Sample Structure**:
```python
"""
Streaming Response Handler

This module provides utilities for handling streaming responses from
AI models with proper error handling and timeout management.

Use Cases:
    - LLM streaming responses (OpenAI, Anthropic, etc.)
    - Server-sent events (SSE)
    - Long-running API calls
    - Real-time data feeds

Example:
    >>> import asyncio
    >>> handler = StreamingResponseHandler(timeout=30)
    >>> async for chunk in handler.stream_response(url):
    ...     print(chunk)
"""

import asyncio
import logging
from typing import AsyncGenerator, Optional, Dict, Any
from dataclasses import dataclass
import aiohttp

logger = logging.getLogger(__name__)


@dataclass
class StreamConfig:
    """Configuration for streaming handler."""
    timeout: int = 30
    chunk_size: int = 1024
    max_retries: int = 3
    retry_delay: float = 1.0


class StreamingResponseHandler:
    """Handle streaming responses with error handling and timeouts."""
    
    def __init__(self, config: Optional[StreamConfig] = None):
        """
        Initialize streaming handler.
        
        Args:
            config: StreamConfig instance for customization
        """
        self.config = config or StreamConfig()
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def stream_response(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream response from URL with error handling.
        
        Args:
            url: URL to stream from
            headers: HTTP headers
            params: Query parameters
        
        Yields:
            Response chunks as strings
            
        Raises:
            StreamingError: If streaming fails after retries
            
        Example:
            >>> async def process_stream():
            ...     async for chunk in handler.stream_response(url):
            ...         print(f"Received: {chunk}")
        """
        attempt = 0
        
        while attempt < self.config.max_retries:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        url,
                        headers=headers,
                        params=params,
                        timeout=aiohttp.ClientTimeout(total=self.config.timeout)
                    ) as response:
                        response.raise_for_status()
                        
                        async for chunk in response.content.iter_chunked(
                            self.config.chunk_size
                        ):
                            if chunk:
                                yield chunk.decode('utf-8', errors='replace')
                return
                
            except asyncio.TimeoutError:
                logger.warning(f"Timeout on attempt {attempt + 1}")
                attempt += 1
                if attempt < self.config.max_retries:
                    await asyncio.sleep(self.config.retry_delay)
                else:
                    raise StreamingError(f"Stream timeout after {attempt} attempts")
                    
            except aiohttp.ClientError as e:
                logger.error(f"Client error: {e}")
                attempt += 1
                if attempt < self.config.max_retries:
                    await asyncio.sleep(self.config.retry_delay)
                else:
                    raise StreamingError(f"Streaming failed: {e}")


class StreamingError(Exception):
    """Exception raised for streaming errors."""
    pass


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def main():
    """Example usage of StreamingResponseHandler."""
    config = StreamConfig(
        timeout=30,
        chunk_size=2048,
        max_retries=3
    )
    
    handler = StreamingResponseHandler(config)
    
    try:
        async for chunk in handler.stream_response(
            url="https://api.example.com/stream",
            headers={"Authorization": "Bearer token"}
        ):
            print(f"Received chunk: {chunk[:100]}...")
    except StreamingError as e:
        logger.error(f"Streaming failed: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
```

---

### Phase 2: Documentation

#### Step 2.1: Create Sample README

For each sample, create a comprehensive README:

```markdown
# Streaming Response Handler

## Overview
Brief description of what this code does and why it's useful.

## Key Features
- ✅ Async/await support
- ✅ Automatic retry logic
- ✅ Timeout management
- ✅ Error handling

## When to Use
- Building real-time applications
- Integrating with LLM APIs
- Streaming large datasets
- Server-sent events (SSE)

## When NOT to Use
- Simple request-response operations
- Small data transfers
- Synchronous-only applications

## Installation

### Prerequisites
- Python 3.8+
- asyncio library
- aiohttp library

### Setup
```bash
pip install aiohttp
```

## Usage

### Basic Example
```python
import asyncio
from streaming_response import StreamingResponseHandler

async def main():
    handler = StreamingResponseHandler()
    async for chunk in handler.stream_response("https://api.example.com/stream"):
        print(chunk)

asyncio.run(main())
```

### Advanced Configuration
```python
from streaming_response import StreamingResponseHandler, StreamConfig

config = StreamConfig(
    timeout=30,
    chunk_size=2048,
    max_retries=3,
    retry_delay=1.0
)

handler = StreamingResponseHandler(config)
```

## API Reference

### StreamingResponseHandler
Main class for handling streaming responses.

**Methods**:
- `stream_response(url, headers, params)` - Stream response from URL

**Example**:
```python
async for chunk in handler.stream_response(url):
    process(chunk)
```

### StreamConfig
Configuration dataclass for handler.

**Parameters**:
- `timeout` (int): Request timeout in seconds
- `chunk_size` (int): Size of each chunk
- `max_retries` (int): Maximum retry attempts
- `retry_delay` (float): Delay between retries

## Error Handling

The handler raises `StreamingError` for:
- Network timeouts
- HTTP errors
- Connection failures (after retries)

```python
try:
    async for chunk in handler.stream_response(url):
        process(chunk)
except StreamingError as e:
    logger.error(f"Streaming failed: {e}")
```

## Performance Considerations

- Chunk size affects memory usage vs throughput
- Larger chunks = more memory but faster processing
- Timeout should match expected response time
- Retry logic adds latency on failures

**Recommended settings**:
- Chunk size: 1024-4096 bytes
- Timeout: 30-60 seconds
- Max retries: 2-3 attempts

## Testing

```bash
pytest streaming_response_test.py -v
```

## Related Samples
- [Error Handling Patterns](../error_handling.py)
- [Async Patterns](../async_patterns.py)
- [Timeout Management](../timeout_management.py)

## Compatibility Matrix

| Python | aiohttp | Status |
|--------|---------|--------|
| 3.8    | 3.7+    | ✅     |
| 3.9    | 3.7+    | ✅     |
| 3.10   | 3.7+    | ✅     |
| 3.11   | 3.8+    | ✅     |
| 3.12   | 3.9+    | ✅     |

## License
MIT License - See LICENSE file

## Author
Backend Team - Extracted from AI Chat Application v2.1

## Last Updated
2025-01-15
```

#### Step 2.2: Add Comments & Docstrings

Ensure all code samples have:

```python
# Module-level docstring
"""
Brief description of module.

Detailed explanation of what this module does, how it works,
and when to use it.

Example:
    >>> from module import Function
    >>> result = Function(param)
"""

# Class docstring
class MyClass:
    """
    Brief description.
    
    Longer description explaining the purpose and usage.
    
    Attributes:
        attr1 (type): Description
        attr2 (type): Description
    
    Example:
        >>> obj = MyClass(param)
        >>> obj.method()
    """

# Method/function docstring
def my_function(param: str) -> int:
    """
    Brief description.
    
    Args:
        param (str): Description of parameter
    
    Returns:
        int: Description of return value
    
    Raises:
        ValueError: When something is invalid
    
    Example:
        >>> result = my_function("test")
        >>> print(result)
    """
```

---

### Phase 3: Testing & Validation

#### Step 3.1: Create Test File

Create `{sample_name}_test.py`:

```python
"""
Tests for Streaming Response Handler
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from streaming_response import (
    StreamingResponseHandler,
    StreamConfig,
    StreamingError
)


class TestStreamingResponseHandler:
    """Test StreamingResponseHandler class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.config = StreamConfig(timeout=5, chunk_size=1024)
        self.handler = StreamingResponseHandler(self.config)
    
    @pytest.mark.asyncio
    async def test_successful_stream(self):
        """Test successful streaming."""
        with patch('aiohttp.ClientSession') as mock_session:
            # Mock implementation
            pass
    
    @pytest.mark.asyncio
    async def test_timeout_handling(self):
        """Test timeout retry logic."""
        pass
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling."""
        pass
    
    def test_config_initialization(self):
        """Test StreamConfig initialization."""
        assert self.config.timeout == 5
        assert self.config.chunk_size == 1024


# Run tests: pytest streaming_response_test.py -v
```

#### Step 3.2: Validation Checklist

Before adding to repository, verify:

- ✅ Code runs without errors
- ✅ All tests pass
- ✅ No external dependencies on removed code
- ✅ Follows language style guide
- ✅ Proper error handling
- ✅ Comprehensive docstrings
- ✅ README is complete
- ✅ Metadata file is accurate
- ✅ No hardcoded credentials
- ✅ Performance is acceptable

---

### Phase 4: Integration into Repository

#### Step 4.1: Directory Setup

Create the following structure:

```
docs/examples/code_samples/python/
├── streaming/
│   ├── streaming_response.py
│   ├── streaming_response.metadata.json
│   ├── streaming_response_README.md
│   ├── streaming_response_test.py
│   └── streaming_response_example.py
```

#### Step 4.2: Create Comprehensive Example File

```python
"""
Complete working examples for Streaming Response Handler.

This file demonstrates various use cases and patterns.
"""

import asyncio
import logging
from streaming_response import StreamingResponseHandler, StreamConfig


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# EXAMPLE 1: Basic Usage
# ============================================================================

async def example_basic():
    """Basic streaming example."""
    handler = StreamingResponseHandler()
    
    try:
        async for chunk in handler.stream_response("https://api.example.com/stream"):
            print(f"Received: {chunk}")
    except Exception as e:
        logger.error(f"Error: {e}")


# ============================================================================
# EXAMPLE 2: Custom Configuration
# ============================================================================

async def example_custom_config():
    """Using custom configuration."""
    config = StreamConfig(
        timeout=60,
        chunk_size=4096,
        max_retries=5,
        retry_delay=2.0
    )
    
    handler = StreamingResponseHandler(config)
    
    async for chunk in handler.stream_response("https://api.example.com/stream"):
        process_chunk(chunk)


# ============================================================================
# EXAMPLE 3: Processing Chunks
# ============================================================================

async def example_chunk_processing():
    """Process each chunk as received."""
    handler = StreamingResponseHandler()
    
    buffer = ""
    async for chunk in handler.stream_response("https://api.example.com/stream"):
        buffer += chunk
        
        # Process complete lines
        if "\n" in buffer:
            lines = buffer.split("\n")
            buffer = lines[-1]
            
            for line in lines[:-1]:
                process_line(line)


# ============================================================================
# EXAMPLE 4: Timeout Handling
# ============================================================================

async def example_timeout_handling():
    """Handle timeouts gracefully."""
    config = StreamConfig(timeout=10, max_retries=3)
    handler = StreamingResponseHandler(config)
    
    try:
        async for chunk in handler.stream_response("https://slow-api.example.com/stream"):
            print(chunk)
    except TimeoutError:
        logger.error("Request timed out after retries")
    except Exception as e:
        logger.error(f"Streaming error: {e}")


# ============================================================================
# EXAMPLE 5: Multiple Streams
# ============================================================================

async def example_multiple_streams():
    """Handle multiple concurrent streams."""
    handler = StreamingResponseHandler()
    
    urls = [
        "https://api.example.com/stream1",
        "https://api.example.com/stream2",
        "https://api.example.com/stream3",
    ]
    
    tasks = [
        stream_and_process(handler, url)
        for url in urls
    ]
    
    await asyncio.gather(*tasks)


async def stream_and_process(handler, url):
    """Stream from URL and process chunks."""
    async for chunk in handler.stream_response(url):
        print(f"From {url}: {chunk}")


# ============================================================================
# Helper Functions
# ============================================================================

def process_chunk(chunk: str) -> None:
    """Process a single chunk."""
    logger.info(f"Processing chunk: {chunk[:50]}...")


def process_line(line: str) -> None:
    """Process a single line."""
    logger.info(f"Processing line: {line}")


# ============================================================================
# Main
# ============================================================================

async def main():
    """Run all examples."""
    logger.info("Running Example 1: Basic Usage")
    # await example_basic()
    
    logger.info("Running Example 2: Custom Configuration")
    # await example_custom_config()
    
    logger.info("Running Example 5: Multiple Streams")
    await example_multiple_streams()


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📋 Complete Projects Structure

### Complete Project Template

```
docs/examples/complete_projects/ai_chat_application/
├── README.md                    # Project overview
├── requirements.md              # Business requirements
├── architecture.md              # System architecture diagram
├── implementation_guide.md      # Step-by-step implementation
│
├── backend/
│   ├── models.py               # Database models
│   ├── api.py                  # API endpoints
│   ├── streaming.py            # Streaming logic
│   ├── middleware.py           # Middleware
│   ├── config.py               # Configuration
│   ├── utils.py                # Utilities
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile              # Container configuration
│   └── tests/
│       ├── test_api.py
│       ├── test_streaming.py
│       └── test_utils.py
│
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── hooks/              # Custom hooks
│   │   ├── services/           # API services
│   │   ├── store/              # State management
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   ├── Dockerfile
│   ├── .env.example
│   └── tests/
│       ├── components.test.tsx
│       └── hooks.test.ts
│
├── deployment/
│   ├── docker-compose.yml      # Local development
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── ingress.yaml
│   ├── terraform/              # Infrastructure as Code
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── .github/workflows/
│   │   ├── ci.yml
│   │   └── deploy.yml
│   └── nginx/
│       └── nginx.conf
│
├── database/
│   ├── schema.sql              # Database schema
│   ├── migrations/
│   │   ├── 001_init.sql
│   │   └── 002_add_features.sql
│   └── seed_data.sql           # Test data
│
├── docs/
│   ├── API.md                  # API documentation
│   ├── DATABASE.md             # Database documentation
│   ├── DEPLOYMENT.md           # Deployment guide
│   └── TROUBLESHOOTING.md      # Troubleshooting guide
│
├── .env.example
├── LICENSE
└── CONTRIBUTING.md
```

### Complete Project README Template

```markdown
# AI Chat Application

## Overview
A production-ready chat application with real-time streaming responses, built with FastAPI, React, and WebSockets.

## Key Features
- ✅ Real-time streaming responses
- ✅ User authentication
- ✅ Message history
- ✅ Multiple models support
- ✅ Scalable architecture
- ✅ Containerized deployment

## Architecture

### Components
- **Backend**: FastAPI server with async streaming
- **Frontend**: React SPA with real-time updates
- **Database**: PostgreSQL with migrations
- **Cache**: Redis for session management
- **Message Queue**: RabbitMQ for async tasks

### Technology Stack
- Backend: Python 3.11, FastAPI, SQLAlchemy, Pydantic
- Frontend: React 18, TypeScript, Redux, Socket.io
- Database: PostgreSQL 14
- Cache: Redis 7
- Deployment: Docker, Kubernetes, Terraform
- CI/CD: GitHub Actions

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Local Development

1. **Clone repository**
   ```bash
   git clone <repo>
   cd ai-chat-application
   ```

2. **Set up environment**
   ```bash
   cp .env.example .env
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **Run migrations**
   ```bash
   docker-compose exec backend python -m alembic upgrade head
   ```

5. **Access application**
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

### Project Structure

See `architecture.md` for detailed system design.

## Usage

### API Examples

#### Start Chat Session
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

#### Stream Response
```bash
curl -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me a story"}' \
  --stream
```

### Frontend Examples

See `frontend/docs/` for React component examples.

## Deployment

### Docker Compose (Local)
```bash
docker-compose up
```

### Kubernetes (Production)
```bash
kubectl apply -f deployment/kubernetes/
```

### Terraform (Infrastructure)
```bash
cd deployment/terraform
terraform init
terraform plan
terraform apply
```

## Testing

```bash
# Backend tests
pytest backend/tests -v

# Frontend tests
npm test

# Integration tests
pytest tests/integration -v

# Performance tests
pytest tests/performance -v
```

## Monitoring & Logging

- **Logs**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Metrics**: Prometheus & Grafana
- **APM**: New Relic or DataDog

## Performance

- API response time: < 200ms (p95)
- Streaming latency: < 100ms (p95)
- Throughput: 1000+ concurrent users
- Database queries: < 50ms (p95)

## Security

- ✅ HTTPS/TLS encryption
- ✅ JWT authentication
- ✅ Rate limiting
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ CORS configuration

See `docs/SECURITY.md` for detailed security measures.

## Troubleshooting

Common issues and solutions in `docs/TROUBLESHOOTING.md`

## Contributing

See `CONTRIBUTING.md` for contribution guidelines.

## License

MIT License - See LICENSE file

## Support

- Documentation: See `/docs` folder
- Issues: GitHub Issues
- Discussions: GitHub Discussions
```

---

## 🔍 Indexing & Discovery

### Create Master Index File

```markdown
# Code Samples & Examples Index

## Quick Navigation

### By Language
- [Python Samples](#python-samples)
- [Node.js/TypeScript Samples](#nodejs-samples)
- [React Samples](#react-samples)
- [Mobile Samples](#mobile-samples)
- [Desktop Samples](#desktop-samples)

### By Category
- [Backend Patterns](#backend-patterns)
- [Frontend Patterns](#frontend-patterns)
- [Integration Patterns](#integration-patterns)
- [Testing Patterns](#testing-patterns)

### By Difficulty
- [Beginner](#beginner)
- [Intermediate](#intermediate)
- [Advanced](#advanced)

---

## Complete Projects

| Project | Tech Stack | Difficulty | Status |
|---------|-----------|-----------|--------|
| [AI Chat Application](./complete_projects/ai_chat_application/) | FastAPI, React, WebSocket | Intermediate | ✅ Complete |
| [E-Commerce Platform](./complete_projects/ecommerce_platform/) | Django, Vue.js, Stripe | Intermediate | ✅ Complete |
| [Task Management System](./complete_projects/task_management_system/) | Express, React, MongoDB | Beginner | ✅ Complete |

---

## Python Samples

### Backend Patterns
- [Streaming Response Handler](./code_samples/python/backend/streaming_response.py) - Handle LLM streaming
- [Database Connection Pool](./code_samples/python/backend/db_pool.py) - Connection management
- [API Rate Limiter](./code_samples/python/backend/rate_limiter.py) - Rate limiting

### Streaming Implementations
- [Server-Sent Events](./code_samples/python/streaming/sse_handler.py) - SSE patterns
- [WebSocket Handler](./code_samples/python/streaming/websocket_handler.py) - WebSocket patterns

### Database Operations
- [Query Optimization](./code_samples/python/database/query_optimization.py) - Efficient queries
- [Batch Operations](./code_samples/python/database/batch_operations.py) - Bulk processing

### Utilities
- [Error Handling](./code_samples/python/utilities/error_handler.py) - Error management
- [Logging Configuration](./code_samples/python/utilities/logging_setup.py) - Structured logging

---

## Node.js/TypeScript Samples

### Backend Patterns
- [Express Middleware](./code_samples/nodejs/backend/middleware.ts) - Custom middleware
- [Async Error Handling](./code_samples/nodejs/backend/async_handler.ts) - Error wrapping

### WebSocket Implementations
- [Socket.io Server](./code_samples/nodejs/websocket/socket_server.ts) - Socket.io setup
- [Real-time Updates](./code_samples/nodejs/websocket/realtime_updates.ts) - Real-time patterns

### Queue Processing
- [RabbitMQ Consumer](./code_samples/nodejs/queues/rabbitmq_consumer.ts) - Message queues
- [Batch Processor](./code_samples/nodejs/queues/batch_processor.ts) - Batch processing

---

## React Samples

### Custom Hooks
- [useStreamingResponse](./code_samples/react/hooks/useStreamingResponse.ts) - Streaming hook
- [usePaginaton](./code_samples/react/hooks/usePagination.ts) - Pagination hook
- [useLocalStorage](./code_samples/react/hooks/useLocalStorage.ts) - Local storage hook

### Streaming Response Handling
- [StreamingChat Component](./code_samples/react/streaming/StreamingChat.tsx) - Chat interface
- [StreamController](./code_samples/react/streaming/StreamController.ts) - Response controller

### State Management
- [Redux Middleware](./code_samples/react/state_management/reduxMiddleware.ts) - Redux setup
- [Zustand Store](./code_samples/react/state_management/zustandStore.ts) - Zustand setup

---

## Mobile Samples

### React Native
- [Navigation Setup](./code_samples/mobile/react_native/navigation.ts) - React Navigation
- [API Integration](./code_samples/mobile/react_native/api_client.ts) - API calls

### Flutter
- [State Management](./code_samples/mobile/flutter/state_management.dart) - Provider pattern
- [HTTP Client](./code_samples/mobile/flutter/http_client.dart) - Dio client

---

## Filter & Search

### Filters
- **Language**: Python, Node.js, React, Kotlin, Swift, etc.
- **Framework**: FastAPI, Express, Django, etc.
- **Category**: Backend, Frontend, Database, etc.
- **Difficulty**: Beginner, Intermediate, Advanced
- **Tags**: async, streaming, real-time, testing, etc.

### Search Examples
```
Query: "streaming python"
Results: Streaming Response Handler, SSE Handler, WebSocket Handler

Query: "react hooks"
Results: useStreamingResponse, usePagination, useLocalStorage

Query: "error handling"
Results: Error Handler, Async Error Handler, Exception Handling
```

---

## Stats

| Metric | Count |
|--------|-------|
| Complete Projects | 3 |
| Python Samples | 12+ |
| Node.js Samples | 8+ |
| React Samples | 10+ |
| Mobile Samples | 6+ |
| Total Code Lines | 5000+ |
| Total Examples | 40+ |

---

## Contributing

Want to add your code sample? See [CONTRIBUTING.md](../../CONTRIBUTING.md)
```

---

## 📊 Tracking & Metrics

### Create Metadata Registry

```json
{
  "registry": {
    "version": "1.0",
    "last_updated": "2025-01-15",
    "total_samples": 40,
    "total_projects": 3,
    
    "by_language": {
      "python": 12,
      "nodejs": 8,
      "react": 10,
      "mobile": 6,
      "desktop": 4
    },
    
    "by_difficulty": {
      "beginner": 10,
      "intermediate": 20,
      "advanced": 10
    },
    
    "by_status": {
      "production_ready": 35,
      "in_development": 3,
      "deprecated": 2
    },
    
    "samples": [
      {
        "id": "py_streaming_001",
        "name": "Streaming Response Handler",
        "language": "Python",
        "category": "Backend/Streaming",
        "difficulty": "Intermediate",
        "created": "2025-01-15",
        "last_updated": "2025-01-15",
        "downloads": 234,
        "rating": 4.8,
        "usage_count": 156,
        "status": "production_ready"
      }
    ]
  }
}
```

---

## ✅ Quality Standards Checklist

Before publishing a code sample:

### Code Quality
- [ ] Follows language style guide
- [ ] Passes linter checks
- [ ] Has comprehensive error handling
- [ ] Includes type hints (if applicable)
- [ ] All tests pass
- [ ] No security vulnerabilities

### Documentation
- [ ] README.md is complete
- [ ] Code comments explain logic
- [ ] Docstrings for all public functions
- [ ] At least 3 usage examples
- [ ] Prerequisites clearly listed
- [ ] Related samples linked

### Testing
- [ ] Unit tests provided (80%+ coverage)
- [ ] Integration tests provided
- [ ] Manual testing completed
- [ ] Performance tested
- [ ] Edge cases handled

### Metadata
- [ ] metadata.json is complete
- [ ] Tags are relevant and searchable
- [ ] Difficulty level accurate
- [ ] Compatibility matrix included
- [ ] Performance metrics included

### Security
- [ ] No hardcoded credentials
- [ ] No sensitive data in code
- [ ] Follows OWASP guidelines
- [ ] Input validation present
- [ ] Error messages don't leak info

### Usability
- [ ] Clear purpose and use cases
- [ ] Easy to understand
- [ ] Can be used independently
- [ ] Well-organized code structure
- [ ] Proper error messages

---

## 🚀 Publishing Workflow

### Step 1: Preparation
```bash
# 1. Extract code from project
# 2. Clean and refactor
# 3. Add comprehensive documentation
# 4. Create test file
# 5. Create examples file
```

### Step 2: Validation
```bash
# Run all tests
pytest code_samples/python/streaming/ -v

# Check code quality
pylint code_samples/python/streaming/

# Verify documentation
markdownlint code_samples/python/streaming/*.md

# Validate metadata
python scripts/validate_metadata.py
```

### Step 3: Integration
```bash
# 1. Create directory structure
# 2. Copy files to appropriate location
# 3. Add to metadata registry
# 4. Update index files
# 5. Commit to repository
```

### Step 4: Publication
```bash
# 1. Create GitHub release
# 2. Post announcement
# 3. Update website
# 4. Add to distribution channels
```

---

## 📚 File Naming Conventions

```
{sample_name}_{type}.{extension}

Examples:
- streaming_response.py           # Main implementation
- streaming_response_test.py       # Tests
- streaming_response_example.py    # Usage examples
- streaming_response_README.md     # Documentation
- streaming_response.metadata.json # Metadata
```

---

## 🔗 Integration Points

### Link in Main Documentation
```markdown
## Related Code Samples
- [Streaming Response Handler](../code_samples/python/streaming/streaming_response.py)
- [Error Handling Patterns](../code_samples/python/utilities/error_handler.py)
```

### Link in Agent Prompts
```markdown
## Recommended Code Samples
For implementing {feature}:
1. [Sample 1](link)
2. [Sample 2](link)
3. [Sample 3](link)
```

### Automated Discovery
- Search functionality indexes all samples
- Filters by language, category, difficulty
- Download tracking
- Usage statistics

---

## ✨ Best Practices

1. **Keep samples focused** - One responsibility per file
2. **Comprehensive documentation** - Make it easy to use
3. **Real-world examples** - Show practical applications
4. **Error handling** - Handle edge cases gracefully
5. **Performance considerations** - Discuss trade-offs
6. **Testing** - Include test suite
7. **Comments** - Explain complex logic
8. **Versioning** - Track compatibility
9. **Maintenance** - Keep up with latest practices
10. **Community feedback** - Listen and improve

---

## 📝 Maintenance Schedule

| Task | Frequency | Owner |
|------|-----------|-------|
| Update compatibility matrix | Quarterly | Tech Lead |
| Review security | Monthly | Security Team |
| Verify working examples | Quarterly | Dev Team |
| Update dependencies | As needed | Maintainers |
| Collect feedback | Continuous | Community |
| Publish new samples | Weekly | Contributors |

---

**Version**: 1.0  
**Last Updated**: 2025-01-15  
**Maintained By**: Development Team
