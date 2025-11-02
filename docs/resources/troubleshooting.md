# Troubleshooting Guide

## Overview

This guide provides solutions for common issues encountered during development, deployment, and operations of the Advanced AI Agent System.

---

## 1. Development Environment Issues

### 1.1 Node.js / npm Issues

**Problem: npm install fails with "Cannot find module" errors**

Solution 1: Clear cache and reinstall
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

Solution 2: Update npm
```bash
npm install -g npm@latest
npm install
```

Solution 3: Check Node version
```bash
node --version  # Should be 16+
npm --version   # Should be 7+
# If old, update:
brew upgrade node  # macOS
apt-get install nodejs npm  # Linux
```

**Problem: Port already in use (3000, 5432, etc.)**

Solution: Find and kill process using port
```bash
# macOS/Linux
lsof -i :3000          # Find process using port 3000
kill -9 <PID>          # Kill the process

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

Or use different port:
```bash
PORT=3001 npm run dev
```

**Problem: Permission denied when installing globally**

Solution: Fix npm permissions
```bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
```

### 1.2 Git Issues

**Problem: "fatal: not a git repository"**

Solution: Initialize Git or navigate to correct directory
```bash
pwd                    # Check current directory
ls -la                 # Verify .git exists
cd /path/to/project    # Navigate to project root
git status             # Verify Git works
```

**Problem: Merge conflicts**

Solution 1: View conflicts
```bash
git diff              # See all conflicts
git status            # See conflicted files
```

Solution 2: Resolve conflicts
- Open conflicted files in editor
- Find sections marked: `<<<<<<`, `======`, `>>>>>>`
- Choose correct version
- Remove conflict markers
- Stage and commit

```bash
git add resolved-file.js
git commit -m "FIX: Resolved merge conflict"
```

Solution 3: Abort if needed
```bash
git merge --abort      # Cancel merge
git rebase --abort     # Cancel rebase
```

**Problem: Detached HEAD state**

Solution: Get back to branch
```bash
git branch             # See branches
git checkout main      # Switch to main branch
```

### 1.3 Docker Issues

**Problem: Docker daemon not running**

Solution 1: Start Docker Desktop (macOS/Windows)
- Click Docker icon in Applications
- Wait for "Docker is running"

Solution 2: Start Docker daemon (Linux)
```bash
sudo systemctl start docker
sudo systemctl enable docker  # Start on boot
```

**Problem: Permission denied while running Docker**

Solution: Add user to docker group
```bash
sudo usermod -aG docker $USER
newgrp docker          # Apply group changes
docker ps              # Test
```

**Problem: Image build fails**

Solution 1: Check Dockerfile
```bash
docker build -t myapp:1.0 .
# Look for specific error line
```

Solution 2: Build with verbose output
```bash
docker build -t myapp:1.0 . --progress=plain
```

Solution 3: Check base image
```dockerfile
# Ensure base image exists and is correct
FROM node:16-alpine  # Verify this exists
```

### 1.4 Database Issues

**Problem: Cannot connect to PostgreSQL**

Solution 1: Verify connection details
```bash
# Check environment variables
echo $DB_HOST
echo $DB_PORT
echo $DB_USER

# Test connection
psql -h localhost -U postgres -d postgres
```

Solution 2: Start PostgreSQL
```bash
# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql

# Docker
docker run -p 5432:5432 postgres:13
```

Solution 3: Check credentials
```bash
# Verify password is correct
psql -h localhost -U postgres
# If prompted for password, enter it
```

**Problem: Database migrations failed**

Solution 1: Check migration status
```bash
npm run migrate:status
```

Solution 2: Rollback migration
```bash
npm run migrate:rollback
```

Solution 3: Create new migration
```bash
npm run migrate:create -- create_users_table
# Edit migration file
npm run migrate:latest
```

---

## 2. Testing Issues

### 2.1 Jest Issues

**Problem: Tests fail with "Cannot find module"**

Solution 1: Clear Jest cache
```bash
npm test -- --clearCache
npm test
```

Solution 2: Install missing dependency
```bash
npm install --save-dev jest @types/jest
```

**Problem: Timeout errors in tests**

Solution 1: Increase timeout
```javascript
test('long running test', async () => {
  // test code
}, 10000); // 10 second timeout
```

Solution 2: Mock slow operations
```javascript
jest.mock('slowModule', () => ({
  slowFunction: jest.fn().mockResolvedValue('result')
}));
```

**Problem: Tests pass locally but fail in CI**

Solution 1: Check environment variables
```bash
# In CI, set all needed env vars
echo $NODE_ENV
echo $DATABASE_URL
```

Solution 2: Check test data
```bash
# Ensure test database is clean
npm run test:setup
npm test
```

Solution 3: Serial vs parallel
```bash
npm test -- --runInBand  # Run tests serially
```

### 2.2 Cypress Issues

**Problem: Cypress can't find element**

Solution 1: Verify element exists
```bash
# Use selector console
cy.get('button').click()
# If fails, check with:
cy.get('button').should('exist')
```

Solution 2: Wait for element
```javascript
cy.get('button', { timeout: 5000 }).click()
```

Solution 3: Use more specific selector
```javascript
// Instead of generic:
cy.get('button').click()
// Use specific:
cy.get('[data-testid="submit-button"]').click()
```

**Problem: Tests fail when running headless**

Solution 1: Use headless mode for debugging
```bash
npx cypress run --headed
```

Solution 2: Check for visual issues
```javascript
// Add debugging screenshots
cy.screenshot()
```

---

## 3. Linting & Formatting Issues

### 3.1 ESLint Issues

**Problem: Linting errors block commit**

Solution 1: Fix errors automatically
```bash
npm run lint -- --fix
```

Solution 2: Review and fix manually
```bash
npm run lint              # See all errors
# Edit files to fix errors
npm run lint              # Verify fixed
```

**Problem: Rule conflicts**

Solution 1: Review .eslintrc configuration
```json
{
  "extends": ["eslint:recommended"],
  "rules": {
    "no-console": "off",  // Allow console
    "semi": ["error", "always"]
  }
}
```

Solution 2: Disable rule for specific line
```javascript
// eslint-disable-next-line no-console
console.log('debug info');
```

### 3.2 Prettier Issues

**Problem: Prettier formatting is wrong**

Solution 1: Check Prettier config
```bash
cat .prettierrc
```

Solution 2: Reformat all files
```bash
npm run format
```

Solution 3: Override for specific file
```javascript
// prettier-ignore
const x=1+2;
```

---

## 4. Build Issues

### 4.1 Build Failures

**Problem: Build fails with "Module not found"**

Solution 1: Install dependencies
```bash
npm install
```

Solution 2: Check imports
```javascript
// Verify import paths are correct
import { Component } from './components/Component';  // Correct
import { Component } from './component';              // Wrong path
```

Solution 3: Clear build cache
```bash
rm -rf dist/ build/
npm run build
```

**Problem: Build is too slow**

Solution 1: Analyze bundle
```bash
npm run build:analyze
```

Solution 2: Remove unused dependencies
```bash
npm audit
npm uninstall unused-package
```

Solution 3: Enable caching
```javascript
// In webpack config
cache: { type: 'filesystem' }
```

---

## 5. API & Server Issues

### 5.1 HTTP Errors

**Problem: 500 Internal Server Error**

Solution 1: Check server logs
```bash
npm run dev              # Start server
# Look at console output
```

Solution 2: Enable debugging
```bash
DEBUG=* npm run dev
```

Solution 3: Check error logs
```bash
tail -f logs/error.log
```

**Problem: 401 Unauthorized**

Solution: Verify authentication
```bash
# Check if token exists
echo $AUTH_TOKEN

# Test with token
curl -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/users

# Verify token is valid
npm run validate:token
```

**Problem: 404 Not Found**

Solution: Verify endpoint exists
```bash
# List all routes
npm run routes:list

# Check request path
curl -v http://localhost:3000/api/users

