# Quick Reference Guide

## Overview

This quick reference guide provides handy cheat sheets for the most common development tasks, commands, and patterns used in the Advanced AI Agent System.

---

## 1. Git Quick Reference

### Branch Management

```bash
# Create and switch to new branch
git checkout -b feature/PROJ-123-description
git switch -c feature/PROJ-123-description

# List branches
git branch                    # Local branches
git branch -a                 # All branches
git branch -vv                # With tracking info

# Delete branches
git branch -d branch-name     # Delete (safe)
git branch -D branch-name     # Force delete
git push origin --delete branch-name

# Switch branches
git checkout branch-name
git switch branch-name

# Rename branch
git branch -m old-name new-name
git push origin -u new-name
git push origin --delete old-name
```

### Committing

```bash
# Stage changes
git add file.js                # Specific file
git add .                      # All changes
git add -A                     # All changes (including deletions)
git add -p                     # Interactive staging

# Commit
git commit -m "[TYPE] [ID] - Message"
git commit --amend             # Modify last commit
git commit --amend --no-edit   # Add to last commit

# Undo commits
git reset HEAD~1               # Keep changes
git reset --hard HEAD~1        # Discard changes
git revert HEAD                # Create reverse commit
```

### Pulling and Pushing

```bash
# Pull latest
git pull origin develop        # Pull from remote
git pull origin main --rebase  # Rebase instead of merge

# Push changes
git push origin feature-name   # Push branch
git push -u origin feature-name # Push and set tracking
git push --force-with-lease    # Force safely

# Fetch without merge
git fetch origin
git fetch --prune              # Remove deleted remote branches
```

### Rebasing and History

```bash
# Rebase
git rebase origin/main         # Rebase on main
git rebase -i HEAD~3           # Interactive rebase last 3 commits
git rebase --abort             # Cancel rebase
git rebase --continue          # Continue after fixing conflicts

# Cherry-pick
git cherry-pick commit-hash    # Apply specific commit
git cherry-pick commit1..commit2 # Apply range

# View history
git log --oneline              # Concise history
git log --graph --all --decorate # Visual history
git log -p                     # With changes
git log --author="Name"        # By author
git log --grep="pattern"       # By message
git show commit-hash           # Show specific commit
git diff branch1..branch2      # Compare branches
```

### Stashing

```bash
# Save work temporarily
git stash                      # Stash all changes
git stash save "message"       # Stash with message
git stash list                 # List stashes
git stash pop                  # Apply and remove
git stash apply                # Apply (keep)
git stash drop                 # Delete
git stash clear                # Delete all
```

### Tags

```bash
# Create tags
git tag v1.0.0                 # Lightweight tag
git tag -a v1.0.0 -m "Version 1.0.0" # Annotated tag
git push origin v1.0.0         # Push tag
git push origin --tags         # Push all tags

# Delete tags
git tag -d v1.0.0              # Delete local
git push origin --delete v1.0.0 # Delete remote

# List tags
git tag                        # List all
git tag -l "v1.*"              # Pattern match
```

---

## 2. Code Quality Quick Reference

### Common Linting Commands

```bash
# ESLint
npm run lint                   # Run linting
npm run lint -- --fix          # Auto-fix issues
npm run lint -- file.js        # Check specific file
eslint . --ext .js,.ts         # Check TypeScript files

# Prettier
npm run format                 # Format all files
npm run format -- file.js      # Format specific file
prettier --check .             # Check if formatted

# Combined
npm run lint && npm run format
npm run lint:fix && npm run format
```

### Testing Commands

```bash
# Jest
npm test                       # Run tests
npm test -- --watch           # Watch mode
npm test -- --coverage        # With coverage
npm test -- --testNamePattern="test name" # Specific test
npm test -- file.test.js      # Specific file

# Integration tests
npm run test:integration
npm run test:e2e

# All tests
npm run test:all
```

### Building

```bash
# Production build
npm run build
npm run build:prod

# Development build
npm run build:dev

# Watch mode
npm run build:watch

# Analyze bundle
npm run build:analyze
```

---

## 3. Common Code Patterns

### Input Validation

```javascript
// Email validation
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if (!emailRegex.test(email)) throw new Error('Invalid email');

// URL validation
try {
  new URL(url);
} catch (e) {
  throw new Error('Invalid URL');
}

// Number validation
if (!Number.isInteger(id) || id <= 0) throw new Error('Invalid ID');

// Array validation
if (!Array.isArray(items) || items.length === 0) {
  throw new Error('Items must be non-empty array');
}

// Object validation
if (typeof obj !== 'object' || obj === null) {
  throw new Error('Must be an object');
}
```

### Error Handling

