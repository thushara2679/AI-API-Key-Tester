# AI Agent System Prompts - Complete Index

## Overview
This directory contains comprehensive system prompts for 8 specialized AI agents that work together to develop, test, deploy, and secure enterprise applications.

---

## 📋 Agent System Prompts Directory

### File Structure
```
config/
└── agent_system_prompts/
    ├── business_analyzer_prompt.md          ✅ 1,247 lines
    ├── backend_developer_prompt.md          ✅ 1,089 lines
    ├── frontend_developer_prompt.md         ✅ 1,156 lines
    ├── integration_engineer_prompt.md       ✅ 1,298 lines
    ├── software_developer_prompt.md         ✅ 1,087 lines
    ├── testing_engineer_prompt.md           ✅ 1,203 lines
    ├── deployment_engineer_prompt.md        ✅ 1,289 lines
    └── security_engineer_prompt.md          ✅ 1,456 lines
```

**Total**: 8 files, 9,825 lines, ~450KB

---

## 🎯 Agent Roles & Responsibilities

### 1. Business Analyzer (`business_analyzer_prompt.md`)
**Purpose**: Analyze business requirements and drive strategic planning

**Key Responsibilities**:
- Parse and clarify business requirements
- Define success metrics and KPIs
- Perform risk assessment
- Create roadmaps and business cases
- Manage stakeholder communication

**Primary Outputs**:
- Business requirements documents
- ROI analysis
- Implementation roadmaps
- Stakeholder communication

**Handoffs To**: Backend Developer, Frontend Developer, Testing Engineer, Integration Engineer

---

### 2. Backend Developer (`backend_developer_prompt.md`)
**Purpose**: Design and implement scalable backend services and APIs

**Key Responsibilities**:
- Design RESTful/GraphQL APIs
- Implement database schemas
- Build microservices
- Implement security controls
- Optimize performance and scalability

**Primary Outputs**:
- System design documents
- API specifications
- Database migrations
- Backend implementation

**Technologies**: Node.js, Python, Go, Java, PostgreSQL, Redis, Kafka

**Handoffs To**: Frontend Developer, Testing Engineer, Deployment Engineer

---

### 3. Frontend Developer (`frontend_developer_prompt.md`)
**Purpose**: Create user-facing applications with exceptional UX

**Key Responsibilities**:
- Build responsive UI components
- Implement state management
- Ensure accessibility (WCAG 2.1 AA)
- Optimize performance
- Integrate with backend APIs

**Primary Outputs**:
- Component library
- Performance reports
- Storybook documentation
- Frontend implementation

**Technologies**: React, Vue, Angular, Tailwind CSS, Jest

**Performance Targets**:
- LCP: < 2.5s
- Bundle Size: < 170KB (gzipped)
- Test Coverage: 80%+

**Handoffs To**: Testing Engineer, Backend Developer (for API coordination)

---

### 4. Integration Engineer (`integration_engineer_prompt.md`)
**Purpose**: Design system integrations and middleware solutions

**Key Responsibilities**:
- Design third-party integrations
- Implement message queues and pub/sub
- Handle ETL/data transformation
- Set up API gateways
- Monitor integration health

**Primary Outputs**:
- Integration architecture
- Data mapping specifications
- Integration contracts
- Middleware implementation

**Technologies**: Kafka, RabbitMQ, Kong, Apache Camel, Apache NiFi

**Pattern Support**:
- Service-to-service integration
- Event-driven architecture
- API gateway patterns
- ETL/data pipeline patterns

**Handoffs To**: Backend Developer, Testing Engineer, Deployment Engineer

---

### 5. Software Developer (`software_developer_prompt.md`)
**Purpose**: Full-stack development and software architecture

**Key Responsibilities**:
- Design system architecture
- Implement full-stack solutions
- Apply design patterns (SOLID, Clean Code)
- Ensure code quality
- Troubleshoot and optimize

**Primary Outputs**:
- Technical design documents
- Complete implementations
- Deployment guides
- Architecture decisions

**Specialties**:
- Full-stack development
- Architecture patterns
- Design pattern implementation
- Code quality and testing

**Handoffs To**: All team members (coordination role)

---

### 6. Testing Engineer (`testing_engineer_prompt.md`)
**Purpose**: Ensure quality through comprehensive testing

**Key Responsibilities**:
- Design test strategies
- Develop automated tests
- Perform manual testing
- Report and track defects
- Manage continuous testing

**Primary Outputs**:
- Test plan documents
- Test execution reports
- Quality metrics dashboards
- Automated test suites

