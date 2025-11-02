# Data Modeling Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Last Updated:** October 26, 2024
**Document Type:** Data Modeling Specification

---

## 📖 Introduction

This document defines the complete data model for the AI Agent System. It includes database schemas, entity-relationship diagrams, data types, constraints, indexing strategies, and data flow patterns. The model supports scalability to 10M+ concurrent users and petabyte-scale data volumes.

---

## 🎯 Data Modeling Principles

1. **Normalization** - Third Normal Form (3NF) for consistency
2. **Scalability** - Horizontal scaling through sharding strategies
3. **Performance** - Strategic denormalization where appropriate
4. **Security** - Encryption of sensitive data
5. **Compliance** - GDPR-compliant data retention
6. **Redundancy** - High availability through replication
7. **Auditability** - Complete audit trail for all changes

---

## 🏗️ System Data Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Data Architecture Overview                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐                                  │
│  │  Primary Data   │                                  │
│  │   (PostgreSQL)  │                                  │
│  └─────────┬────────┘                                  │
│            │                                            │
│  ┌─────────▼────────────────────────────────────────┐  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  Business Context (Contexts)             │   │  │
│  │  │  • Organizations                         │   │  │
│  │  │  • Projects                              │   │  │
│  │  │  • Teams                                 │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  │                                                  │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  Development Data                        │   │  │
│  │  │  • Requirements                          │   │  │
│  │  │  • Features                              │   │  │
│  │  │  • Code Repositories                     │   │  │
│  │  │  • Build Artifacts                       │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  │                                                  │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  Testing & Quality Data                  │   │  │
│  │  │  • Test Cases                            │   │  │
│  │  │  • Test Results                          │   │  │
│  │  │  • Test Coverage                         │   │  │
│  │  │  • Defects & Bugs                        │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  │                                                  │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  Deployment & Operations Data            │   │  │
│  │  │  • Deployments                           │   │  │
│  │  │  • Environments                          │   │  │
│  │  │  • Configuration                         │   │  │
│  │  │  • Monitoring Metrics                    │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  │                                                  │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  Security & Compliance Data              │   │  │
│  │  │  • Users & Access                        │   │  │
│  │  │  • Audit Logs                            │   │  │
│  │  │  • Security Events                       │   │  │
│  │  │  • Compliance Records                    │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  │                                                  │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  Caching Layer (Redis)                   │   │  │
│  │  │  • Session Cache                         │   │  │
│  │  │  • Query Cache                           │   │  │
│  │  │  • Configuration Cache                   │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  │                                                  │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  Time-Series Data (InfluxDB/Prometheus)  │   │  │
│  │  │  • Metrics                               │   │  │
│  │  │  • Performance Data                      │   │  │
│  │  │  • System Health                         │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  │                                                  │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  Document Store (MongoDB/Elasticsearch)  │   │  │
│  │  │  • Logs                                  │   │  │
│  │  │  • Events                                │   │  │
│  │  │  • Search Indexes                        │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  │                                                  │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  Object Storage (S3)                     │   │  │
│  │  │  • Artifacts & Builds                    │   │  │
│  │  │  • Backups                               │   │  │
│  │  │  • Media & Documents                     │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  │                                                  │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │  Message Queue (RabbitMQ/Kafka)          │   │  │
│  │  │  • Event Streaming                       │   │  │
│  │  │  • Job Queuing                           │   │  │
│  │  │  • Notifications                         │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Replication & Backup Strategy                  │  │
│  │  • Multi-region replication                     │  │
│  │  • Hourly backups                               │  │
│  │  • Point-in-time recovery                       │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Entity Relationship Diagram (ERD)

### Core Domain Entities