```javascript
// Try-catch pattern
try {
  const result = await riskyOperation();
  return result;
} catch (error) {
  if (error instanceof SpecificError) {
    logger.warn('Expected error', { error: error.message });
    return defaultValue;
  }
  logger.error('Unexpected error', { error });
  throw new ApplicationError('Operation failed', { cause: error });
}

// Promise catch
promise
  .then(result => processResult(result))
  .catch(error => handleError(error));

// Async error handling
async function handler() {
  try {
    await asyncOperation();
  } catch (error) {
    next(error); // Pass to Express error handler
  }
}
```

### Logging

```javascript
// Structured logging
logger.info('User login', {
  userId: user.id,
  timestamp: new Date(),
  ipAddress: req.ip
});

// Error logging
logger.error('Database connection failed', {
  error: error.message,
  code: error.code,
  host: process.env.DB_HOST
});

// Different levels
logger.debug('Debug info');
logger.info('Information');
logger.warn('Warning');
logger.error('Error');
logger.fatal('Fatal error');
```

### Async Operations

```javascript
// Sequential
async function sequential() {
  const result1 = await operation1();
  const result2 = await operation2(result1);
  return result2;
}

// Parallel
async function parallel() {
  const [result1, result2] = await Promise.all([
    operation1(),
    operation2()
  ]);
  return [result1, result2];
}

// Race
async function race() {
  const first = await Promise.race([
    operation1(),
    operation2()
  ]);
  return first;
}

// Error handling
async function withErrorHandling() {
  const results = await Promise.allSettled([
    operation1(),
    operation2()
  ]);
  
  results.forEach((result, i) => {
    if (result.status === 'fulfilled') {
      console.log(`Operation ${i} succeeded:`, result.value);
    } else {
      console.error(`Operation ${i} failed:`, result.reason);
    }
  });
}
```

### Database Operations

```javascript
// Query with parameters (prevent SQL injection)
const user = db.query('SELECT * FROM users WHERE id = ?', [userId]);

// Batch operations
const results = await db.transaction(async (trx) => {
  return Promise.all([
    trx('users').insert(user1),
    trx('users').insert(user2),
    trx('profiles').insert(profile)
  ]);
});

// Error handling
try {
  await db.insert(record);
} catch (error) {
  if (error.code === 'ER_DUP_ENTRY') {
    throw new ValidationError('Record already exists');
  }
  throw error;
}
```

---

## 4. API Quick Reference

### Common HTTP Methods

```
GET     - Retrieve data (safe, idempotent)
POST    - Create data (not idempotent)
PUT     - Replace entire resource (idempotent)
PATCH   - Partial update (may be idempotent)
DELETE  - Remove data (idempotent)
HEAD    - Like GET but no body
OPTIONS - Describe communication options
```

### Status Codes

```
200 - OK (success, body present)
201 - Created (resource created)
202 - Accepted (processing)
204 - No Content (success, no body)

400 - Bad Request (client error)
401 - Unauthorized (auth required)
403 - Forbidden (permission denied)
404 - Not Found
409 - Conflict (duplicate, etc.)

500 - Internal Server Error
502 - Bad Gateway
503 - Service Unavailable
```

### Request/Response

```javascript
// GET request
GET /api/v1/users/123
Authorization: Bearer token123
Accept: application/json

// POST request
POST /api/v1/users
Content-Type: application/json
Authorization: Bearer token123

{
  "name": "John Doe",
  "email": "john@example.com"
}

// Successful response
{
  "status": "success",
  "data": { ... },
  "metadata": {
    "timestamp": "2025-10-26T10:00:00Z",
    "version": "1.0"
  }
}

// Error response
{
  "status": "error",
  "error": "Invalid email format",
  "code": "VALIDATION_ERROR",
  "details": { ... }
}
```

### Common Headers

```
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/json
X-Request-ID: unique-id
Cache-Control: no-cache
ETag: "abc123"
Vary: Accept-Encoding
Access-Control-Allow-Origin: *
```

---

## 5. Security Quick Reference

### Password Requirements

```
Minimum 12 characters
At least 1 uppercase letter (A-Z)
At least 1 lowercase letter (a-z)
At least 1 number (0-9)
At least 1 special character (!@#$%^&*)
No common patterns (123456, qwerty, etc.)
Not similar to username/email
```

### Environment Variables

```bash
# Never commit these:
DATABASE_PASSWORD=secret
API_KEY=sk_live_abc123
JWT_SECRET=mysecret
AWS_SECRET_ACCESS_KEY=xxx

# Store in .env (gitignored):
# .env
DB_HOST=localhost
DB_PORT=5432
NODE_ENV=development

# Load in code:
require('dotenv').config();
const dbHost = process.env.DB_HOST;
```

### Encryption

```javascript
// Hashing (one-way)
const hash = bcrypt.hashSync(password, 10);
const matches = bcrypt.compareSync(password, hash);

// Encryption (two-way)
const encrypted = encrypt(sensitiveData, encryptionKey);
const decrypted = decrypt(encrypted, encryptionKey);

// Never log sensitive data
logger.info('User:', { id, name, email }); // ✓
logger.info('User:', { id, password }); // ✗
```

