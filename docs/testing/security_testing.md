# Security Testing Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Security Testing Guide
**Focus:** 50+ security testing techniques

---

## 🔐 Security Testing Fundamentals

### OWASP Top 10 Testing

```typescript
describe('Security Tests - OWASP Top 10', () => {
  const api = 'http://localhost:3000/api';

  describe('1. Injection', () => {
    it('should prevent SQL injection', async () => {
      const response = await request(app)
        .post(`${api}/features`)
        .send({
          name: "'; DROP TABLE features; --",
          priority: 10
        });

      expect(response.status).toBe(400);
      
      // Verify table still exists
      const features = await db.features.findAll();
      expect(features).toBeDefined();
    });

    it('should prevent NoSQL injection', async () => {
      const response = await request(app)
        .get(`${api}/features`)
        .query({
          name: { $ne: '' }
        });

      expect(response.status).toBe(400);
    });

    it('should prevent command injection', async () => {
      const response = await request(app)
        .post(`${api}/deploy`)
        .send({
          command: 'ls; rm -rf /'
        });

      expect(response.status).toBe(400);
    });
  });

  describe('2. Broken Authentication', () => {
    it('should enforce strong passwords', async () => {
      const response = await request(app)
        .post(`${api}/auth/register`)
        .send({
          email: 'user@example.com',
          password: '123'
        });

      expect(response.status).toBe(400);
      expect(response.body).toContain('password too weak');
    });

    it('should implement rate limiting', async () => {
      let response;
      for (let i = 0; i < 10; i++) {
        response = await request(app)
          .post(`${api}/auth/login`)
          .send({
            email: 'user@example.com',
            password: 'wrong'
          });
      }

      expect(response.status).toBe(429); // Too Many Requests
    });

    it('should expire sessions', async () => {
      const token = generateToken({ userId: '1' }, { expiresIn: '1s' });

      await new Promise(resolve => setTimeout(resolve, 2000));

      const response = await request(app)
        .get(`${api}/profile`)
        .set('Authorization', `Bearer ${token}`);

      expect(response.status).toBe(401);
    });
  });

  describe('3. Sensitive Data Exposure', () => {
    it('should not expose sensitive data in logs', async () => {
      const logSpy = jest.spyOn(console, 'log');

      await request(app)
        .post(`${api}/auth/login`)
        .send({
          email: 'user@example.com',
          password: 'secretpassword'
        });

      expect(logSpy).not.toHaveBeenCalledWith(
        expect.stringContaining('secretpassword')
      );
    });

    it('should hash passwords', async () => {
      const user = await db.users.findOne({ email: 'user@example.com' });
      
      expect(user.password).not.toBe('plaintext');
      expect(user.password).toMatch(/^\$2[aby]\$/); // bcrypt format
    });

    it('should use HTTPS', async () => {
      const response = await fetch('http://localhost:3000/api/sensitive');
      expect(response.status).not.toBe(200);
    });
  });

  describe('4. XML External Entities (XXE)', () => {
    it('should prevent XXE attacks', async () => {
      const xxePayload = `<?xml version="1.0"?>
        <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
        <root>&xxe;</root>`;

      const response = await request(app)
        .post(`${api}/upload`)
        .set('Content-Type', 'application/xml')
        .send(xxePayload);

      expect(response.status).toBe(400);
    });
  });

  describe('5. Access Control', () => {
    it('should prevent unauthorized access', async () => {
      const response = await request(app)
        .get(`${api}/admin/users`)
        .set('Authorization', 'Bearer usertoken');

      expect(response.status).toBe(403);
    });

    it('should enforce RBAC', async () => {
      const response = await request(app)
        .delete(`${api}/features/1`)
        .set('Authorization', 'Bearer viewertoken');

      expect(response.status).toBe(403);
    });
  });

  describe('6. CSRF Protection', () => {
    it('should require CSRF token', async () => {
      const response = await request(app)
        .post(`${api}/features`)
        .send({
          name: 'OAuth',
          priority: 10
        });

      expect(response.status).toBe(403); // Forbidden
    });

    it('should validate CSRF token', async () => {
      const csrfToken = 'invalid-token';

      const response = await request(app)
        .post(`${api}/features`)
        .set('X-CSRF-Token', csrfToken)
        .send({
          name: 'OAuth',
          priority: 10
        });

      expect(response.status).toBe(403);
    });
  });

  describe('7. Using Components with Known Vulnerabilities', () => {
    it('should not use vulnerable packages', async () => {
      // Run npm audit
      const { execSync } = require('child_process');
      const auditOutput = execSync('npm audit --json', { encoding: 'utf8' });
      const audit = JSON.parse(auditOutput);

      expect(audit.vulnerabilities).toEqual({});
    });
  });

  describe('8. Insufficient Logging & Monitoring', () => {
    it('should log security events', async () => {
      const logSpy = jest.spyOn(securityLogger, 'warn');

      await request(app)
        .post(`${api}/auth/login`)
        .send({
          email: 'user@example.com',
          password: 'wrong'
        });

      expect(logSpy).toHaveBeenCalledWith(
        expect.stringContaining('Failed login attempt')
      );
    });
  });

  describe('9. Using Weak Cryptography', () => {
    it('should use strong encryption', async () => {
      const token = generateToken({ userId: '1' });

      // Token should be signed with strong algorithm
      const decoded = jwt.decode(token, { complete: true });
      expect(decoded.header.alg).toBe('HS256');
    });
  });

  describe('10. Broken Error Handling', () => {
    it('should not expose stack traces', async () => {
      const response = await request(app)
        .get(`${api}/invalid-endpoint`);

      expect(response.body).not.toContain('at');
      expect(response.body).not.toContain('/src/');
    });
  });
});
```

