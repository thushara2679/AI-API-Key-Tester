# Encryption Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Encryption Strategies Guide
**Focus:** Data encryption at rest and in transit

---

## 🔐 Encryption at Rest

### Database Encryption

```sql
-- PostgreSQL with pgcrypto
CREATE EXTENSION pgcrypto;

-- Encrypt sensitive columns
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255),
  password TEXT,
  ssn TEXT ENCRYPTED WITH (CIPHER 'aes-256-cbc')
);

-- Encrypt data
INSERT INTO users (email, password, ssn) VALUES (
  'user@example.com',
  crypt('password123', gen_salt('bf')),
  pgp_sym_encrypt('123-45-6789', 'encryption_key')
);
```

### File Encryption

```typescript
import crypto from 'crypto';
import fs from 'fs';

class FileEncryption {
  private algorithm = 'aes-256-cbc';
  private key = crypto.scryptSync(process.env.ENCRYPTION_KEY, 'salt', 32);

  encryptFile(filePath: string, outputPath: string): void {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(this.algorithm, this.key, iv);

    const input = fs.createReadStream(filePath);
    const output = fs.createWriteStream(outputPath);

    output.write(iv);
    input.pipe(cipher).pipe(output);
  }

  decryptFile(filePath: string, outputPath: string): void {
    const input = fs.createReadStream(filePath);
    const iv = Buffer.alloc(16);

    input.on('readable', () => {
      const chunk = input.read(16);
      if (chunk) {
        chunk.copy(iv);
        
        const decipher = crypto.createDecipheriv(this.algorithm, this.key, iv);
        input.pipe(decipher).pipe(fs.createWriteStream(outputPath));
      }
    });
  }
}
```

### Key Management

```bash
#!/bin/bash
# Key management

# Generate encryption key
openssl rand -base64 32 > encryption.key

# Store in environment variable
export ENCRYPTION_KEY=$(cat encryption.key)

# Rotate encryption key (re-encrypt with new key)
./scripts/rotate-encryption-key.sh

# Store keys in HSM or KMS
# AWS KMS
aws kms create-key --description "AI Agent Encryption Key"

# Azure Key Vault
az keyvault create --name ai-agent-vault --resource-group mygroup
```

---

## 🔒 Encryption in Transit

### TLS/SSL Configuration

```nginx
# nginx.conf - TLS configuration

server {
  listen 443 ssl http2;
  server_name example.com;

  # TLS Certificate
  ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

  # TLS Version - Use 1.3 and 1.2 only
  ssl_protocols TLSv1.2 TLSv1.3;

  # Cipher suites
  ssl_ciphers HIGH:!aNULL:!MD5;
  ssl_prefer_server_ciphers on;

  # HSTS - Force HTTPS
  add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

  # Session configuration
  ssl_session_timeout 1d;
  ssl_session_cache shared:SSL:50m;
  ssl_session_tickets off;
}

# Redirect HTTP to HTTPS
server {
  listen 80;
  server_name example.com;
  return 301 https://$server_name$request_uri;
}
```

### API Encryption

```typescript
// ✅ SECURE - HTTPS with encryption
import https from 'https';
import fs from 'fs';
import express from 'express';

const app = express();

const options = {
  key: fs.readFileSync('/path/to/private.key'),
  cert: fs.readFileSync('/path/to/certificate.crt')
};

https.createServer(options, app).listen(3000);

// Encrypt sensitive fields in request/response
app.post('/api/payment', (req, res) => {
  const encryptedPayload = encryptData(req.body);
  // Process payment
  const encryptedResponse = encryptData(result);
  res.json(encryptedResponse);
});
```

---

## 🔑 Key Encryption Key (KEK) Strategy

```typescript
class KeyManagementService {
  private kekProvider: KmsProvider; // AWS KMS, Azure Key Vault, etc.

  async encryptDataKey(plaintext: Buffer): Promise<Buffer> {
    // Data key encrypted with Master Key
    const dataKey = crypto.randomBytes(32);
    return this.kekProvider.encrypt(dataKey);
  }

  async decryptDataKey(encrypted: Buffer): Promise<Buffer> {
    // Decrypt data key with Master Key
    return this.kekProvider.decrypt(encrypted);
  }

  async encryptSensitiveData(plaintext: string): Promise<string> {
    // Generate data key
    const dataKey = await this.encryptDataKey(Buffer.from(''));
    
    // Encrypt data
    const encryptedData = this.encryptWithDataKey(plaintext, dataKey);
    
    // Return data + encrypted key
    return `${encryptedData}:${dataKey.toString('base64')}`;
  }

  private encryptWithDataKey(plaintext: string, key: Buffer): string {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
    
    let encrypted = cipher.update(plaintext, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    return `${iv.toString('hex')}:${encrypted}`;
  }
}
```

---

## 🌐 End-to-End Encryption

```typescript
// Client-side encryption
class E2EEncryption {
  private clientKeyPair: KeyPair;

  async encryptMessage(message: string, recipientPublicKey: string): Promise<string> {
    const encrypted = await this.encrypt(
      message,
      recipientPublicKey
    );
    return encrypted;
  }

  async decryptMessage(encryptedMessage: string, privateKey: string): Promise<string> {
    const decrypted = await this.decrypt(
      encryptedMessage,
      privateKey
    );
    return decrypted;
  }
}

// Server never has access to plaintext
app.post('/api/messages', async (req, res) => {
  // Encrypted message stored as-is
  const message = await Message.create({
    fromUserId: req.user.id,
    toUserId: req.body.toUserId,
    encryptedContent: req.body.encryptedContent, // Can't decrypt server-side
    timestamp: new Date()
  });

  res.json(message);
});
```

---

## 📊 Encryption Best Practices

```yaml
Data Classification:
  Public:
    - No encryption required
    - Cache-friendly
  
  Confidential:
    - Encrypt at rest
    - TLS in transit
    - Access controls
  
  Restricted:
    - AES-256 encryption
    - Key rotation
    - Audit logging

Encryption Algorithms:
  Symmetric:
    - AES-256 for data
    - HMAC-SHA256 for integrity
  
  Asymmetric:
    - RSA-2048 for key exchange
    - ECDSA for signatures
  
  Hashing:
    - bcrypt for passwords
    - SHA-256 for integrity

Key Management:
  - Separate encryption/decryption keys
  - Rotate keys regularly
  - Store in secure location (KMS)
  - Never hardcode keys
  - Audit key access

Certificate Management:
  - Use strong algorithms (SHA-256+)
  - Set expiration dates
  - Automate renewal (Let's Encrypt)
  - Monitor expiration
```

---

## 📚 Related Documents

- Security Overview (security_overview.md)
- Secure Coding (secure_coding.md)
- Authentication Security (authentication_security.md)

---

**END OF ENCRYPTION DOCUMENT**