### Input Validation Checklist

```
✓ Type validation (string, number, etc.)
✓ Length validation (min/max)
✓ Format validation (email, phone, date)
✓ Required fields check
✓ No SQL injection (parameterized queries)
✓ No XSS (output encoding)
✓ No command injection
✓ Whitelist validation (not blacklist)
```

---

## 6. NPM Quick Reference

### Package Management

```bash
# Install
npm install                   # Install dependencies
npm install package-name      # Add package
npm install package-name@latest # Latest version
npm install package-name@1.0.0  # Specific version
npm install --save-dev package-name # Dev dependency

# Update
npm update                    # Update all packages
npm update package-name       # Update specific package
npm outdated                  # Check outdated packages

# Remove
npm uninstall package-name
npm prune                     # Remove unused packages

# List
npm list                      # Tree view
npm list --depth=0            # Top-level only
npm ls package-name           # Check if installed

# Security
npm audit                     # Check vulnerabilities
npm audit fix                 # Auto-fix vulnerabilities
npm audit fix --force         # Force fix
```

### Scripts

```json
{
  "scripts": {
    "start": "node server.js",
    "dev": "nodemon server.js",
    "build": "webpack",
    "test": "jest",
    "lint": "eslint .",
    "format": "prettier --write .",
    "pretest": "npm run lint",
    "posttest": "npm run coverage"
  }
}
```

### Running Scripts

```bash
npm start                     # npm run start
npm test                      # npm run test
npm run dev                   # Run dev script
npm run build -- --mode=prod  # Pass arguments
npm run lint && npm run test  # Run multiple
```

---

## 7. Docker Quick Reference

### Image Management

```bash
# Build image
docker build -t myapp:1.0 .
docker build -t myapp:latest .
docker build -f Dockerfile.prod -t myapp:prod .

# List images
docker images
docker images myapp

# Remove images
docker rmi myapp:1.0
docker rmi $(docker images -q)  # All images

# Push/Pull
docker push myrepo/myapp:1.0
docker pull myrepo/myapp:1.0
```

### Container Management

```bash
# Run container
docker run -d --name myapp myapp:1.0
docker run -p 3000:3000 myapp:1.0
docker run -e NODE_ENV=production myapp:1.0
docker run -v /path/host:/path/container myapp:1.0

# List containers
docker ps                     # Running
docker ps -a                  # All

# Stop/Start
docker stop container-id
docker start container-id
docker restart container-id
docker kill container-id      # Force stop

# Logs
docker logs container-id
docker logs -f container-id   # Follow
docker logs --tail 100 container-id

# Execute
docker exec -it container-id bash
docker exec container-id npm test
```

### Docker Compose

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - db
  
  db:
    image: postgres:13
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

```bash
# Compose commands
docker-compose up                # Start services
docker-compose up -d             # Detached mode
docker-compose down              # Stop services
docker-compose logs -f           # View logs
docker-compose ps                # Status
docker-compose exec app bash     # Execute in container
```

---

## 8. Kubernetes Quick Reference

### Pods

```bash
# Create pod
kubectl run myapp --image=myapp:1.0

# Get pods
kubectl get pods
kubectl get pods -n namespace
kubectl get pods -o wide

# Pod details
kubectl describe pod pod-name
kubectl logs pod-name
kubectl logs -f pod-name           # Follow

# Execute
kubectl exec -it pod-name -- bash
kubectl exec pod-name -- npm test

# Delete
kubectl delete pod pod-name
```

### Deployments

```bash
# Create deployment
kubectl create deployment myapp --image=myapp:1.0
kubectl apply -f deployment.yaml

# Scale
kubectl scale deployment myapp --replicas=3
kubectl autoscale deployment myapp --min=1 --max=10

# Update
kubectl set image deployment/myapp myapp=myapp:1.1
kubectl rollout status deployment/myapp

# Rollback
kubectl rollout undo deployment/myapp
kubectl rollout history deployment/myapp

# Delete
kubectl delete deployment myapp
```

### Services

```bash
# Create service
kubectl expose deployment myapp --type=LoadBalancer --port=80 --target-port=3000
kubectl apply -f service.yaml

# Get services
kubectl get services
kubectl get svc

# Delete service
kubectl delete service myapp
```

### Namespaces

```bash
# Create namespace
kubectl create namespace production

# Switch namespace
kubectl config set-context --current --namespace=production

# Get resources in namespace
kubectl get pods -n production
kubectl get pods --all-namespaces
```

---

## 9. Database Quick Reference

### PostgreSQL