```
┌─────────────────────────────────────────────────────────────┐
│                    Core ERD (Simplified)                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐      ┌──────────────────┐           │
│  │  Organization    │      │  User            │           │
│  ├──────────────────┤      ├──────────────────┤           │
│  │ id (PK)          │◄─────│ id (PK)          │           │
│  │ name             │  1:M │ email            │           │
│  │ type             │      │ organization_id  │           │
│  │ created_at       │      │ role             │           │
│  └──────────────────┘      └──────────────────┘           │
│         │                          │                       │
│         │                          │                       │
│         ▼                          ▼                       │
│  ┌──────────────────┐      ┌──────────────────┐           │
│  │  Project         │      │  AccessControl   │           │
│  ├──────────────────┤      ├──────────────────┤           │
│  │ id (PK)          │      │ id (PK)          │           │
│  │ name             │◄─────│ user_id (FK)     │           │
│  │ org_id (FK)      │ 1:M  │ resource_type    │           │
│  │ status           │      │ resource_id      │           │
│  │ created_at       │      │ permission       │           │
│  └──────────────────┘      │ created_at       │           │
│         │                  └──────────────────┘           │
│         │                                                 │
│         ▼                                                 │
│  ┌──────────────────────────────────────────┐            │
│  │  Requirement                             │            │
│  ├──────────────────────────────────────────┤            │
│  │ id (PK)                                  │            │
│  │ project_id (FK)                          │            │
│  │ title                                    │            │
│  │ description                              │            │
│  │ priority                                 │            │
│  │ status                                   │            │
│  │ acceptance_criteria (JSON)               │            │
│  │ created_by                               │            │
│  │ created_at                               │            │
│  └──────────────────────────────────────────┘            │
│         │                                                 │
│         ▼                                                 │
│  ┌──────────────────────────────────────────┐            │
│  │  Feature                                 │            │
│  ├──────────────────────────────────────────┤            │
│  │ id (PK)                                  │            │
│  │ requirement_id (FK)                      │            │
│  │ name                                     │            │
│  │ description                              │            │
│  │ implementation_status                    │            │
│  │ developer_id (FK)                        │            │
│  │ branch_name                              │            │
│  │ created_at                               │            │
│  └──────────────────────────────────────────┘            │
│         │                                                 │
│    ┌────┴─────────────────────┬─────────────┐            │
│    │                          │             │            │
│    ▼                          ▼             ▼            │
│ ┌──────────┐        ┌──────────────┐  ┌──────────┐      │
│ │ TestCase │        │  TestResult  │  │  Build   │      │
│ ├──────────┤        ├──────────────┤  ├──────────┤      │
│ │ id (PK)  │◄───────│ id (PK)      │  │ id (PK)  │      │
│ │ feature_ │  1:M   │ test_case_id │  │ feature_ │      │
│ │ id (FK)  │        │ status       │  │ id (FK)  │      │
│ │ name     │        │ duration     │  │ commit   │      │
│ │ type     │        │ timestamp    │  │ status   │      │
│ └──────────┘        └──────────────┘  └──────────┘      │
│                                               │           │
│                                               ▼           │
│                                         ┌──────────────┐  │
│                                         │ Deployment   │  │
│                                         ├──────────────┤  │
│                                         │ id (PK)      │  │
│                                         │ build_id     │  │
│                                         │ environment  │  │
│                                         │ status       │  │
│                                         │ deployed_at  │  │
│                                         └──────────────┘  │
│                                                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Detailed Schema Definitions

### 1. Organization & User Management

#### Table: organizations

```sql
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL UNIQUE,
    slug VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    type ENUM('enterprise', 'startup', 'nonprofit') NOT NULL,
    plan ENUM('free', 'professional', 'enterprise') DEFAULT 'free',
    logo_url VARCHAR(512),
    website_url VARCHAR(512),
    max_users INTEGER DEFAULT 10,
    max_projects INTEGER DEFAULT 5,
    max_storage_gb INTEGER DEFAULT 100,
    billing_email VARCHAR(255),
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    settings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT organization_name_min_length CHECK (LENGTH(name) >= 2),
    CONSTRAINT organization_slug_format CHECK (slug ~ '^[a-z0-9-]+$')
);

