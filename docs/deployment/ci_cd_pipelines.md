# CI/CD Pipelines Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Last Updated:** October 26, 2024
**Document Type:** CI/CD Pipelines & Deployment Guide
**Focus:** Modern CI/CD strategies and implementations

---

## 🔄 CI/CD Pipeline Architecture

### Pipeline Stages Overview

```
Trigger → Checkout → Build → Test → Security → 
Build Image → Deploy Staging → Deploy Production → Monitor
```

### GitHub Actions Pipeline

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/

  test:
    needs: build
    runs-on: ubuntu-latest
    strategy:
      matrix:
        test-type: [unit, integration, e2e]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      
      - run: npm ci
      - run: npm run test:${{ matrix.test-type }}
      
      - uses: codecov/codecov-action@v3
        if: matrix.test-type == 'unit'

  security:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run SAST
        run: npm run security:scan
      
      - name: Check dependencies
        run: npm audit
      
      - name: OWASP dependency check
        uses: dependency-check/Dependency-Check_Action@main

  build-image:
    needs: [test, security]
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v3
      
      - uses: docker/setup-buildx-action@v2
      
      - uses: docker/login-action@v2
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - uses: docker/metadata-action@v4
        id: meta
        with:
          images: ghcr.io/ai-agent-system
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha
      
      - uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    needs: build-image
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to staging
        run: |
          ./scripts/deploy.sh staging ${{ needs.build-image.outputs.image-tag }}
      
      - name: Run smoke tests
        run: npm run test:smoke -- --env=staging

  deploy-prod:
    needs: [test, security, build-image]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to production
        run: |
          ./scripts/deploy.sh production ${{ needs.build-image.outputs.image-tag }}
      
      - name: Verify deployment
        run: npm run verify:deployment -- --env=prod
```

---

## 🚀 Deployment Strategies

### Blue-Green Deployment

```bash
#!/bin/bash
# scripts/blue-green-deploy.sh

set -e

ENVIRONMENT=$1
IMAGE=$2

# Current version (blue)
BLUE_VERSION=$(kubectl get deployment ai-agent-system-blue -o jsonpath='{.spec.template.spec.containers[0].image}')

# Deploy new version (green)
kubectl set image deployment/ai-agent-system-green ai-agent-system=${IMAGE} --record

# Wait for rollout
kubectl rollout status deployment/ai-agent-system-green --timeout=5m

# Run smoke tests
GREEN_POD=$(kubectl get pod -l app=ai-agent-system,version=green -o jsonpath='{.items[0].metadata.name}')
kubectl exec ${GREEN_POD} -- npm run test:smoke

# Switch traffic
kubectl patch service ai-agent-system -p '{"spec":{"selector":{"version":"green"}}}'

# Monitor
sleep 60
echo "Deployment successful!"
```

### Canary Deployment

```bash
#!/bin/bash
# scripts/canary-deploy.sh

ENVIRONMENT=$1
IMAGE=$2

# Deploy canary (10% traffic)
kubectl set image deployment/ai-agent-system-canary ai-agent-system=${IMAGE}

# Update traffic weights
cat <<EOF | kubectl apply -f -
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: ai-agent-system
spec:
  hosts:
  - ai-agent-system
  http:
  - match:
    - uri:
        prefix: /
    route:
    - destination:
        host: ai-agent-system-stable
      weight: 90
    - destination:
        host: ai-agent-system-canary
      weight: 10
EOF

# Monitor and gradually increase
for weight in 25 50 75 100; do
  echo "Increasing canary traffic to ${weight}%..."
  sleep 120
done

echo "Canary deployment complete!"
```

### Rolling Update

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-agent-system
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: ai-agent-system
  template:
    metadata:
      labels:
        app: ai-agent-system
    spec:
      containers:
      - name: app
        image: ghcr.io/ai-agent-system:latest
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
```

---

## 🔗 Pipeline Tools

### GitLab CI

```yaml
stages:
  - build
  - test
  - security
  - deploy

build:
  stage: build
  image: docker:latest
  script:
    - docker build -t registry.gitlab.com/ai-agent-system:$CI_COMMIT_SHA .
    - docker push registry.gitlab.com/ai-agent-system:$CI_COMMIT_SHA

test-unit:
  stage: test
  image: node:18
  script:
    - npm ci
    - npm run test:unit

security:
  stage: security
  image: node:18
  script:
    - npm audit
    - npm run security:scan

deploy-staging:
  stage: deploy
  script:
    - ./scripts/deploy.sh staging
  environment:
    name: staging
  only:
    - develop

deploy-production:
  stage: deploy
  script:
    - ./scripts/deploy.sh production
  environment:
    name: production
  when: manual
  only:
    - main
```

### Jenkins Pipeline

```groovy
pipeline {
  agent any
  
  stages {
    stage('Build') {
      steps {
        sh 'npm ci && npm run build'
      }
    }
    
    stage('Test') {
      parallel {
        stage('Unit') {
          steps {
            sh 'npm run test:unit'
          }
        }
        stage('Integration') {
          steps {
            sh 'npm run test:integration'
          }
        }
      }
    }
    
    stage('Security') {
      steps {
        sh 'npm audit && npm run security:scan'
      }
    }
    
    stage('Deploy Staging') {
      when { branch 'develop' }
      steps {
        sh './scripts/deploy.sh staging'
      }
    }
    
    stage('Deploy Production') {
      when { branch 'main' }
      input { message "Deploy to production?" }
      steps {
        sh './scripts/deploy.sh production'
      }
    }
  }
  
  post {
    always {
      junit 'test-results/**/*.xml'
    }
  }
}
```

---

## 🔐 Secrets Management

### GitHub Secrets

```bash
gh secret set DATABASE_URL --body "postgresql://localhost/db"
gh secret set API_KEY --body "secret-key"
gh secret set AWS_ACCESS_KEY_ID --body "..."
```

### HashiCorp Vault

```bash
#!/bin/bash
# Fetch secrets from Vault
vault login -method=github token=$GITHUB_TOKEN

DB_URL=$(vault kv get -field=url secret/database)
API_KEY=$(vault kv get -field=key secret/api)

export DATABASE_URL=$DB_URL
export API_KEY=$API_KEY

./scripts/deploy.sh production
```

---

## 📊 Pipeline Metrics

```typescript
interface PipelineMetrics {
  buildTime: number;
  testDuration: number;
  deploymentTime: number;
  successRate: number;
}

class PipelineMonitor {
  async collectMetrics(): Promise<PipelineMetrics> {
    return {
      buildTime: 300,
      testDuration: 600,
      deploymentTime: 120,
      successRate: 98.5
    };
  }
}
```

---

## 📚 Related Documents

- Containerization (containerization.md)
- Cloud Platforms (cloud_platforms.md)
- Monitoring (monitoring.md)
- Scaling (scaling.md)

---

**END OF CI/CD PIPELINES DOCUMENT**