# Verify controller exists
ls src/controllers/
```

### 5.2 CORS Issues

**Problem: CORS error in browser console**

Solution 1: Check CORS configuration
```javascript
const cors = require('cors');
app.use(cors({
  origin: ['http://localhost:3000', 'https://example.com'],
  credentials: true
}));
```

Solution 2: Test with curl
```bash
curl -H "Origin: http://localhost:3000" http://localhost:3001/api/users
```

---

## 6. Deployment Issues

### 6.1 Docker Deployment

**Problem: Container won't start**

Solution 1: Check logs
```bash
docker logs container-name
docker logs -f container-name  # Follow logs
```

Solution 2: Debug container
```bash
docker run -it image-name /bin/sh
# Check environment, files, etc.
```

Solution 3: Verify entry point
```dockerfile
# Ensure ENTRYPOINT or CMD is correct
CMD ["npm", "start"]
```

### 6.2 Kubernetes Deployment

**Problem: Pod won't start**

Solution 1: Check pod status
```bash
kubectl describe pod pod-name
kubectl logs pod-name
```

Solution 2: Check image exists
```bash
kubectl get pods
docker images | grep myimage
```

Solution 3: Verify configuration
```bash
kubectl get configmap
kubectl describe configmap config-name
```

**Problem: Service not accessible**

Solution 1: Check service
```bash
kubectl get services
kubectl describe service service-name
```

Solution 2: Test port forwarding
```bash
kubectl port-forward service-name 3000:3000
curl http://localhost:3000
```

---

## 7. Performance Issues

### 7.1 High CPU Usage

**Problem: CPU at 100%**

Solution 1: Identify process
```bash
top                     # Interactive
ps aux | grep node      # Find process
```

Solution 2: Profile application
```bash
node --prof app.js
node --prof-process isolate-*.log > profile.txt
```

Solution 3: Check for infinite loops
```bash
# Add logging to identify stuck code
logger.debug('Starting loop');
for (const item of items) {
  logger.debug('Processing:', item);
  // Find where logging stops
}
```

### 7.2 High Memory Usage

**Problem: Memory keeps growing**

Solution 1: Check for memory leaks
```bash
node --max-old-space-size=4096 app.js
```

Solution 2: Profile memory
```bash
node --inspect app.js
# Use Chrome DevTools for memory profiling
```

Solution 3: Check for circular references
```javascript
// Example of memory leak
let cache = {};
function addToCache(key, value) {
  cache[key] = value;
  value.reference = cache;  // Circular reference!
}
```

### 7.3 Database Slow Queries

**Problem: Queries are slow**

Solution 1: Use EXPLAIN
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE id = 1;
```

Solution 2: Add indexes
```sql
CREATE INDEX idx_users_id ON users(id);
CREATE INDEX idx_users_email ON users(email);
```

Solution 3: Optimize query
```javascript
// Instead of N+1 queries:
for (const user of users) {
  user.posts = await Post.find({ userId: user.id });
}

// Use join:
const users = await User.find().populate('posts');
```

---

## 8. Security Issues

### 8.1 Vulnerability Scanning

**Problem: Vulnerabilities found in dependencies**

Solution 1: Update package
```bash
npm audit
npm audit fix
npm audit fix --force  # If needed
```

Solution 2: Review vulnerability
```bash
npm audit --json | grep vulnerability
# Review fix carefully before force updating
```

### 8.2 Secret Exposure

**Problem: Secrets committed to repository**

Solution 1: Immediately rotate secrets
```bash
# Change all passwords
# Revoke all tokens
# Update credentials
```

Solution 2: Remove from history
```bash
git filter-branch --tree-filter 'rm -f .env' HEAD
# or use BFG Repo-Cleaner
```

Solution 3: Prevent future commits
```bash
# Use git-secrets
git secrets --install
git secrets --register-aws
```

---

## 9. Network Issues

### 9.1 Connection Problems

**Problem: Can't connect to external API**

