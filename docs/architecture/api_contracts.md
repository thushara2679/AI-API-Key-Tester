# API Contracts Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Last Updated:** October 26, 2024
**Document Type:** API Specification
**API Format:** OpenAPI 3.0 / REST
**Base URL:** `https://api.example.com/v1`

---

## 📖 Introduction

This document specifies all REST API contracts for the AI Agent System. It includes request/response schemas, authentication mechanisms, error handling, rate limiting, and comprehensive examples.

---

## 🔐 Authentication & Authorization

### Authentication Methods

```yaml
Authentication:
  OAuth 2.0:
    - Authorization Code Flow (web apps)
    - Client Credentials Flow (service-to-service)
    - Refresh Token Flow (long-lived sessions)
  
  JWT Tokens:
    - HS256 (symmetric) for signing
    - RS256 (asymmetric) for verification
    - Issued by auth service
    - TTL: 1 hour (access), 30 days (refresh)
  
  API Keys:
    - For service-to-service communication
    - Rate limited per API key
    - Revocable

All APIs require:
  Authorization: Bearer <jwt_token>
  OR
  X-API-Key: <api_key>
```

### JWT Token Format

```json
{
  "sub": "user-uuid",
  "org": "organization-uuid",
  "email": "user@example.com",
  "role": "developer",
  "permissions": ["projects:read", "projects:write", "deployments:read"],
  "iat": 1698336000,
  "exp": 1698339600,
  "iss": "https://auth.example.com"
}
```

### Authorization Scopes

```yaml
Scopes:
  organizations:
    - organizations:read
    - organizations:write
    - organizations:admin
  
  projects:
    - projects:read
    - projects:write
    - projects:delete
    - projects:admin
  
  features:
    - features:read
    - features:write
    - features:delete
  
  tests:
    - tests:read
    - tests:write
    - tests:execute
  
  deployments:
    - deployments:read
    - deployments:write
    - deployments:approve
  
  security:
    - security:read
    - security:write
    - security:admin
```

---

## 📊 API Response Format

### Standard Response Structure

```json
{
  "success": true,
  "status": 200,
  "data": {},
  "meta": {
    "timestamp": "2024-10-26T10:30:00Z",
    "request_id": "req-uuid-12345",
    "version": "1.0"
  }
}
```

### Paginated Response

```json
{
  "success": true,
  "status": 200,
  "data": [
    { "id": "1", "name": "Item 1" },
    { "id": "2", "name": "Item 2" }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 150,
    "pages": 8,
    "has_next": true,
    "has_prev": false
  },
  "meta": {
    "timestamp": "2024-10-26T10:30:00Z",
    "request_id": "req-uuid-12345"
  }
}
```

### Error Response

```json
{
  "success": false,
  "status": 400,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "email",
        "message": "Email format invalid"
      },
      {
        "field": "password",
        "message": "Password must be at least 8 characters"
      }
    ]
  },
  "meta": {
    "timestamp": "2024-10-26T10:30:00Z",
    "request_id": "req-uuid-12345"
  }
}
```

---

## 📌 Core API Endpoints

### 1. Organizations

#### GET /organizations

```yaml
Summary: List organizations (admin only)
Security: Bearer token required
Permissions: organizations:read

Query Parameters:
  - page: integer (default: 1)
  - page_size: integer (default: 20, max: 100)
  - status: enum (active, inactive, suspended)
  - search: string (search by name or slug)
  - sort_by: enum (name, created_at, updated_at)
  - sort_order: enum (asc, desc)

Response:
  200: Success
    data: Organization[]
    pagination: PaginationInfo
  
  401: Unauthorized
  403: Forbidden
  429: Rate Limited

Example Request:
  GET /organizations?page=1&page_size=10&status=active

Example Response:
  {
    "success": true,
    "status": 200,
    "data": [
      {
        "id": "org-uuid-1",
        "name": "Acme Corp",
        "slug": "acme-corp",
        "type": "enterprise",
        "plan": "enterprise",
        "status": "active",
        "max_users": 500,
        "max_projects": 100,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-10-26T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 10,
      "total": 42,
      "pages": 5,
      "has_next": true,
      "has_prev": false
    }
  }
```