CREATE INDEX idx_organizations_slug ON organizations(slug);
CREATE INDEX idx_organizations_status ON organizations(status);
CREATE INDEX idx_organizations_created_at ON organizations(created_at DESC);
```

#### Table: users

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    email_verified BOOLEAN DEFAULT false,
    email_verified_at TIMESTAMP WITH TIME ZONE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    avatar_url VARCHAR(512),
    phone_number VARCHAR(20),
    preferred_language VARCHAR(10) DEFAULT 'en',
    timezone VARCHAR(50) DEFAULT 'UTC',
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    role ENUM('owner', 'admin', 'developer', 'viewer') DEFAULT 'developer',
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    password_hash VARCHAR(255) NOT NULL,
    last_login_at TIMESTAMP WITH TIME ZONE,
    login_count INTEGER DEFAULT 0,
    mfa_enabled BOOLEAN DEFAULT false,
    mfa_secret VARCHAR(255),
    password_changed_at TIMESTAMP WITH TIME ZONE,
    password_expires_at TIMESTAMP WITH TIME ZONE,
    settings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT user_email_format CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'),
    CONSTRAINT user_phone_format CHECK (phone_number ~ '^\+?[0-9]{7,15}$' OR phone_number IS NULL)
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_organization_id ON users(organization_id);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_created_at ON users(created_at DESC);
```

#### Table: access_control

```sql
CREATE TABLE access_control (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    resource_type VARCHAR(50) NOT NULL, -- 'project', 'team', 'repository'
    resource_id UUID NOT NULL,
    permission ENUM('read', 'write', 'admin', 'owner') NOT NULL,
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    granted_by UUID REFERENCES users(id),
    expires_at TIMESTAMP WITH TIME ZONE,
    reason TEXT,
    
    CONSTRAINT access_unique UNIQUE(user_id, resource_type, resource_id)
);

CREATE INDEX idx_access_control_user_id ON access_control(user_id);
CREATE INDEX idx_access_control_resource ON access_control(resource_type, resource_id);
CREATE INDEX idx_access_control_permission ON access_control(permission);
```

---

### 2. Project & Development

#### Table: projects

```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT,
    repository_url VARCHAR(512),
    repository_type ENUM('git', 'svn') DEFAULT 'git',
    status ENUM('active', 'archived', 'deleted') DEFAULT 'active',
    visibility ENUM('private', 'internal', 'public') DEFAULT 'private',
    template_type VARCHAR(50), -- 'microservice', 'monolith', 'mobile', etc.
    tech_stack JSONB DEFAULT '[]'::jsonb, -- Array of technologies
    team_id UUID,
    owner_id UUID NOT NULL REFERENCES users(id),
    budget_allocated_cents INTEGER,
    estimated_hours INTEGER,
    actual_hours INTEGER,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT unique_project_slug UNIQUE(organization_id, slug),
    CONSTRAINT project_name_length CHECK (LENGTH(name) >= 2)
);

CREATE INDEX idx_projects_organization_id ON projects(organization_id);
CREATE INDEX idx_projects_owner_id ON projects(owner_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_created_at ON projects(created_at DESC);
```

#### Table: requirements

```sql
CREATE TABLE requirements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    user_stories JSONB DEFAULT '[]'::jsonb, -- Array of user stories
    acceptance_criteria JSONB NOT NULL DEFAULT '[]'::jsonb,
    priority ENUM('critical', 'high', 'medium', 'low') DEFAULT 'medium',
    status ENUM('draft', 'approved', 'in_progress', 'completed', 'rejected') DEFAULT 'draft',
    estimated_effort_points INTEGER,
    actual_effort_points INTEGER,
    priority_order INTEGER,
    created_by UUID NOT NULL REFERENCES users(id),
    assigned_to UUID REFERENCES users(id),
    start_date DATE,
    target_date DATE,
    completed_date DATE,
    dependencies JSONB DEFAULT '[]'::jsonb, -- Array of requirement IDs
    tags JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT req_title_length CHECK (LENGTH(title) >= 3)
);

CREATE INDEX idx_requirements_project_id ON requirements(project_id);
CREATE INDEX idx_requirements_status ON requirements(status);
CREATE INDEX idx_requirements_priority ON requirements(priority);
CREATE INDEX idx_requirements_assigned_to ON requirements(assigned_to);
CREATE INDEX idx_requirements_target_date ON requirements(target_date);
```