```sql
-- Connect
psql -h localhost -U username -d database_name

-- List databases
\l

-- Connect to database
\c database_name

-- List tables
\dt

-- Table structure
\d table_name

-- Common queries
SELECT * FROM users LIMIT 10;
SELECT COUNT(*) FROM users;
INSERT INTO users (name, email) VALUES ('John', 'john@example.com');
UPDATE users SET name='Jane' WHERE id=1;
DELETE FROM users WHERE id=1;

-- Create table
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Drop table
DROP TABLE users;

-- Backup/Restore
pg_dump -U username database_name > backup.sql
psql -U username database_name < backup.sql
```

### MongoDB

```javascript
// Connect
const client = new MongoClient('mongodb://localhost:27017');

// Get database and collection
const db = client.db('myapp');
const users = db.collection('users');

// Create
await users.insertOne({ name: 'John', email: 'john@example.com' });

// Read
await users.findOne({ _id: ObjectId('...') });
await users.find({ status: 'active' }).toArray();

// Update
await users.updateOne({ _id: id }, { $set: { name: 'Jane' } });

// Delete
await users.deleteOne({ _id: id });

// Query operators
{ age: { $gte: 18 } }          // Greater than or equal
{ status: { $in: ['a', 'b'] } } // In array
{ $and: [...], $or: [...] }    // Logical operators
```

---

## 10. Configuration Quick Reference

### Environment Profiles

```bash
# Development
NODE_ENV=development
DEBUG=true
LOG_LEVEL=debug
DB_HOST=localhost

# Staging
NODE_ENV=staging
DEBUG=false
LOG_LEVEL=info
DB_HOST=staging-db.example.com

# Production
NODE_ENV=production
DEBUG=false
LOG_LEVEL=warn
DB_HOST=prod-db.example.com
```

### Feature Flags

```javascript
// Check feature flag
if (featureFlags.isEnabled('new-auth-system')) {
  // Use new auth
} else {
  // Use old auth
}

// Enable for percentage of users
if (featureFlags.enabledFor(user, 'new-ui', 50)) {
  // Show to 50% of users
}

// Enable for specific users
if (featureFlags.enabledFor(user, 'beta-feature', ['admin@example.com'])) {
  // Show to admin
}
```

---

## 11. Debugging Quick Reference

### Console Methods

```javascript
console.log('Message');           // Standard output
console.error('Error message');   // Error output
console.warn('Warning message');  // Warning output
console.info('Info message');     // Info output
console.debug('Debug message');   // Debug output
console.table(data);              // Table format
console.group('Label');           // Group logs
console.groupEnd();
console.time('label');            // Timer start
console.timeEnd('label');         // Timer end
console.trace();                  // Stack trace
```

### Node Debugging

```bash
# Run with debugger
node --inspect server.js
node --inspect-brk server.js      # Break on start

# Debug in Chrome
chrome://inspect

# VSCode debugging (launch.json)
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/server.js"
    }
  ]
}
```

### Browser DevTools

```javascript
// Breakpoints
debugger;                         // Hard breakpoint

// Conditional breakpoints
// Set in DevTools

// Watch expressions
// Set in DevTools

// Network debugging
// Network tab in DevTools

// Memory profiling
// Memory tab in DevTools
```

---

## 12. Performance Quick Reference

### Profiling

```bash
# Node profiling
node --prof server.js
node --prof-process isolate-*.log > profile.txt

# Memory usage
node --trace-gc server.js

# CPU profiling with clinic
clinic doctor -- node server.js
clinic flame -- node server.js
```

### Optimization Tips

```javascript
// Cache expensive operations
const cache = new Map();
function getCached(key, fn) {
  if (cache.has(key)) return cache.get(key);
  const value = fn();
  cache.set(key, value);
  return value;
}

// Lazy loading
const module = require('module-name'); // Load on demand

// Batch operations
// Instead of: await db.query() in loop
// Use: await db.batchInsert(items)

// Use appropriate data structures
// Array for ordered, Set for unique, Map for key-value
```

---

## Quick Links

### Common Commands by Task

**Starting Development:**
```bash
git checkout -b feature/PROJ-123-name
npm install
npm run dev
```

**Creating a PR:**
```bash
git add .
git commit -m "[FEAT] [PROJ-123] - Description"
git push -u origin feature/PROJ-123-name
# Create PR on GitHub
```

**Code Review:**
```bash
npm run lint
npm test
npm run build
# Check security_checklist.md
```

**Merging PR:**
```bash
git checkout main
git pull origin main
git merge feature/PROJ-123-name
git push origin main
git branch -d feature/PROJ-123-name
```

**Deploying:**
```bash
npm run build:prod
docker build -t app:1.0 .
docker push registry/app:1.0
kubectl apply -f deployment.yaml
```

---

## Conclusion

This quick reference provides the most common commands and patterns for daily development work. Bookmark this page for quick access! 🚀