#### POST /organizations

```yaml
Summary: Create new organization
Security: Bearer token required (must be admin)
Permissions: organizations:write

Request Body:
  name: string (required, min: 2, max: 255)
  slug: string (required, pattern: ^[a-z0-9-]+$)
  type: enum (enterprise, startup, nonprofit)
  description: string (optional)
  website_url: string (optional, format: url)
  plan: enum (free, professional, enterprise)
  max_users: integer (default: 10)
  max_projects: integer (default: 5)

Response:
  201: Created
    data: Organization
  
  400: Validation Error
    error.code: VALIDATION_ERROR
  
  409: Conflict
    error.code: DUPLICATE_SLUG
  
  429: Rate Limited

Example Request:
  POST /organizations
  {
    "name": "TechStart Inc",
    "slug": "techstart-inc",
    "type": "startup",
    "plan": "professional",
    "max_users": 50,
    "max_projects": 10
  }

Example Response (201):
  {
    "success": true,
    "status": 201,
    "data": {
      "id": "org-uuid-new",
      "name": "TechStart Inc",
      "slug": "techstart-inc",
      "type": "startup",
      "plan": "professional",
      "status": "active",
      "max_users": 50,
      "max_projects": 10,
      "created_at": "2024-10-26T10:30:00Z",
      "updated_at": "2024-10-26T10:30:00Z"
    }
  }
```

---

### 2. Projects

#### GET /organizations/:org_id/projects

```yaml
Summary: List projects for organization
Security: Bearer token required
Permissions: projects:read

Path Parameters:
  org_id: UUID (required)

Query Parameters:
  - page: integer (default: 1)
  - page_size: integer (default: 20, max: 100)
  - status: enum (active, archived, deleted)
  - search: string (search by name)
  - sort_by: enum (name, created_at, updated_at)

Response:
  200: Success
    data: Project[]
  
  401: Unauthorized
  403: Forbidden (no access to org)
  404: Organization not found
  429: Rate Limited

Example Response:
  {
    "success": true,
    "status": 200,
    "data": [
      {
        "id": "proj-uuid-1",
        "organization_id": "org-uuid-1",
        "name": "Backend API",
        "slug": "backend-api",
        "description": "Core API services",
        "repository_url": "https://github.com/acme/backend-api",
        "status": "active",
        "visibility": "private",
        "owner_id": "user-uuid-1",
        "tech_stack": ["python", "fastapi", "postgresql"],
        "created_at": "2024-01-15T00:00:00Z",
        "updated_at": "2024-10-26T10:30:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 5,
      "pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
```

#### POST /organizations/:org_id/projects

```yaml
Summary: Create new project
Security: Bearer token required
Permissions: projects:write

Request Body:
  name: string (required, min: 2, max: 255)
  slug: string (required)
  description: string (optional)
  repository_url: string (required, format: url)
  repository_type: enum (git, svn)
  visibility: enum (private, internal, public)
  template_type: enum (microservice, monolith, mobile, web)
  tech_stack: string[] (optional)

Response:
  201: Created
    data: Project
  
  400: Validation Error
  404: Organization not found
  429: Rate Limited

Example Request:
  POST /organizations/org-uuid-1/projects
  {
    "name": "Frontend Web App",
    "slug": "frontend-web",
    "description": "React-based web application",
    "repository_url": "https://github.com/acme/frontend-web",
    "repository_type": "git",
    "visibility": "private",
    "template_type": "web",
    "tech_stack": ["react", "typescript", "webpack"]
  }
```

---

### 3. Requirements

#### POST /projects/:project_id/requirements