#### Table: features

```sql
CREATE TABLE features (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    requirement_id UUID NOT NULL REFERENCES requirements(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    implementation_status ENUM('not_started', 'in_progress', 'completed', 'blocked') DEFAULT 'not_started',
    implementation_notes JSONB DEFAULT '[]'::jsonb,
    developer_id UUID REFERENCES users(id),
    branch_name VARCHAR(255),
    pull_request_url VARCHAR(512),
    code_review_status ENUM('pending', 'approved', 'rejected', 'changes_requested') DEFAULT 'pending',
    estimated_hours INTEGER,
    actual_hours INTEGER,
    complexity_points INTEGER, -- 1-13 story points
    start_date TIMESTAMP WITH TIME ZONE,
    completed_date TIMESTAMP WITH TIME ZONE,
    blocked_reason TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT feature_name_length CHECK (LENGTH(name) >= 2),
    CONSTRAINT feature_complexity_range CHECK (complexity_points BETWEEN 1 AND 13)
);

CREATE INDEX idx_features_requirement_id ON features(requirement_id);
CREATE INDEX idx_features_project_id ON features(project_id);
CREATE INDEX idx_features_developer_id ON features(developer_id);
CREATE INDEX idx_features_status ON features(implementation_status);
CREATE INDEX idx_features_created_at ON features(created_at DESC);
```

---

### 3. Testing & Quality

#### Table: test_cases

```sql
CREATE TABLE test_cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    feature_id UUID NOT NULL REFERENCES features(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    test_type ENUM('unit', 'integration', 'e2e', 'performance', 'security', 'accessibility') NOT NULL,
    priority ENUM('critical', 'high', 'medium', 'low') DEFAULT 'medium',
    status ENUM('active', 'deprecated', 'disabled') DEFAULT 'active',
    preconditions JSONB DEFAULT '[]'::jsonb,
    steps JSONB NOT NULL DEFAULT '[]'::jsonb, -- Array of test steps
    expected_result TEXT,
    test_data JSONB DEFAULT '{}'::jsonb,
    automated BOOLEAN DEFAULT false,
    automation_tool VARCHAR(100), -- 'pytest', 'jest', 'cypress', etc.
    automation_script_path VARCHAR(512),
    coverage_areas JSONB DEFAULT '[]'::jsonb, -- Code coverage areas
    created_by UUID NOT NULL REFERENCES users(id),
    last_run_at TIMESTAMP WITH TIME ZONE,
    last_run_status ENUM('passed', 'failed', 'skipped'),
    run_count INTEGER DEFAULT 0,
    pass_count INTEGER DEFAULT 0,
    fail_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT test_name_length CHECK (LENGTH(name) >= 3)
);

CREATE INDEX idx_test_cases_feature_id ON test_cases(feature_id);
CREATE INDEX idx_test_cases_project_id ON test_cases(project_id);
CREATE INDEX idx_test_cases_type ON test_cases(test_type);
CREATE INDEX idx_test_cases_status ON test_cases(status);
```

#### Table: test_results