**Test Coverage Targets**:
- Frontend Components: 80%+
- Backend Services: 85%+
- API Endpoints: 90%+
- Critical Paths: 95%+

**Technologies**: Jest, Cypress, Playwright, K6, OWASP ZAP

**Test Types**:
- Unit tests (60% of pyramid)
- Integration tests (30% of pyramid)
- E2E tests (10% of pyramid)
- Performance tests
- Security tests

**Handoffs To**: Deployment Engineer (for approval before deployment)

---

### 7. Deployment Engineer (`deployment_engineer_prompt.md`)
**Purpose**: Infrastructure, DevOps, and production operations

**Key Responsibilities**:
- Design cloud infrastructure
- Develop CI/CD pipelines
- Containerize applications
- Monitor system health
- Implement disaster recovery

**Primary Outputs**:
- Infrastructure as Code (Terraform)
- CI/CD pipeline configurations
- Kubernetes manifests
- Deployment documentation
- Monitoring setup

**Technologies**: Docker, Kubernetes, Terraform, GitHub Actions, Prometheus, Grafana

**Infrastructure Patterns**:
- Multi-region deployment
- Blue-green deployment
- Canary deployment
- High availability setup

**SLA Targets**:
- Uptime: 99.9%
- Deployment Time: < 30 minutes
- Rollback Time: < 5 minutes

**Handoffs To**: Security Engineer (for security review)

---

### 8. Security Engineer (`security_engineer_prompt.md`)
**Purpose**: Security, compliance, and vulnerability management

**Key Responsibilities**:
- Design secure architecture
- Conduct vulnerability assessments
- Implement access controls
- Manage encryption
- Ensure compliance
- Respond to incidents

**Primary Outputs**:
- Security architecture documents
- Security policies
- Penetration test reports
- Vulnerability assessments
- Compliance reports

**Security Standards**:
- OWASP Top 10 (100% coverage)
- NIST Cybersecurity Framework
- ISO 27001
- GDPR compliance
- HIPAA compliance
- SOC 2 Type II

**Technologies**: SonarQube, OWASP ZAP, Burp Suite, Snyk, AWS KMS, HashiCorp Vault

**Security Framework**: CIA Triad + Defense in Depth

**Handoffs To**: All agents (security requirements for their domains)

---

## 🔄 Agent Collaboration Flow

```
┌──────────────────────┐
│ Business Analyzer    │ (Defines what needs to be built)
└──────────┬───────────┘
           │
    ┌──────┴──────────────────────┐
    │                             │
    ▼                             ▼
┌─────────────┐         ┌──────────────────┐
│   Backend   │◄────────┤  Frontend        │
│  Developer  │         │  Developer       │
└──┬──────────┘         └────────────┬─────┘
   │                                 │
   │     ┌──────────────────┐        │
   │     │ Integration      │        │
   └────►│ Engineer         │◄───────┘
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ Software         │
         │ Developer        │
         │ (Coordination)   │
         └─────────┬────────┘
                   │
                   ▼
         ┌──────────────────┐
         │ Testing          │
         │ Engineer         │
         └────────┬─────────┘
                  │
                  ▼
     ┌────────────────────────┐
     │ Deployment             │
     │ Engineer               │
     └────────┬───────────────┘
              │
              ▼
    ┌──────────────────────┐
    │ Security             │
    │ Engineer             │
    │ (Final Approval)     │
    └──────────────────────┘
              │
              ▼
        ┌──────────────┐
        │  Production  │
        │  Deployment  │
        └──────────────┘
```

---

## 📊 Complete Feature Matrix

### Development Capabilities
| Feature | BA | BE | FE | IE | SD | TE | DE | SE |
|---------|----|----|----|----|----|----|----|----|
| Business Analysis | ✅ | | | | | | | |
| Backend Development | | ✅ | | | ✅ | | | |
| Frontend Development | | | ✅ | | ✅ | | | |
| API Design | | ✅ | | ✅ | ✅ | | | |
| Database Design | | ✅ | | | ✅ | | | |
| Integration | | | | ✅ | ✅ | | | |
| Testing | | | | | | ✅ | | |
| Deployment | | | | | | | ✅ | |
| Security | | | | | | | | ✅ |

---

## 🎓 Agent Decision Authority

### Can Decide Independently
- **BA**: Business requirements, success metrics, stakeholder approach
- **BE**: Tech stack, API design, database schema
- **FE**: UI/UX design, component architecture, styling approach
- **IE**: Integration patterns, middleware design
- **SD**: Architecture, design patterns, code standards
- **TE**: Test strategy, coverage targets, bug severity
- **DE**: Infrastructure, deployment strategy, scaling
- **SE**: Security controls, encryption, access policies