```yaml
Summary: Create requirement (triggered by business analyzer)
Security: Bearer token required
Permissions: features:write

Request Body:
  title: string (required, min: 3)
  description: string (required)
  user_stories: object[] (optional)
    - title: string
    - description: string
    - acceptance_criteria: string[]
  acceptance_criteria: string[] (required, min: 1)
  priority: enum (critical, high, medium, low)
  estimated_effort_points: integer (optional)
  tags: string[] (optional)

Response:
  201: Created
    data: Requirement
  
  400: Validation Error
  404: Project not found
  429: Rate Limited

Example Request:
  POST /projects/proj-uuid-1/requirements
  {
    "title": "User Authentication System",
    "description": "Implement OAuth 2.0 authentication...",
    "user_stories": [
      {
        "title": "User Login",
        "description": "As a user, I want to login...",
        "acceptance_criteria": [
          "User can enter email and password",
          "User receives JWT token on success"
        ]
      }
    ],
    "acceptance_criteria": [
      "OAuth 2.0 implemented",
      "JWT tokens issued correctly",
      "Refresh token flow working"
    ],
    "priority": "critical",
    "estimated_effort_points": 13
  }

Example Response (201):
  {
    "success": true,
    "status": 201,
    "data": {
      "id": "req-uuid-new",
      "project_id": "proj-uuid-1",
      "title": "User Authentication System",
      "description": "...",
      "acceptance_criteria": [...],
      "priority": "critical",
      "status": "draft",
      "estimated_effort_points": 13,
      "created_by": "user-uuid-business-analyzer",
      "created_at": "2024-10-26T10:30:00Z",
      "updated_at": "2024-10-26T10:30:00Z"
    }
  }
```

---

### 4. Features

#### POST /requirements/:requirement_id/features

```yaml
Summary: Create feature (triggered by backend developer agent)
Security: Bearer token required
Permissions: features:write

Request Body:
  name: string (required, min: 2)
  description: string (required)
  implementation_notes: string (optional)
  complexity_points: integer (1-13)
  developer_id: UUID (optional)

Response:
  201: Created
    data: Feature
  
  400: Validation Error
  404: Requirement not found
  429: Rate Limited

Example Request:
  POST /requirements/req-uuid-1/features
  {
    "name": "OAuth 2.0 Integration",
    "description": "Implement OAuth 2.0 provider integration",
    "complexity_points": 8,
    "implementation_notes": "Use python-social-auth library"
  }

Example Response:
  {
    "success": true,
    "status": 201,
    "data": {
      "id": "feat-uuid-new",
      "requirement_id": "req-uuid-1",
      "name": "OAuth 2.0 Integration",
      "description": "...",
      "implementation_status": "not_started",
      "complexity_points": 8,
      "created_at": "2024-10-26T10:30:00Z",
      "updated_at": "2024-10-26T10:30:00Z"
    }
  }
```

#### PATCH /features/:feature_id/status

```yaml
Summary: Update feature implementation status
Security: Bearer token required
Permissions: features:write

Request Body:
  status: enum (not_started, in_progress, completed, blocked)
  blocked_reason: string (required if status == blocked)

Response:
  200: Success
    data: Feature
  
  400: Validation Error
  404: Feature not found
  429: Rate Limited

Example Request:
  PATCH /features/feat-uuid-1/status
  {
    "status": "in_progress"
  }
```

---

### 5. Test Cases & Results

#### POST /features/:feature_id/tests

```yaml
Summary: Create test case (triggered by testing engineer agent)
Security: Bearer token required
Permissions: tests:write

Request Body:
  name: string (required, min: 3)
  description: string (required)
  test_type: enum (unit, integration, e2e, performance, security)
  priority: enum (critical, high, medium, low)
  steps: object[] (required)
    - step_number: integer
    - action: string
    - expected_result: string
  expected_result: string (required)
  automated: boolean (default: false)
  automation_tool: string (optional)
  automation_script_path: string (optional)

Response:
  201: Created
    data: TestCase
  
  400: Validation Error
  404: Feature not found
  429: Rate Limited

Example Request:
  POST /features/feat-uuid-1/tests
  {
    "name": "OAuth Login Flow",
    "description": "Test complete OAuth login process",
    "test_type": "e2e",
    "priority": "critical",
    "steps": [
      {
        "step_number": 1,
        "action": "Navigate to login page",
        "expected_result": "Login form displayed"
      },
      {
        "step_number": 2,
        "action": "Click OAuth button",
        "expected_result": "Redirected to OAuth provider"
      },
      {
        "step_number": 3,
        "action": "Authenticate and authorize",
        "expected_result": "Redirected back with token"
      }
    ],
    "expected_result": "User logged in successfully",
    "automated": true,
    "automation_tool": "cypress",
    "automation_script_path": "tests/e2e/oauth-login.cy.js"
  }
```