```sql
CREATE TABLE test_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_case_id UUID NOT NULL REFERENCES test_cases(id) ON DELETE CASCADE,
    feature_id UUID NOT NULL REFERENCES features(id) ON DELETE CASCADE,
    build_id UUID REFERENCES builds(id),
    status ENUM('passed', 'failed', 'skipped', 'error') NOT NULL,
    duration_ms INTEGER,
    error_message TEXT,
    error_stacktrace TEXT,
    assertions_run INTEGER,
    assertions_passed INTEGER,
    assertions_failed INTEGER,
    code_coverage_percent DECIMAL(5, 2),
    memory_used_mb INTEGER,
    cpu_percent DECIMAL(5, 2),
    execution_environment VARCHAR(100), -- 'docker', 'kubernetes', 'local'
    logs JSONB DEFAULT '[]'::jsonb,
    artifacts JSONB DEFAULT '[]'::jsonb, -- Screenshots, videos, etc.
    executed_by UUID REFERENCES users(id),
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT test_result_assertions CHECK (assertions_run >= 0)
);

CREATE INDEX idx_test_results_test_case_id ON test_results(test_case_id);
CREATE INDEX idx_test_results_feature_id ON test_results(feature_id);
CREATE INDEX idx_test_results_status ON test_results(status);
CREATE INDEX idx_test_results_executed_at ON test_results(executed_at DESC);
CREATE INDEX idx_test_results_build_id ON test_results(build_id);
```

#### Table: defects

```sql
CREATE TABLE defects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    feature_id UUID REFERENCES features(id) ON DELETE SET NULL,
    test_result_id UUID REFERENCES test_results(id) ON DELETE SET NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    severity ENUM('critical', 'high', 'medium', 'low') NOT NULL,
    priority ENUM('critical', 'high', 'medium', 'low') NOT NULL,
    status ENUM('open', 'assigned', 'in_progress', 'resolved', 'verified', 'closed', 'wont_fix') DEFAULT 'open',
    type ENUM('bug', 'enhancement', 'documentation', 'task') DEFAULT 'bug',
    assigned_to UUID REFERENCES users(id),
    reported_by UUID NOT NULL REFERENCES users(id),
    reproduction_steps TEXT,
    environment VARCHAR(100), -- 'dev', 'staging', 'production'
    affected_version VARCHAR(50),
    fixed_version VARCHAR(50),
    root_cause TEXT,
    fix_description TEXT,
    estimated_fix_hours INTEGER,
    actual_fix_hours INTEGER,
    due_date DATE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    verified_at TIMESTAMP WITH TIME ZONE,
    verified_by UUID REFERENCES users(id),
    labels JSONB DEFAULT '[]'::jsonb,
    attachments JSONB DEFAULT '[]'::jsonb, -- Screenshots, error logs, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT defect_title_length CHECK (LENGTH(title) >= 5)
);

CREATE INDEX idx_defects_project_id ON defects(project_id);
CREATE INDEX idx_defects_status ON defects(status);
CREATE INDEX idx_defects_severity ON defects(severity);
CREATE INDEX idx_defects_assigned_to ON defects(assigned_to);
CREATE INDEX idx_defects_created_at ON defects(created_at DESC);
```

---

### 4. Build & Deployment

#### Table: builds

