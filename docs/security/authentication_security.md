# Authentication Security Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Authentication & Authorization Security Guide
**Focus:** Secure authentication mechanisms and access control

---

## 🔐 Authentication Methods

### Multi-Factor Authentication (MFA)

```typescript
import speakeasy from 'speakeasy';
import QRCode from 'qrcode';

class MFAService {
  async generateTOTP(userId: string): Promise<{ secret: string; qrCode: string }> {
    const secret = speakeasy.generateSecret({
      name: `AI Agent (${userId})`,
      issuer: 'AI Agent System'
    });

    const qrCode = await QRCode.toDataURL(secret.otpauth_url);

    return { secret: secret.base32, qrCode };
  }

  async verifyTOTP(token: string, secret: string): Promise<boolean> {
    return speakeasy.totp.verify({
      secret,
      encoding: 'base32',
      token,
      window: 2
    });
  }

  async sendSMS(phoneNumber: string): Promise<string> {
    const code = this.generateCode();
    // Send via Twilio, AWS SNS, etc.
    return code;
  }

  private generateCode(): string {
    return Math.floor(100000 + Math.random() * 900000).toString();
  }
}
```

### OAuth 2.0 Implementation

```typescript
import passport from 'passport';
import OAuth2Strategy from 'passport-oauth2';

// Configure OAuth strategy
passport.use(new OAuth2Strategy({
  authorizationURL: 'https://auth.example.com/oauth/authorize',
  tokenURL: 'https://auth.example.com/oauth/token',
  clientID: process.env.OAUTH_CLIENT_ID,
  clientSecret: process.env.OAUTH_CLIENT_SECRET,
  callbackURL: '/auth/callback'
}, (accessToken, refreshToken, profile, done) => {
  // Verify user
  User.findOrCreate({ id: profile.id }, (error, user) => {
    return done(error, user);
  });
}));

// Routes
app.get('/auth/login', passport.authenticate('oauth2'));

app.get('/auth/callback',
  passport.authenticate('oauth2', { failureRedirect: '/login' }),
  (req, res) => {
    res.redirect('/dashboard');
  }
);
```

### JWT Implementation

```typescript
import jwt from 'jsonwebtoken';

class JWTService {
  private accessTokenSecret = process.env.JWT_ACCESS_SECRET;
  private refreshTokenSecret = process.env.JWT_REFRESH_SECRET;

  generateAccessToken(userId: string): string {
    return jwt.sign(
      { userId, type: 'access' },
      this.accessTokenSecret,
      { expiresIn: '15m', algorithm: 'HS256' }
    );
  }

  generateRefreshToken(userId: string): string {
    return jwt.sign(
      { userId, type: 'refresh' },
      this.refreshTokenSecret,
      { expiresIn: '7d', algorithm: 'HS256' }
    );
  }

  verifyAccessToken(token: string): any {
    try {
      return jwt.verify(token, this.accessTokenSecret, {
        algorithms: ['HS256']
      });
    } catch (error) {
      throw new Error('Invalid token');
    }
  }

  refreshAccessToken(refreshToken: string): string {
    try {
      const decoded = jwt.verify(refreshToken, this.refreshTokenSecret);
      return this.generateAccessToken(decoded.userId);
    } catch (error) {
      throw new Error('Invalid refresh token');
    }
  }
}

// Middleware
const authenticateJWT = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'No token' });
  }

  try {
    const decoded = jwtService.verifyAccessToken(token);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(403).json({ error: 'Invalid token' });
  }
};
```

---

## 👥 Authorization & RBAC

```typescript
interface Role {
  name: string;
  permissions: Set<string>;
}

class RBAC {
  private roles = new Map<string, Role>();
  private userRoles = new Map<string, Set<string>>();

  defineRole(name: string, permissions: string[]): void {
    this.roles.set(name, {
      name,
      permissions: new Set(permissions)
    });
  }

  assignRole(userId: string, role: string): void {
    if (!this.userRoles.has(userId)) {
      this.userRoles.set(userId, new Set());
    }
    this.userRoles.get(userId)!.add(role);
  }

  hasPermission(userId: string, permission: string): boolean {
    const roles = this.userRoles.get(userId) || new Set();
    
    for (const roleName of roles) {
      const role = this.roles.get(roleName);
      if (role?.permissions.has(permission)) {
        return true;
      }
    }
    
    return false;
  }
}

// Usage
app.post('/api/admin/users',
  authenticate,
  authorize(rbac, 'create_users'),
  (req, res) => {
    // Create user
  }
);
```

---

## 🔑 Password Security

```typescript
class PasswordPolicy {
  validate(password: string): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    // Minimum length
    if (password.length < 12) {
      errors.push('Password must be at least 12 characters');
    }

    // Uppercase
    if (!/[A-Z]/.test(password)) {
      errors.push('Password must contain uppercase letter');
    }

    // Lowercase
    if (!/[a-z]/.test(password)) {
      errors.push('Password must contain lowercase letter');
    }

    // Numbers
    if (!/[0-9]/.test(password)) {
      errors.push('Password must contain number');
    }

    // Special characters
    if (!/[!@#$%^&*]/.test(password)) {
      errors.push('Password must contain special character');
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  async hash(password: string): Promise<string> {
    return bcrypt.hash(password, 12);
  }

  async verify(password: string, hash: string): Promise<boolean> {
    return bcrypt.compare(password, hash);
  }
}
```

---

## 🛡️ Session Security

```typescript
import RedisStore from 'connect-redis';

app.use(session({
  store: new RedisStore({ client: redis }),
  secret: process.env.SESSION_SECRET,
  name: 'sessionId',
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    sameSite: 'strict',
    maxAge: 24 * 60 * 60 * 1000 // 24 hours
  }
}));

// Session renewal
app.use((req, res, next) => {
  req.session.touch();
  next();
});

// Logout
app.post('/logout', (req, res) => {
  req.session.destroy((error) => {
    if (error) {
      logger.error('Session destruction failed', { error });
    }
    res.clearCookie('sessionId');
    res.json({ success: true });
  });
});
```

---

## 📊 Authentication Monitoring

```typescript
class AuthenticationMonitor {
  async monitorFailedAttempts(userId: string): Promise<void> {
    const attempts = await redis.incr(`failed_login:${userId}`);
    
    if (attempts === 1) {
      await redis.expire(`failed_login:${userId}`, 300); // 5 minutes
    }

    if (attempts > 5) {
      logger.warn('Multiple failed login attempts', { userId, attempts });
      await this.lockAccount(userId, 15); // 15 minute lockout
    }
  }

  async monitorAnomalousActivity(userId: string, context: any): Promise<void> {
    const userProfile = await this.getUserProfile(userId);
    
    // Check location
    if (context.location !== userProfile.lastLocation) {
      logger.info('Unusual location', { userId, location: context.location });
      // Trigger additional verification
    }

    // Check time
    if (!this.isNormalTimeOfAccess(context.time, userProfile.usagePatterns)) {
      logger.info('Unusual access time', { userId, time: context.time });
    }

    // Check device
    if (context.deviceId !== userProfile.knownDevices) {
      logger.info('Unknown device', { userId, deviceId: context.deviceId });
      // Send verification email
    }
  }

  private isNormalTimeOfAccess(time: Date, patterns: any): boolean {
    const hour = time.getHours();
    return hour >= 6 && hour <= 22;
  }
}
```

---

## 📚 Related Documents

- Security Overview (security_overview.md)
- Secure Coding (secure_coding.md)
- Encryption (encryption.md)
- Network Security (network_security.md)

---

**END OF AUTHENTICATION SECURITY DOCUMENT**
