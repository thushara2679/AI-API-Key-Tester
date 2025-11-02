# App Distribution Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** App Distribution & Deployment Guide
**Focus:** iOS, Android, desktop, and web deployment

---

## 📱 iOS App Store Distribution

### Code Signing & Provisioning

```bash
# Generate certificate signing request (CSR)
# Use Keychain Access on macOS

# Create App ID
# Go to Apple Developer Portal > Identifiers > App IDs
# Register new App ID with Bundle ID: com.example.app

# Create provisioning profile
# Development profile for testing
# Ad Hoc profile for distribution

# In Xcode:
# Project > Signing & Capabilities > Team
# Automatically manage signing enabled
```

### Build for Release

```bash
#!/bin/bash
# build-ios.sh

# Set build settings
xcodebuild archive \
  -workspace FeatureApp.xcworkspace \
  -scheme FeatureApp \
  -configuration Release \
  -archivePath ./build/FeatureApp.xcarchive \
  CODE_SIGN_IDENTITY="iPhone Distribution" \
  PROVISIONING_PROFILE_SPECIFIER="Distribution Profile"

# Export to ipa
xcodebuild -exportArchive \
  -archivePath ./build/FeatureApp.xcarchive \
  -exportOptionsPlist ExportOptions.plist \
  -exportPath ./build/Release

# Generate ExportOptions.plist
cat > ExportOptions.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>method</key>
  <string>app-store</string>
  <key>signingStyle</key>
  <string>automatic</string>
  <key>stripSwiftSymbols</key>
  <true/>
  <key>teamID</key>
  <string>TEAM_ID</string>
</dict>
</plist>
EOF
```

### App Store Connect Upload

```bash
#!/bin/bash
# upload-ios.sh

APP_IDENTIFIER="com.example.app"
APP_PASSWORD=$(xcrun altool --list-apps -u "$APPLE_ID" -p "$APP_PASSWORD_KEYCHAIN" 2>&1 | grep -o 'password')

# Upload using altool (deprecated but still works)
xcrun altool --upload-app \
  -f ./build/Release/FeatureApp.ipa \
  -u "$APPLE_ID" \
  -p "$APP_PASSWORD"

# Or using Transporter (new method)
/Applications/Transporter.app/Contents/MacOS/Transporter \
  -m upload \
  -u "$APPLE_ID" \
  -p "$APP_PASSWORD" \
  -f ./build/Release/FeatureApp.ipa

# After upload, go to App Store Connect:
# 1. Review app info
# 2. Set pricing and availability
# 3. Submit for review
# 4. Wait for approval (24-48 hours typically)
# 5. Release to App Store
```

### App Store Metadata

```typescript
// App Store Connect JSON
{
  "app_name": "Feature Manager",
  "app_subtitle": "Manage features efficiently",
  "description": "A comprehensive feature management app for teams",
  "keywords": ["feature", "management", "productivity"],
  "support_url": "https://support.example.com",
  "privacy_policy_url": "https://example.com/privacy",
  "screenshots": [
    {
      "device_type": "iphone_6_1",
      "position": 1,
      "url": "screenshot1.png",
      "text": "Manage your features"
    }
  ],
  "rating": {
    "violent_content": 0,
    "frequent_mild_language": 0,
    "medical_treatment_info": 1,
    "alcohol_tobacco": 0,
    "gambling": 0,
    "sexual_content": 0,
    "graphic_violence": 0,
    "frequent_strong_language": 0
  }
}
```

---

## 🤖 Android Play Store Distribution

### Build for Release

```gradle
// build.gradle (app level)
android {
    compileSdk 34

    defaultConfig {
        applicationId "com.example.app"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0.0"
    }

    signingConfigs {
        release {
            storeFile file("release-key.jks")
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias System.getenv("KEY_ALIAS")
            keyPassword System.getenv("KEY_PASSWORD")
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}

dependencies {
    implementation 'androidx.compose.ui:ui:1.6.0'
    implementation 'androidx.lifecycle:lifecycle-viewmodel-compose:2.6.1'
    implementation 'androidx.hilt:hilt-navigation-compose:1.1.0'
    // ... more dependencies
}
```

### Generate Signed APK/AAB

```bash
#!/bin/bash
# build-android.sh

# Generate keystore
keytool -genkey -v -keystore release-key.jks \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -alias android-key

# Build signed APK
./gradlew assembleRelease \
  -Pandroid.injected.signing.store.file=release-key.jks \
  -Pandroid.injected.signing.store.password=$KEYSTORE_PASSWORD \
  -Pandroid.injected.signing.key.alias=android-key \
  -Pandroid.injected.signing.key.password=$KEY_PASSWORD

# Or build AAB for Play Store (recommended)
./gradlew bundleRelease \
  -Pandroid.injected.signing.store.file=release-key.jks \
  -Pandroid.injected.signing.store.password=$KEYSTORE_PASSWORD \
  -Pandroid.injected.signing.key.alias=android-key \
  -Pandroid.injected.signing.key.password=$KEY_PASSWORD

# Output will be:
# app/build/outputs/apk/release/app-release.apk
# app/build/outputs/bundle/release/app-release.aab
```

### Play Store Upload

```bash
#!/bin/bash
# upload-android.sh

# Setup Google Play Console API
# Download service account key JSON

# Use bundletool for AAB testing
bundletool build-apks \
  --bundle=app-release.aab \
  --output=app.apks \
  --ks=release-key.jks \
  --ks-pass=pass:$KEYSTORE_PASSWORD

# Upload using Google Play API
python3 upload-to-play-store.py \
  --aab=app-release.aab \
  --service-account=service-account-key.json \
  --package-name=com.example.app \
  --track=internal
```