```sql
CREATE TABLE builds (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    feature_id UUID NOT NULL REFERENCES features(id) ON DELETE CASCADE,
    build_number INTEGER NOT NULL,
    version_tag VARCHAR(50) NOT NULL,
    git_commit_hash VARCHAR(40) NOT NULL,
    git_branch VARCHAR(255) NOT NULL,
    status ENUM('pending', 'building', 'success', 'failed', 'cancelled') DEFAULT 'pending',
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_seconds INTEGER,
    triggered_by UUID REFERENCES users(id),
    build_output TEXT,
    build_errors TEXT,
    artifact_path VARCHAR(512),
    artifact_size_bytes INTEGER,
    docker_image_url VARCHAR(512),
    docker_image_size_bytes INTEGER,
    tests_run INTEGER DEFAULT 0,
    tests_passed INTEGER DEFAULT 0,
    tests_failed INTEGER DEFAULT 0,
    code_coverage_percent DECIMAL(5, 2),
    security_scan_status ENUM('pending', 'passed', 'failed', 'warnings') DEFAULT 'pending',
    vulnerabilities_critical INTEGER DEFAULT 0,
    vulnerabilities_high INTEGER DEFAULT 0,
    vulnerabilities_medium INTEGER DEFAULT 0,
    vulnerabilities_low INTEGER DEFAULT 0,
    performance_metrics JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT build_unique UNIQUE(project_id, build_number),
    CONSTRAINT build_number_positive CHECK (build_number > 0)
);

CREATE INDEX idx_builds_project_id ON builds(project_id);
CREATE INDEX idx_builds_status ON builds(status);
CREATE INDEX idx_builds_git_commit ON builds(git_commit_hash);
CREATE INDEX idx_builds_created_at ON builds(created_at DESC);
CREATE INDEX idx_builds_version ON builds(version_tag);
```

#### Table: deployments

```sql
CREATE TABLE deployments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    build_id UUID NOT NULL REFERENCES builds(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    environment VARCHAR(50) NOT NULL, -- 'dev', 'staging', 'production'
    status ENUM('pending', 'deploying', 'success', 'failed', 'rolled_back') DEFAULT 'pending',
    deployment_strategy ENUM('blue_green', 'canary', 'rolling', 'ramp') DEFAULT 'blue_green',
    canary_percentage INTEGER DEFAULT 0, -- For canary deployments
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_seconds INTEGER,
    deployed_by UUID REFERENCES users(id),
    approved_by UUID REFERENCES users(id),
    approval_notes TEXT,
    deployment_log TEXT,
    deployment_errors TEXT,
    rollback_reason TEXT,
    rolled_back_at TIMESTAMP WITH TIME ZONE,
    rolled_back_to_build_id UUID REFERENCES builds(id),
    pre_deployment_checks JSONB DEFAULT '[]'::jsonb,
    post_deployment_checks JSONB DEFAULT '[]'::jsonb,
    health_check_status ENUM('healthy', 'unhealthy', 'degraded') DEFAULT 'healthy',
    endpoints_tested JSONB DEFAULT '[]'::jsonb,
    performance_metrics JSONB DEFAULT '{}'::jsonb,
    error_rate_percent DECIMAL(5, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT deployment_canary_percent CHECK (canary_percentage BETWEEN 0 AND 100)
);

CREATE INDEX idx_deployments_build_id ON deployments(build_id);
CREATE INDEX idx_deployments_project_id ON deployments(project_id);
CREATE INDEX idx_deployments_environment ON deployments(environment);
CREATE INDEX idx_deployments_status ON deployments(status);
CREATE INDEX idx_deployments_created_at ON deployments(created_at DESC);
```

---

### 5. Monitoring & Security

#### Table: audit_logs

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL, -- 'create', 'update', 'delete', etc.
    resource_type VARCHAR(50) NOT NULL, -- 'project', 'feature', 'deployment', etc.
    resource_id UUID,
    changes JSONB DEFAULT '{}'::jsonb, -- Before/after values
    ip_address INET,
    user_agent VARCHAR(512),
    status ENUM('success', 'failure', 'pending') DEFAULT 'success',
    error_message TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_organization_id ON audit_logs(organization_id);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at DESC);
```

#### Table: security_events

```sql
CREATE TABLE security_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    event_type VARCHAR(100) NOT NULL, -- 'failed_login', 'suspicious_activity', 'vulnerability_detected', etc.
    severity ENUM('critical', 'high', 'medium', 'low', 'info') NOT NULL,
    description TEXT NOT NULL,
    ip_address INET,
    user_agent VARCHAR(512),
    resource_type VARCHAR(50),
    resource_id UUID,
    resolved BOOLEAN DEFAULT false,
    resolved_at TIMESTAMP WITH TIME ZONE,
    resolved_by UUID REFERENCES users(id),
    resolution_notes TEXT,
    investigation_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_security_events_organization_id ON security_events(organization_id);
