# OWASP Top 10 Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** OWASP Top 10 Vulnerabilities Guide
**Focus:** Testing and mitigation for 2023 vulnerabilities

---

## 🎯 OWASP Top 10 (2023)

### 1. Broken Access Control

**Vulnerability:**
```typescript
// ❌ VULNERABLE
app.get('/api/users/:id', (req, res) => {
  const user = db.users.findById(req.params.id);
  res.json(user); // No authorization check
});

// ✅ SECURE
app.get('/api/users/:id', authenticate, authorize('admin'), (req, res) => {
  if (req.user.id !== req.params.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  const user = db.users.findById(req.params.id);
  res.json(user);
});
```

**Testing:**
```typescript
describe('Broken Access Control', () => {
  it('should deny access without auth', async () => {
    const response = await request(app)
      .get('/api/users/123');
    expect(response.status).toBe(401);
  });
  
  it('should deny cross-user access', async () => {
    const response = await request(app)
      .get('/api/users/456')
      .set('Authorization', 'Bearer user123Token');
    expect(response.status).toBe(403);
  });
});
```

---

### 2. Cryptographic Failures

**Vulnerability:**
```typescript
// ❌ VULNERABLE - No encryption
const password = user.password; // Plain text storage
const apiResponse = sendOverHTTP(data); // Unencrypted

// ✅ SECURE
const bcrypt = require('bcrypt');
const hashedPassword = await bcrypt.hash(password, 10);

// TLS for transit
app.use(helmet.hsts({ maxAge: 31536000 }));

// AES-256 for sensitive data
const encryptedData = encrypt(sensitiveData, secretKey);
```

---

### 3. Injection

**SQL Injection - Vulnerable:**
```typescript
// ❌ VULNERABLE
const query = `SELECT * FROM users WHERE email = '${email}'`;
db.query(query); // Email: admin'--

// ✅ SECURE
const query = 'SELECT * FROM users WHERE email = ?';
db.query(query, [email]);
```

**NoSQL Injection - Secure:**
```typescript
// ❌ VULNERABLE
const user = db.users.findOne({ email: req.body.email });

// ✅ SECURE - Validate/sanitize input
const email = validator.isEmail(req.body.email);
if (!email) throw new Error('Invalid email');
const user = db.users.findOne({ email });
```

**Command Injection:**
```typescript
// ❌ VULNERABLE
exec(`convert ${fileName} output.jpg`);

// ✅ SECURE
execFile('convert', [fileName, 'output.jpg']);
```

---

### 4. Insecure Design

**Vulnerability:**
```typescript
// ❌ VULNERABLE - No rate limiting, weak password policy
app.post('/api/auth/login', (req, res) => {
  // Multiple attempts allowed
  // Weak password requirements
});

// ✅ SECURE - With design patterns
app.post('/api/auth/login', 
  rateLimiter,
  validatePasswordPolicy,
  authenticate,
  (req, res) => {
    // Implementation
  }
);
```

---

### 5. Security Misconfiguration

**Vulnerability:**
```typescript
// ❌ VULNERABLE - Security headers missing
app.use(express.json());
app.listen(3000);

// ✅ SECURE - Proper configuration
app.use(helmet());
app.use(cors({
  origin: ['https://example.com'],
  credentials: true
}));
app.use(express.json({ limit: '10kb' }));
app.listen(3000, 'localhost');
```

**Configuration Check:**
```yaml
Security Checklist:
  - Default credentials changed
  - Unnecessary services disabled
  - Security headers configured
  - Error messages generic
  - Debug mode disabled
  - Dependencies updated
  - SSL/TLS enabled
  - Database isolated
```

---

### 6. Vulnerable Components

**Vulnerability:**
```bash
# ❌ Check for vulnerabilities
npm audit

# ✅ Fix vulnerabilities
npm audit fix
npm update

# Regular scanning
snyk test
npm audit --production
```

---

### 7. Authentication Failures

**Vulnerability:**
```typescript
// ❌ VULNERABLE
app.post('/login', (req, res) => {
  const user = db.users.findOne({ email: req.body.email });
  if (user.password === req.body.password) {
    res.json({ token: user.id });
  }
});

// ✅ SECURE
app.post('/login', async (req, res) => {
  const user = db.users.findOne({ email: req.body.email });
  if (!user) return res.status(401).json({ error: 'Invalid' });
  
  const validPassword = await bcrypt.compare(req.body.password, user.hashedPassword);
  if (!validPassword) return res.status(401).json({ error: 'Invalid' });
  
  const token = jwt.sign({ userId: user.id }, SECRET, { expiresIn: '1h' });
  res.json({ token });
});
```

---

### 8. Data Integrity Failures

**Vulnerability:**
```typescript
// ❌ VULNERABLE - No signature verification
const user = jwt.decode(token);

// ✅ SECURE - Verify signature
try {
  const user = jwt.verify(token, SECRET);
} catch (error) {
  return res.status(401).json({ error: 'Invalid token' });
}
```

---

### 9. Logging & Monitoring Failures

**Vulnerability:**
```typescript
// ❌ VULNERABLE
app.get('/api/data', (req, res) => {
  const data = db.getData();
  res.json(data); // No logging
});

// ✅ SECURE
app.get('/api/data', (req, res) => {
  logger.info('Data accessed', {
    userId: req.user.id,
    timestamp: new Date(),
    ip: req.ip
  });
  
  const data = db.getData();
  res.json(data);
});
```

---

### 10. SSRF (Server-Side Request Forgery)

**Vulnerability:**
```typescript
// ❌ VULNERABLE
app.post('/api/fetch', (req, res) => {
  const url = req.body.url;
  fetch(url).then(response => res.json(response));
});

// ✅ SECURE - Whitelist URLs
const allowedDomains = ['api.example.com'];

app.post('/api/fetch', (req, res) => {
  const url = new URL(req.body.url);
  if (!allowedDomains.includes(url.hostname)) {
    return res.status(403).json({ error: 'Forbidden domain' });
  }
  fetch(url).then(response => res.json(response));
});
```

---

## 🧪 OWASP Testing Techniques

### XSS Prevention

```typescript
// ✅ SECURE - Use templating
<div>{{ userInput }}</div> // Auto-escaped

// ✅ SECURE - Sanitize
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userInput);

// ✅ SECURE - Encode output
const escaped = html`<div>${userInput}</div>`;
```

### CSRF Protection

```typescript
app.use(csrf());

// Generate token
app.get('/form', (req, res) => {
  res.render('form', { csrfToken: req.csrfToken() });
});

// Verify token
app.post('/api/action', csrfProtection, (req, res) => {
  // Process action
});
```

---

## 📚 Related Documents

- Penetration Testing (penetration_testing.md)
- Secure Coding (secure_coding.md)
- Vulnerability Assessment (vulnerability_assessment.md)

---

**END OF OWASP TOP 10 DOCUMENT**