#### POST /testcases/:testcase_id/results

```yaml
Summary: Record test result (triggered by testing engineer agent)
Security: Bearer token required
Permissions: tests:write

Request Body:
  status: enum (passed, failed, skipped, error)
  duration_ms: integer
  error_message: string (optional)
  assertions_run: integer
  assertions_passed: integer
  assertions_failed: integer
  code_coverage_percent: decimal (optional)
  logs: object[] (optional)

Response:
  201: Created
    data: TestResult
  
  400: Validation Error
  429: Rate Limited

Example Request:
  POST /testcases/test-uuid-1/results
  {
    "status": "passed",
    "duration_ms": 1250,
    "assertions_run": 5,
    "assertions_passed": 5,
    "assertions_failed": 0,
    "code_coverage_percent": 92.5
  }

Example Response:
  {
    "success": true,
    "status": 201,
    "data": {
      "id": "result-uuid-new",
      "test_case_id": "test-uuid-1",
      "status": "passed",
      "duration_ms": 1250,
      "assertions_run": 5,
      "assertions_passed": 5,
      "assertions_failed": 0,
      "code_coverage_percent": 92.5,
      "executed_at": "2024-10-26T10:30:00Z",
      "created_at": "2024-10-26T10:30:00Z"
    }
  }
```

---

### 6. Builds

#### POST /features/:feature_id/builds

```yaml
Summary: Create build (triggered by deployment engineer)
Security: Bearer token required
Permissions: deployments:write

Request Body:
  version_tag: string (required, format: semver)
  git_commit_hash: string (required)
  git_branch: string (required)
  docker_image_url: string (optional)
  tests_passed: integer (optional)
  tests_failed: integer (optional)
  code_coverage_percent: decimal (optional)
  security_scan_status: enum (passed, failed, warnings)

Response:
  201: Created
    data: Build
  
  400: Validation Error
  429: Rate Limited

Example Request:
  POST /features/feat-uuid-1/builds
  {
    "version_tag": "1.2.0",
    "git_commit_hash": "abc123def456",
    "git_branch": "main",
    "docker_image_url": "registry.example.com/project:1.2.0",
    "tests_passed": 245,
    "tests_failed": 0,
    "code_coverage_percent": 88.5,
    "security_scan_status": "passed"
  }

Example Response:
  {
    "success": true,
    "status": 201,
    "data": {
      "id": "build-uuid-new",
      "feature_id": "feat-uuid-1",
      "build_number": 42,
      "version_tag": "1.2.0",
      "status": "success",
      "tests_passed": 245,
      "tests_failed": 0,
      "code_coverage_percent": 88.5,
      "security_scan_status": "passed",
      "completed_at": "2024-10-26T10:30:00Z",
      "created_at": "2024-10-26T10:30:00Z"
    }
  }
```

#### GET /builds/:build_id

```yaml
Summary: Get build details
Security: Bearer token required
Permissions: deployments:read

Response:
  200: Success
    data: Build (with full details)
  
  404: Build not found
  429: Rate Limited

Example Response:
  {
    "success": true,
    "status": 200,
    "data": {
      "id": "build-uuid-1",
      "feature_id": "feat-uuid-1",
      "project_id": "proj-uuid-1",
      "build_number": 42,
      "version_tag": "1.2.0",
      "git_commit_hash": "abc123def456",
      "git_branch": "main",
      "status": "success",
      "docker_image_url": "registry.example.com/project:1.2.0",
      "docker_image_size_bytes": 524288000,
      "tests_run": 245,
      "tests_passed": 245,
      "tests_failed": 0,
      "code_coverage_percent": 88.5,
      "vulnerabilities_critical": 0,
      "vulnerabilities_high": 0,
      "vulnerabilities_medium": 1,
      "vulnerabilities_low": 3,
      "started_at": "2024-10-26T10:00:00Z",
      "completed_at": "2024-10-26T10:30:00Z",
      "duration_seconds": 1800
    }
  }
```