---

## 🛡️ Advanced Security Testing

### Penetration Testing

```typescript
describe('Penetration Testing', () => {
  it('should prevent Path Traversal', async () => {
    const response = await request(app)
      .get(`${api}/files/../../../../etc/passwd`);

    expect(response.status).toBe(400);
  });

  it('should prevent Header Injection', async () => {
    const response = await request(app)
      .post(`${api}/send`)
      .send({
        recipient: 'user@example.com\r\nBcc: attacker@example.com',
        message: 'test'
      });

    expect(response.status).toBe(400);
  });

  it('should prevent Open Redirect', async () => {
    const response = await request(app)
      .get('/redirect')
      .query({ url: 'https://evil.com' });

    expect(response.status).toBe(400);
  });

  it('should prevent CORS bypass', async () => {
    const response = await request(app)
      .get(`${api}/sensitive`)
      .set('Origin', 'https://evil.com');

    expect(response.headers['access-control-allow-origin']).toBeUndefined();
  });
});
```

### Cryptographic Testing

```typescript
describe('Cryptography', () => {
  it('should use secure random generation', () => {
    const values = new Set();

    for (let i = 0; i < 100; i++) {
      const token = generateSecureToken();
      values.add(token);
    }

    expect(values.size).toBe(100); // All unique
  });

  it('should rotate encryption keys', async () => {
    const oldKey = await keyManager.getCurrentKey();

    await keyManager.rotateKey();

    const newKey = await keyManager.getCurrentKey();
    expect(newKey).not.toBe(oldKey);

    // Old key still works for decryption
    const encrypted = encryptWithKey(oldKey, 'data');
    const decrypted = decryptWithKey(newKey, encrypted);
    expect(decrypted).toBe('data');
  });

  it('should use HTTPS only', async () => {
    const response = await fetch('http://localhost:3000/api');
    
    expect(response.status).not.toBe(200);
    expect(response.url).toMatch(/^https/);
  });
});
```

### Input Validation Testing

```typescript
describe('Input Validation', () => {
  it('should validate email format', async () => {
    const invalidEmails = [
      'notanemail',
      '@example.com',
      'user@',
      'user @example.com'
    ];

    for (const email of invalidEmails) {
      const response = await request(app)
        .post(`${api}/auth/register`)
        .send({ email, password: 'ValidPassword1!' });

      expect(response.status).toBe(400);
    }
  });

  it('should validate file uploads', async () => {
    const response = await request(app)
      .post(`${api}/upload`)
      .attach('file', Buffer.from('malicious.exe'), 'malicious.exe');

    expect(response.status).toBe(400);
  });

  it('should sanitize HTML input', async () => {
    const response = await request(app)
      .post(`${api}/features`)
      .send({
        name: '<script>alert("xss")</script>',
        priority: 10
      });

    const feature = await db.features.findOne({ name: { $regex: '<script>' } });
    expect(feature).toBeUndefined();
  });
});
```

---

## 🔍 SAST/DAST Tools

### Static Application Security Testing

```yaml
# sonarqube config
sonar:
  host: http://sonarqube:9000
  login: token
  projectKey: ai-agent-system
  sources: src
  exclusions:
    - "**/node_modules/**"
    - "**/dist/**"
  rules:
    - key: security
      enable: true
    - key: sql-injection
      enable: true
    - key: xss
      enable: true
```

### Dependency Scanning

```bash
# Automated dependency checking
npm audit
npm audit fix

# OWASP Dependency Check
dependency-check --project "AI Agent System" --scan ./node_modules

# Snyk
snyk test
snyk monitor
```

---

## 🚨 Security Headers

```typescript
describe('Security Headers', () => {
  it('should include HSTS header', async () => {
    const response = await request(app).get('/');

    expect(response.headers['strict-transport-security']).toBeDefined();
    expect(response.headers['strict-transport-security'])
      .toContain('max-age=31536000');
  });

  it('should include CSP header', async () => {
    const response = await request(app).get('/');

    expect(response.headers['content-security-policy']).toBeDefined();
  });

  it('should include X-Frame-Options', async () => {
    const response = await request(app).get('/');

    expect(response.headers['x-frame-options']).toBe('DENY');
  });

  it('should include X-Content-Type-Options', async () => {
    const response = await request(app).get('/');

    expect(response.headers['x-content-type-options']).toBe('nosniff');
  });
});
```

---

## 📚 Related Documents

- Testing Strategies (testing_strategies.md)
- Performance Testing (performance_testing.md)
- Test Automation (test_automation.md)

---

**END OF SECURITY TESTING DOCUMENT**