CREATE INDEX idx_security_events_severity ON security_events(severity);
CREATE INDEX idx_security_events_resolved ON security_events(resolved);
CREATE INDEX idx_security_events_created_at ON security_events(created_at DESC);
```

#### Table: vulnerabilities

```sql
CREATE TABLE vulnerabilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    cve_id VARCHAR(50),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    severity ENUM('critical', 'high', 'medium', 'low') NOT NULL,
    cvss_score DECIMAL(3, 1),
    affected_version VARCHAR(100),
    fixed_version VARCHAR(100),
    affected_components JSONB DEFAULT '[]'::jsonb, -- Dependencies, etc.
    status ENUM('open', 'acknowledged', 'remediated', 'false_positive', 'accepted_risk') DEFAULT 'open',
    discovered_at TIMESTAMP WITH TIME ZONE,
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    remediated_at TIMESTAMP WITH TIME ZONE,
    assigned_to UUID REFERENCES users(id),
    remediation_notes TEXT,
    remediation_url VARCHAR(512),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_vulnerabilities_project_id ON vulnerabilities(project_id);
CREATE INDEX idx_vulnerabilities_severity ON vulnerabilities(severity);
CREATE INDEX idx_vulnerabilities_status ON vulnerabilities(status);
CREATE INDEX idx_vulnerabilities_cve_id ON vulnerabilities(cve_id);
```

---

## 📊 Data Volume & Growth Projections

### Expected Data Volumes (Year 1)

| Entity | Records | Storage |
|--------|---------|---------|
| Organizations | 1,000 | 5 MB |
| Users | 50,000 | 50 MB |
| Projects | 10,000 | 20 MB |
| Requirements | 100,000 | 200 MB |
| Features | 500,000 | 1 GB |
| Test Cases | 1,000,000 | 2 GB |
| Test Results | 100,000,000 | 50 GB |
| Deployments | 1,000,000 | 500 MB |
| Audit Logs | 50,000,000 | 100 GB |
| **Total Primary DB** | | **155 GB** |

### Scaling Strategy

```yaml
Year 1: Single-region, single database
Year 2: Multi-region replicas for read scaling
Year 3: Database sharding by organization_id
Year 4: Partitioning by time for audit logs
Year 5: Archival strategy for old data
```

---

## 🔄 Data Relationships & Constraints

### Cardinality

```
Organization 1 ──────── * User
Organization 1 ──────── * Project
Project 1 ──────── * Requirement
Requirement 1 ──────── * Feature
Feature 1 ──────── * TestCase
Feature 1 ──────── * Build
Build 1 ──────── * Deployment
User 1 ──────── * AuditLog
Organization 1 ──────── * SecurityEvent
Project 1 ──────── * Vulnerability
```

### Referential Integrity

All foreign keys implement:
- **ON DELETE CASCADE** - For dependent entities
- **ON DELETE RESTRICT** - For critical references
- **ON UPDATE CASCADE** - For all updates

---

## 💾 Backup & Recovery Strategy

### Backup Schedule

```yaml
Full Backup:
  Frequency: Daily (01:00 UTC)
  Duration: 2-4 hours
  Retention: 30 days
  Location: Multi-region S3

Incremental Backup:
  Frequency: Hourly
  Retention: 7 days
  Location: Primary region S3

Transaction Logs:
  Retention: 14 days
  Point-in-time recovery: Up to 14 days back
```

### Recovery Procedures

```yaml
RTO (Recovery Time Objective): 4 hours
RPO (Recovery Point Objective): 1 hour

Recovery Steps:
  1. Create new database instance (30 minutes)
  2. Restore from latest backup (2-3 hours)
  3. Apply transaction logs (15 minutes)
  4. Verify data integrity (15 minutes)
  5. Update connection strings (5 minutes)
  6. Run post-recovery tests (15 minutes)