---

### 7. Deployments

#### POST /builds/:build_id/deploy

```yaml
Summary: Deploy build to environment
Security: Bearer token required
Permissions: deployments:write (and deployments:approve for production)

Request Body:
  environment: enum (dev, staging, production)
  deployment_strategy: enum (blue_green, canary, rolling, ramp)
  canary_percentage: integer (0-100, required for canary)
  approval_notes: string (required for production)

Response:
  201: Accepted
    data: Deployment
  
  400: Validation Error
  404: Build not found
  403: Forbidden (insufficient permissions for environment)
  429: Rate Limited

Example Request:
  POST /builds/build-uuid-1/deploy
  {
    "environment": "production",
    "deployment_strategy": "blue_green",
    "approval_notes": "Approved for production release v1.2.0"
  }

Example Response:
  {
    "success": true,
    "status": 201,
    "data": {
      "id": "deploy-uuid-new",
      "build_id": "build-uuid-1",
      "environment": "production",
      "status": "pending",
      "deployment_strategy": "blue_green",
      "health_check_status": null,
      "created_at": "2024-10-26T10:30:00Z",
      "updated_at": "2024-10-26T10:30:00Z"
    }
  }
```

#### GET /deployments/:deployment_id

```yaml
Summary: Get deployment status
Security: Bearer token required
Permissions: deployments:read

Response:
  200: Success
    data: Deployment (with full details)
  
  404: Deployment not found
  429: Rate Limited

Example Response:
  {
    "success": true,
    "status": 200,
    "data": {
      "id": "deploy-uuid-1",
      "build_id": "build-uuid-1",
      "environment": "production",
      "status": "success",
      "deployment_strategy": "blue_green",
      "started_at": "2024-10-26T10:30:00Z",
      "completed_at": "2024-10-26T10:45:00Z",
      "duration_seconds": 900,
      "health_check_status": "healthy",
      "error_rate_percent": 0.01,
      "performance_metrics": {
        "p95_response_time_ms": 245,
        "throughput_rps": 12500,
        "error_rate_percent": 0.01
      }
    }
  }
```

#### POST /deployments/:deployment_id/rollback

```yaml
Summary: Rollback deployment
Security: Bearer token required
Permissions: deployments:write

Request Body:
  reason: string (required)

Response:
  200: Success
    data: Deployment (rolled back)
  
  400: Invalid state for rollback
  404: Deployment not found
  429: Rate Limited

Example Request:
  POST /deployments/deploy-uuid-1/rollback
  {
    "reason": "High error rate detected post-deployment"
  }

Example Response:
  {
    "success": true,
    "status": 200,
    "data": {
      "id": "deploy-uuid-1",
      "status": "rolled_back",
      "rollback_reason": "High error rate detected post-deployment",
      "rolled_back_at": "2024-10-26T10:50:00Z"
    }
  }
```

---

### 8. Monitoring & Health

#### GET /health

```yaml
Summary: System health check (public endpoint)
Security: None required

Response:
  200: Healthy
  503: Unhealthy

Example Response (200):
  {
    "status": "healthy",
    "timestamp": "2024-10-26T10:30:00Z",
    "services": {
      "database": "healthy",
      "cache": "healthy",
      "message_queue": "healthy",
      "storage": "healthy"
    },
    "version": "1.2.0"
  }

Example Response (503):
  {
    "status": "unhealthy",
    "timestamp": "2024-10-26T10:30:00Z",
    "services": {
      "database": "unhealthy",
      "cache": "healthy",
      "message_queue": "healthy",
      "storage": "healthy"
    },
    "errors": ["Database connection failed"]
  }
```

#### GET /metrics

```yaml
Summary: Get system metrics
Security: Bearer token required
Permissions: metrics:read

Query Parameters:
  - time_range: enum (1h, 6h, 24h, 7d, 30d)
  - aggregation: enum (1m, 5m, 1h)

Response:
  200: Success
    data: Metrics

Example Response:
  {
    "success": true,
    "status": 200,
    "data": {
      "timestamp": "2024-10-26T10:30:00Z",
      "time_range": "1h",
      "aggregation": "1m",
      "metrics": {
        "api_requests_total": 125000,
        "api_latency_p50_ms": 145,
        "api_latency_p95_ms": 380,
        "api_latency_p99_ms": 650,
        "error_rate_percent": 0.05,
        "database_query_count": 450000,
        "database_slow_queries": 12,
        "cache_hit_rate": 92.5,
        "cpu_percent": 45.2,
        "memory_percent": 62.1
      }
    }
  }
```