Solution 1: Check network connectivity
```bash
ping external-api.com
curl -v https://external-api.com/health
```

Solution 2: Check proxy settings
```bash
npm config get https-proxy
npm config set https-proxy http://proxy.company.com:8080
```

Solution 3: Check firewall
```bash
# On macOS
sudo lsof -i -P -n | grep LISTEN

# On Linux
sudo ss -tulpn | grep LISTEN
```

### 9.2 DNS Issues

**Problem: Cannot resolve hostname**

Solution 1: Check DNS
```bash
nslookup example.com
dig example.com
```

Solution 2: Flush DNS cache
```bash
# macOS
sudo dscacheutil -flushcache

# Linux
sudo systemctl restart nscd
```

---

## 10. Git Advanced Troubleshooting

### 10.1 Undoing Changes

**Problem: Need to undo recent commits**

Solution 1: Soft reset (keep changes)
```bash
git reset --soft HEAD~1
# Make new commit
git commit -m "Fixed commit message"
```

Solution 2: Hard reset (discard changes)
```bash
git reset --hard HEAD~1
# Lost the commit forever (use reflog if needed)
```

Solution 3: Revert (create inverse commit)
```bash
git revert HEAD
# Creates new commit that undoes changes
```

### 10.2 Finding Lost Commits

**Problem: Lost important commit**

Solution: Use reflog
```bash
git reflog                    # See all HEAD references
git reset --hard <commit>    # Go back to commit
```

---

## 11. Quick Diagnostic Commands

### Health Check Script

```bash
#!/bin/bash
echo "=== Development Environment Check ==="

echo "✓ Node.js:"
node --version

echo "✓ npm:"
npm --version

echo "✓ Git:"
git --version

echo "✓ Docker:"
docker --version

echo "✓ Docker running:"
docker ps > /dev/null && echo "Running" || echo "Not running"

echo "✓ Dependencies:"
npm list 2>/dev/null | head -5

echo "✓ Tests:"
npm test -- --listTests 2>/dev/null | wc -l

echo "=== All systems operational! ==="
```

### Debugging Checklist

- [ ] Restart terminal/IDE
- [ ] Clear caches (`npm cache clean --force`)
- [ ] Update dependencies (`npm update`)
- [ ] Check Node version (`node --version`)
- [ ] Check environment variables (`env | grep DB_`)
- [ ] Check Docker daemon (`docker ps`)
- [ ] Review logs (`npm run dev` output)
- [ ] Test locally (`curl http://localhost:3000`)
- [ ] Check network (`ping external-api.com`)
- [ ] Review error messages carefully

---

## 12. Getting Help

### Escalation Path

1. **Check Quick Reference Guide**
   - `/quick_reference.md` for commands
   - `/glossary.md` for terms

2. **Search Documentation**
   - Search relevant doc sections
   - Check examples

3. **Ask Team**
   - Post in Slack
   - Pair program
   - Code review

4. **External Resources**
   - Stack Overflow
   - GitHub issues
   - Official documentation

### Reporting Issues

When reporting a problem, include:
- [ ] Error message (full stack trace)
- [ ] Steps to reproduce
- [ ] Environment (OS, Node version, etc.)
- [ ] Expected vs actual behavior
- [ ] What you've already tried

---

## 13. Prevention Tips

### Common Prevention Practices

**Prevent port conflicts:**
```bash
# Use random available port
PORT=0 npm run dev
```

**Prevent npm issues:**
```bash
# Regular maintenance
npm audit fix
npm update
npm cache clean --force
```

**Prevent merge conflicts:**
```bash
# Keep branches short-lived
# Pull frequently
git pull origin main
```

**Prevent secrets exposure:**
```bash
# Use .env files
# Enable pre-commit hooks
git secrets --install
```

**Prevent deployment issues:**
```bash
# Test locally first
npm run build
npm test
docker build -t app:test .
```

---

## Conclusion

Most issues have simple solutions. Use this guide systematically: **identify → diagnose → fix → verify → prevent**. When stuck, don't hesitate to reach out to team members! 🚀