```

---

## 🔐 Data Security & Encryption

### Encryption Strategy

```yaml
At Rest:
  Algorithm: AES-256
  Key Management: AWS KMS
  Encrypted Fields:
    - passwords
    - email_verified (masked)
    - phone_number
    - mfa_secret
    - sensitive_metadata

In Transit:
  Protocol: TLS 1.3
  Certificate: Wildcard SSL
  Cipher Suites: Modern high-security
```

### Data Masking

```python
# Sensitive fields masked in logs/exports
PASSWORD_FIELDS = ['password_hash', 'mfa_secret']
PII_FIELDS = ['email', 'phone_number']
FINANCIAL_FIELDS = ['budget_allocated_cents']

def mask_sensitive_data(record):
    for field in PASSWORD_FIELDS:
        if field in record:
            record[field] = '***REDACTED***'
    for field in PII_FIELDS:
        if field in record:
            record[field] = mask_pii(record[field])
    return record
```

---

## 📈 Performance Optimization

### Indexing Strategy

```yaml
B-tree Indexes:
  - Primary Keys (automatic)
  - Foreign Keys
  - Status/State fields
  - Timestamp fields (for sorting)
  - Frequently filtered fields

Composite Indexes:
  - (project_id, status) on features
  - (organization_id, created_at) on audit_logs
  - (feature_id, status, created_at) on test_results

Full-text Search:
  - Requirement descriptions
  - Feature names and descriptions
  - Defect titles and descriptions

Partial Indexes:
  - Active records only for status queries
  - Recent records (last 90 days) for performance
```

### Query Optimization

```sql
-- Example: Get recent test results with coverage
EXPLAIN ANALYZE
SELECT 
    tc.name,
    tr.status,
    tr.code_coverage_percent,
    tr.duration_ms
FROM test_results tr
JOIN test_cases tc ON tr.test_case_id = tc.id
WHERE tr.executed_at > CURRENT_TIMESTAMP - INTERVAL '7 days'
    AND tr.status = 'passed'
ORDER BY tr.executed_at DESC
LIMIT 100;

-- Use covering index for performance
CREATE INDEX idx_test_results_coverage ON test_results 
    (executed_at DESC, status) 
    INCLUDE (code_coverage_percent, duration_ms)
    WHERE executed_at > CURRENT_TIMESTAMP - INTERVAL '90 days';
```

---

## 🔄 Data Migration Strategy

### Schema Migrations

```yaml
Version Control:
  Tool: Flyway or Liquibase
  Location: /migrations
  Naming: V001__Initial_schema.sql
  
Zero-Downtime Migrations:
  1. Add new column with default value
  2. Backfill data in batches
  3. Update application code
  4. Remove old code path (after verification)
  5. Drop old column (if applicable)

Rollback Procedure:
  Keep previous schema version
  Maintain bidirectional compatibility
  Test rollback in staging first
```

---

## 📊 Data Quality Metrics

```yaml
Data Quality Goals:
  Completeness: > 98%
    - Ensure required fields populated
    - Monitor NULL values
  
  Accuracy: > 99.5%
    - Validate data types
    - Check constraints
    - Verify relationships
  
  Consistency: 100%
    - Foreign key integrity
    - Referential consistency
    - No orphaned records
  
  Timeliness: Real-time
    - Updates immediate
    - Replication lag < 1 second
    - Cache invalidation < 100ms
```

---

## 📚 Related Documents

- API Contracts (api_contracts.md)
- Database Administration Guide
- Disaster Recovery Plan
- Data Privacy Policy
- Performance Tuning Guide

---

## 📝 Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Oct 26, 2024 | Data Team | Initial version |
| 1.1 | [TBD] | [Author] | Schema refinement |
| 1.2 | [TBD] | [Author] | Performance optimization |

---

**END OF DATA MODELING DOCUMENT**