---

## ⚠️ Error Codes & Handling

### Standard HTTP Status Codes

```yaml
2xx Success:
  200: OK (successful GET, PATCH, DELETE)
  201: Created (successful POST)
  204: No Content (successful DELETE returning no data)

4xx Client Errors:
  400: Bad Request (validation error)
  401: Unauthorized (missing/invalid auth)
  403: Forbidden (insufficient permissions)
  404: Not Found (resource doesn't exist)
  409: Conflict (resource already exists)
  422: Unprocessable Entity (semantic error)
  429: Too Many Requests (rate limited)

5xx Server Errors:
  500: Internal Server Error
  502: Bad Gateway
  503: Service Unavailable
  504: Gateway Timeout
```

### Application Error Codes

```yaml
Error Codes:
  VALIDATION_ERROR:
    description: Invalid request data
    http_status: 400
  
  AUTHENTICATION_FAILED:
    description: Invalid credentials
    http_status: 401
  
  AUTHORIZATION_DENIED:
    description: Insufficient permissions
    http_status: 403
  
  RESOURCE_NOT_FOUND:
    description: Requested resource not found
    http_status: 404
  
  DUPLICATE_RESOURCE:
    description: Resource already exists
    http_status: 409
  
  RATE_LIMIT_EXCEEDED:
    description: Too many requests
    http_status: 429
  
  SERVICE_UNAVAILABLE:
    description: Service temporarily unavailable
    http_status: 503
  
  TIMEOUT:
    description: Request timeout
    http_status: 504
```

---

## 🚦 Rate Limiting

### Rate Limit Headers

```yaml
Response Headers:
  X-RateLimit-Limit: 1000
  X-RateLimit-Remaining: 975
  X-RateLimit-Reset: 1698339600

Rate Limits:
  Free Tier:
    - 100 requests/minute
    - 1,000 requests/hour
    - 10,000 requests/day
  
  Professional:
    - 1,000 requests/minute
    - 50,000 requests/hour
    - 500,000 requests/day
  
  Enterprise:
    - Custom limits (contact sales)
```

### Rate Limit Error Response

```json
{
  "success": false,
  "status": 429,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "You have exceeded the rate limit. Please retry after 60 seconds."
  },
  "meta": {
    "retry_after": 60,
    "limit_resets_at": "2024-10-26T10:31:00Z"
  }
}
```

---

## 📝 Versioning & Deprecation

### API Versioning

```yaml
Current Version: v1
Base URL: https://api.example.com/v1

Versioning Strategy:
  - Major version in URL path
  - Breaking changes require new major version
  - Backward compatibility maintained for 12 months
  - Deprecation period: 6 months with warnings

Version Lifecycle:
  - v1: Current (full support)
  - v0: Deprecated (sunset date: 2024-12-31)
```

### Deprecation Headers

```yaml
Response Headers (when endpoint deprecated):
  Deprecation: true
  Sunset: 2024-12-31T00:00:00Z
  Link: <https://api.example.com/v2/...>; rel="successor-version"

Message: "This endpoint is deprecated. Please migrate to /v2 API."
```

---

## 🔄 Async Operations

### Long-Running Operations

For operations that take >5 seconds:

```yaml
POST /features/:feature_id/build-and-deploy
Response (202):
  {
    "success": true,
    "status": 202,
    "data": {
      "operation_id": "op-uuid-123",
      "status": "pending",
      "resource_type": "deployment",
      "resource_id": "deploy-uuid-1",
      "progress_url": "/operations/op-uuid-123",
      "poll_interval_seconds": 5
    }
  }

GET /operations/:operation_id
Response (200):
  {
    "success": true,
    "status": 200,
    "data": {
      "operation_id": "op-uuid-123",
      "status": "in_progress",
      "progress_percent": 75,
      "eta_seconds": 30,
      "current_step": "Running security scans...",
      "resource_url": "/deployments/deploy-uuid-1"
    }
  }

GET /operations/:operation_id (completed)
Response (200):
  {
    "success": true,
    "status": 200,
    "data": {
      "operation_id": "op-uuid-123",
      "status": "completed",
      "progress_percent": 100,
      "completed_at": "2024-10-26T10:45:00Z",
      "result_url": "/deployments/deploy-uuid-1"
    }
  }
```

---

## 🔗 Webhook Events

### Supported Events

```yaml
Events:
  feature.created:
    - Triggered when feature created
    - Payload: Feature object
  
  feature.status_changed:
    - Triggered when feature status changes
    - Payload: Feature object with previous/current status
  
  test.completed:
    - Triggered when test run completes
    - Payload: TestResult object
  
  build.completed:
    - Triggered when build completes
    - Payload: Build object with status
  
  deployment.started:
    - Triggered when deployment begins
    - Payload: Deployment object
  
  deployment.completed:
    - Triggered when deployment completes
    - Payload: Deployment object with status
  
  vulnerability.detected:
    - Triggered when vulnerability found
    - Payload: Vulnerability object
```

### Webhook Request Format

```json
{
  "event": "deployment.completed",
  "timestamp": "2024-10-26T10:30:00Z",
  "event_id": "evt-uuid-123",
  "retry_count": 0,
  "data": {
    "deployment": {
      "id": "deploy-uuid-1",
      "status": "success",
      "environment": "production"
    }
  }
}
```

### Webhook Signature Verification

```yaml
Header: X-Signature-256
Format: sha256=<hex-encoded-signature>

Verification:
  1. Extract signature from header
  2. Create HMAC-SHA256(webhook_secret, request_body)
  3. Compare computed signature with header signature
  4. Reject if signatures don't match
```

---

## 📚 Client SDKs

### SDK Support

```yaml
Official SDKs:
  - Python (https://github.com/ai-agents/python-sdk)
  - JavaScript/TypeScript (https://github.com/ai-agents/js-sdk)
  - Go (https://github.com/ai-agents/go-sdk)
  - Java (https://github.com/ai-agents/java-sdk)

Installation:
  pip install ai-agents-sdk
  npm install @ai-agents/sdk
  go get github.com/ai-agents/sdk
```

### Python SDK Example

```python
from ai_agents import Client

client = Client(
    api_key="sk-...",
    base_url="https://api.example.com/v1"
)

# Get projects
projects = client.projects.list(org_id="org-uuid-1")

# Create requirement
requirement = client.requirements.create(
    project_id="proj-uuid-1",
    title="New Feature",
    description="...",
    acceptance_criteria=[...]
)

# Create build
build = client.builds.create(
    feature_id="feat-uuid-1",
    version_tag="1.2.0",
    git_commit_hash="abc123"
)

# Deploy
deployment = client.deployments.create(
    build_id="build-uuid-1",
    environment="production"
)
```

---

## 📊 API Documentation Tools

### OpenAPI Specification

```yaml
openapi: 3.0.0
info:
  title: AI Agent System API
  version: 1.0.0
  description: Complete API for AI Agent System
  contact:
    name: API Support
    email: api-support@example.com

servers:
  - url: https://api.example.com/v1
    description: Production server

tags:
  - name: Organizations
    description: Organization management
  - name: Projects
    description: Project management
  - name: Requirements
    description: Requirement management
  - name: Deployments
    description: Deployment operations

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
```

### Interactive API Documentation

- **Swagger UI:** https://api.example.com/docs
- **ReDoc:** https://api.example.com/redoc
- **Postman Collection:** https://example.com/postman-collection.json

---

## 📚 Related Documents

- Data Modeling (data_modeling.md)
- Authentication & Security Guide
- Rate Limiting & Quotas
- SDK Documentation
- Integration Examples

---

## 📝 Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Oct 26, 2024 | API Team | Initial version |
| 1.1 | [TBD] | [Author] | v2 planning |

---

**END OF API CONTRACTS DOCUMENT**