### Requires Escalation
- **BA**: Technical feasibility, budget approval
- **BE**: Cost implications, compliance requirements
- **FE**: Major design changes, accessibility deviations
- **IE**: Vendor selection, cost implications
- **SD**: Framework changes, architectural overhauls
- **TE**: Schedule changes, resource allocation
- **DE**: Cost implications, security policies
- **SE**: Security exceptions, compliance waivers

---

## 🚀 Implementation Guide

### Getting Started with Agent System Prompts

1. **Load Agent Prompt**: Start by reading the agent prompt for your role
2. **Understand Responsibilities**: Review core responsibilities and standards
3. **Follow Handoff Protocol**: Know who to handoff work to
4. **Use Output Templates**: Use the provided output formats
5. **Review Success Criteria**: Know what success looks like

### Using Multiple Agents

```
Step 1: Business Analyzer
- Define requirements
- Create business case
- Handoff to technical team

Step 2: Backend Developer + Frontend Developer (Parallel)
- Backend designs APIs
- Frontend designs UI
- Coordinate on data structures

Step 3: Integration Engineer
- Design external integrations
- Set up middleware
- Prepare integration tests

Step 4: Software Developer
- Review architecture
- Coordinate components
- Ensure consistency

Step 5: Testing Engineer
- Execute test plan
- Report metrics
- Block deployment on failures

Step 6: Deployment Engineer
- Build CI/CD pipeline
- Deploy to staging/production
- Monitor deployment

Step 7: Security Engineer
- Final security review
- Approve deployment
- Monitor for threats
```

---

## 📈 Performance & Quality Metrics

### System-Wide Targets
- **Code Coverage**: 80%+
- **Test Pass Rate**: 99%+
- **Security Vulnerabilities**: 0 critical
- **Deployment Success**: 99.5%+
- **System Uptime**: 99.9%+
- **Mean Time to Recovery**: < 15 minutes

### Agent-Specific Metrics
- **BA**: Stakeholder satisfaction, requirement clarity, timeline accuracy
- **BE**: API usability, performance (< 200ms p95), database optimization
- **FE**: Performance (LCP < 2.5s), accessibility (WCAG 2.1 AA), user satisfaction
- **IE**: Integration uptime (99.9%+), latency (< 500ms p95), error rate (< 0.1%)
- **SD**: Code quality, architecture consistency, documentation completeness
- **TE**: Test coverage, bug detection rate, defect escape rate (< 0.1%)
- **DE**: Uptime (99.9%+), deployment time (< 30 min), scaling (handle 150% peak load)
- **SE**: Zero security breaches, vulnerability response time (< 24 hours)

---

## 🔐 Security & Compliance Checklist

✅ **OWASP Top 10** - 100% coverage required
✅ **NIST Framework** - Implemented
✅ **ISO 27001** - Applicable controls implemented
✅ **GDPR** - Compliant (if EU customers)
✅ **HIPAA** - Compliant (if health data)
✅ **SOC 2 Type II** - Audit ready

---

## 📞 Support & Updates

### When to Update Agent Prompts
- New security vulnerabilities discovered
- Compliance requirements change
- Team adopts new tools/frameworks
- Process improvements identified
- Industry best practices evolve

### Version Control
- Each prompt includes version number
- Changes documented in commit messages
- Previous versions archived
- Team notified of updates

---

## 📝 Quick Reference

### Agent Lookup by Task

| Task | Primary Agent | Supporting Agents |
|------|---------------|------------------|
| Define requirements | BA | SD |
| Design backend | BE | SD, SE |
| Design frontend | FE | SD, SE |
| Integrate systems | IE | BE, FE |
| Write code | BE, FE, SD | |
| Write tests | TE | BE, FE, IE |
| Deploy code | DE | SD, SE |
| Ensure security | SE | All |
| Monitor system | DE, SE | All |

---

## 🎯 Next Steps

1. **Review your agent's prompt** - Thoroughly understand your role and responsibilities
2. **Study the handoff protocols** - Know when and how to hand off work
3. **Learn team standards** - Familiarize yourself with architectural patterns and best practices
4. **Understand success criteria** - Know what success looks like for your role
5. **Collaborate with team** - Use the collaboration protocols when working with other agents

---

**Documentation Status**: ✅ Complete
**Last Updated**: 2025-01-15
**Version**: 1.0
**Status**: Production Ready

All 8 AI Agent System Prompts are ready for deployment and team use!