### Google Play Store Metadata

```json
{
  "package_name": "com.example.app",
  "app_name": "Feature Manager",
  "short_description": "Manage features efficiently",
  "full_description": "A comprehensive feature management app for teams. Track, prioritize, and deploy features seamlessly.",
  "category": "PRODUCTIVITY",
  "contact_email": "support@example.com",
  "website": "https://example.com",
  "privacy_policy": "https://example.com/privacy",
  "screenshots": [
    "screenshot_1.png",
    "screenshot_2.png"
  ],
  "feature_graphic": "feature_graphic.png",
  "content_rating": {
    "violence": "VERY_MILD",
    "sexual_content": "NONE",
    "profanity": "NONE",
    "alcohol": "NONE",
    "drugs": "NONE",
    "gambling": "NONE",
    "other_concerns": "NONE"
  }
}
```

---

## 🖥️ Desktop Distribution

### Electron Auto-Update

```typescript
// Auto-update server
import { S3 } from 'aws-sdk';

const s3 = new S3();

app.get('/update/:os/:version', async (req, res) => {
  const { os, version } = req.params;

  try {
    const latestVersion = await getLatestVersion(os);

    if (latestVersion > version) {
      const updateUrl = await getUpdateUrl(os, latestVersion);

      return res.json({
        version: latestVersion,
        url: updateUrl,
        releaseDate: new Date(),
        releaseNotes: getChangeLog(latestVersion),
      });
    }

    res.status(204).send();
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// In Electron app
autoUpdater.setFeedURL({
  provider: 'generic',
  url: 'https://api.example.com/update/win32',
  channel: 'latest',
});

autoUpdater.checkForUpdates();

autoUpdater.on('update-available', () => {
  dialog.showMessageBox(mainWindow, {
    type: 'info',
    title: 'Update Available',
    message: 'A new version is available. Download now?',
    buttons: ['Yes', 'No'],
  });
});
```

### MSI Installer (Windows)

```xml
<!-- installer.wxs -->
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" Name="Feature Manager" Language="1033" Version="1.0.0.0">
    <Package InstallerVersion="200" Compressed="yes" />
    <Media Id="1" Cabinet="FeatureManager.cab" EmbedCab="yes" />

    <Feature Id="ProductFeature" Title="Feature Manager" Level="1">
      <ComponentRef Id="MainExecutable" />
    </Feature>

    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="FeatureManager" />
      </Directory>
    </Directory>

    <Component Id="MainExecutable" Directory="INSTALLFOLDER">
      <File Id="FeatureManagerExe" Source="dist/FeatureManager.exe" KeyPath="yes" />
    </Component>
  </Product>
</Wix>
```

### DMG Package (macOS)

```bash
#!/bin/bash
# create-dmg.sh

# Create DMG
hdiutil create -volname "Feature Manager" \
  -srcfolder dist/Feature\ Manager.app \
  -ov -format UDZO \
  dist/FeatureManager.dmg

# Sign DMG
codesign -s "Developer ID Application" dist/FeatureManager.dmg

# Notarize for macOS Catalina+
xcrun altool --notarize-file \
  -f dist/FeatureManager.dmg \
  -u "$APPLE_ID" \
  -p "$APP_PASSWORD"
```

---

## 🌐 Web Deployment

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: 18
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build
        run: npm run build
      
      - name: Run tests
        run: npm test
      
      - name: Deploy to Vercel
        uses: vercel/action@master
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
      
      - name: Deploy to AWS S3
        run: |
          aws s3 sync dist/ s3://${{ secrets.AWS_BUCKET }} --delete
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CLOUDFRONT_ID }} \
            --paths "/*"
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --production

COPY --from=builder /app/dist ./dist
COPY --from=builder /app/public ./public

EXPOSE 3000

CMD ["npm", "start"]
```

```bash
# Deploy to Docker registry
docker build -t myapp:1.0.0 .
docker tag myapp:1.0.0 registry.example.com/myapp:1.0.0
docker push registry.example.com/myapp:1.0.0

# Deploy to Kubernetes
kubectl set image deployment/myapp \
  myapp=registry.example.com/myapp:1.0.0 \
  --record
```

---

## 📊 Monitoring & Analytics

### Release Monitoring

```typescript
// Sentry for error tracking
import * as Sentry from "@sentry/react";

Sentry.init({
  dsn: "https://key@sentry.io/project",
  environment: process.env.NODE_ENV,
  tracesSampleRate: 0.1,
});

// Firebase Analytics
import { initializeApp } from 'firebase/app';
import { getAnalytics, logEvent } from "firebase/analytics";

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Track events
logEvent(analytics, 'feature_created', {
  featureName: 'OAuth',
  priority: 10
});

// Crash reporting (iOS)
import FirebaseCrashlytics

Crashlytics.crashlytics().recordError(NSError(domain: "example", code: 1))

// Crash reporting (Android)
import com.google.firebase.crashlytics.FirebaseCrashlytics

FirebaseCrashlytics.getInstance().recordException(exception)
```

---

## 📚 Related Documents

- Desktop Development (desktop_development.md)
- Mobile Development (mobile_development.md)
- Native iOS (native_ios.md)
- Native Android (native_android.md)
- Cross-Platform Strategies (cross_platform.md)

---

**END OF APP DISTRIBUTION DOCUMENT**
