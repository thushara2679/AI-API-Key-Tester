# Secure Coding Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Secure Coding Practices Guide
**Focus:** Secure development patterns and practices

---

## 📝 Input Validation

```typescript
// ✅ SECURE - Whitelist validation
function validateEmail(email: string): boolean {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return pattern.test(email) && email.length <= 255;
}

// ✅ SECURE - Type checking
function processNumber(value: unknown): number {
  if (typeof value !== 'number') {
    throw new Error('Invalid type');
  }
  if (value < 0 || value > 1000) {
    throw new Error('Out of range');
  }
  return value;
}

// ✅ SECURE - Array validation
function validateArray(items: unknown): string[] {
  if (!Array.isArray(items)) {
    throw new Error('Must be array');
  }
  if (items.length === 0 || items.length > 100) {
    throw new Error('Invalid array size');
  }
  return items.map(item => {
    if (typeof item !== 'string') {
      throw new Error('Invalid item type');
    }
    return item.trim().substring(0, 100);
  });
}
```

---

## 🛡️ Output Encoding

```typescript
// ✅ SECURE - HTML encoding
function encodeHTML(text: string): string {
  const map: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  };
  return text.replace(/[&<>"']/g, char => map[char]);
}

// ✅ SECURE - JavaScript escaping
function encodeJS(text: string): string {
  return text.replace(/[\\"\n\r\u2028\u2029]/g, char => {
    const code = char.charCodeAt(0);
    return `\\u${code.toString(16).padStart(4, '0')}`;
  });
}

// ✅ SECURE - Template literals with escaping
const safe = html`<div>${encodeHTML(userInput)}</div>`;
```

---

## 🔐 Cryptography Usage

```typescript
import crypto from 'crypto';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

// ✅ SECURE - Password hashing
async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, 10);
}

async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// ✅ SECURE - Encryption
function encryptData(plaintext: string, key: Buffer): string {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
  
  let encrypted = cipher.update(plaintext, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  return iv.toString('hex') + ':' + encrypted;
}

// ✅ SECURE - JWT signing
function generateToken(userId: string, secret: string): string {
  return jwt.sign(
    { userId },
    secret,
    { expiresIn: '1h', algorithm: 'HS256' }
  );
}

function verifyToken(token: string, secret: string): any {
  try {
    return jwt.verify(token, secret, { algorithms: ['HS256'] });
  } catch (error) {
    throw new Error('Invalid token');
  }
}
```

---

## 🔍 Error Handling

```typescript
// ❌ VULNERABLE - Leaks information
app.get('/api/data', (req, res) => {
  try {
    const data = db.query(req.query.id);
    res.json(data);
  } catch (error) {
    res.status(500).json({ error: error.stack }); // Stack trace exposed!
  }
});

// ✅ SECURE - Generic errors with logging
app.get('/api/data', (req, res) => {
  try {
    if (!req.query.id) {
      return res.status(400).json({ error: 'Missing parameter' });
    }
    const data = db.query(req.query.id);
    res.json(data);
  } catch (error) {
    logger.error('Database error', {
      error: error.message,
      stack: error.stack,
      userId: req.user?.id,
      timestamp: new Date()
    });
    res.status(500).json({ error: 'Internal server error' });
  }
});
```

---

## 🔒 Authentication & Authorization

```typescript
// ✅ SECURE - Role-based access control
interface AuthContext {
  userId: string;
  roles: string[];
  permissions: Set<string>;
}

function authorize(...requiredRoles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    const hasRole = requiredRoles.some(role => req.user.roles.includes(role));
    
    if (!hasRole) {
      logger.warn('Unauthorized access attempt', {
        userId: req.user.id,
        requiredRoles,
        resource: req.path
      });
      return res.status(403).json({ error: 'Forbidden' });
    }
    
    next();
  };
}

// Usage
app.delete('/api/admin/users/:id', 
  authenticate,
  authorize('admin'),
  (req, res) => {
    // Delete user
  }
);
```

---

## 🔐 Session Management

```typescript
// ✅ SECURE - Secure session configuration
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: true,        // HTTPS only
    httpOnly: true,      // JavaScript cannot access
    sameSite: 'strict',  // CSRF protection
    maxAge: 3600000      // 1 hour
  }
}));

// ✅ SECURE - Session invalidation
app.post('/logout', (req, res) => {
  req.session.destroy((error) => {
    if (error) {
      logger.error('Session destruction failed', { error });
    }
    res.clearCookie('connect.sid');
    res.json({ success: true });
  });
});
```

---

## 🚫 Security Anti-Patterns

```typescript
// ❌ AVOID: Direct object reference
app.get('/api/users/:id', (req, res) => {
  const user = db.users.findById(req.params.id); // No auth check
  res.json(user);
});

// ❌ AVOID: Eval usage
const result = eval(userInput); // Never do this!

// ❌ AVOID: Hardcoded secrets
const API_KEY = 'sk_live_123456'; // Don't hardcode!

// ❌ AVOID: Weak random generation
const token = Math.random().toString(36); // Not cryptographically secure

// ❌ AVOID: Storing passwords in plain text
user.password = req.body.password; // NEVER!

// ❌ AVOID: No HTTPS
app.listen(3000); // Should use HTTPS in production

// ❌ AVOID: No rate limiting
app.post('/api/login', (req, res) => {
  // Unlimited attempts possible
});
```

---

## ✅ Secure Coding Checklist

```yaml
Input Validation:
  - Whitelist validation
  - Type checking
  - Length limits
  - Format validation
  - Range checking

Output Encoding:
  - HTML encoding
  - URL encoding
  - JavaScript escaping
  - Context-aware encoding

Cryptography:
  - Strong algorithms (AES-256)
  - Proper key management
  - Secure random generation
  - Regular key rotation

Authentication:
  - Strong password policy
  - Multi-factor authentication
  - Secure password storage (bcrypt)
  - Session timeout
  - Secure session cookies

Authorization:
  - Principle of least privilege
  - Role-based access control
  - Resource-level checks
  - Action auditing

Error Handling:
  - Generic error messages
  - Detailed logging
  - No sensitive data in errors
  - Proper HTTP status codes

Logging & Monitoring:
  - Security events logged
  - Suspicious activity monitored
  - Alerts configured
  - Regular review

Dependencies:
  - Minimal dependencies
  - Regular updates
  - Vulnerability scanning
  - Security patches
```

---

## 📚 Related Documents

- Security Overview (security_overview.md)
- OWASP Top 10 (owasp_top_10.md)
- Encryption (encryption.md)

---

**END OF SECURE CODING DOCUMENT**
