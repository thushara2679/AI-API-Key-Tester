# Third-Party Services Integration Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** Third-Party Services Integration Guide
**Focus:** 100+ integration techniques

---

## 📧 Email Services

### SendGrid Integration

```typescript
import sgMail from '@sendgrid/mail';

sgMail.setApiKey(process.env.SENDGRID_API_KEY);

async function sendNotificationEmail(
  to: string,
  featureName: string
): Promise<void> {
  const msg = {
    to,
    from: 'noreply@example.com',
    subject: `Feature ${featureName} created`,
    html: `<h1>New Feature: ${featureName}</h1>`,
    trackingSettings: {
      clickTracking: { enable: true },
      openTracking: { enable: true }
    }
  };

  await sgMail.send(msg);
}

// Batch emails
async function sendBatchEmails(recipients: string[], subject: string) {
  const emails = recipients.map(to => ({
    to,
    from: 'noreply@example.com',
    subject,
    html: '<h1>Notification</h1>',
    personalizations: [{
      to: [{ email: to }],
      substitutions: { '-name-': 'User' }
    }]
  }));

  await sgMail.sendMultiple({
    personalizations: emails.map(e => e.personalizations[0]),
    from: 'noreply@example.com',
    subject,
    html: '<h1>Notification</h1>'
  });
}

// Template emails
async function sendTemplateEmail(to: string, templateId: string, data: any) {
  await sgMail.send({
    to,
    from: 'noreply@example.com',
    templateId,
    dynamicTemplateData: data
  });
}
```

### Mailgun Integration

```typescript
import mailgun from 'mailgun.js';

const mg = mailgun.client({
  username: 'api',
  key: process.env.MAILGUN_API_KEY,
  url: 'https://api.mailgun.net'
});

async function sendEmail(to: string, subject: string, html: string) {
  return mg.messages.create('example.com', {
    from: 'noreply@example.com',
    to,
    subject,
    html,
    'o:tracking': true,
    'o:tracking-clicks': true,
    'o:tracking-opens': true
  });
}

// Scheduled email
async function scheduleEmail(
  to: string,
  subject: string,
  html: string,
  scheduledTime: Date
) {
  return mg.messages.create('example.com', {
    from: 'noreply@example.com',
    to,
    subject,
    html,
    'o:deliverytime': scheduledTime.toISOString()
  });
}
```

---

## 💬 SMS & Push Notifications

### Twilio SMS

```typescript
import twilio from 'twilio';

const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

async function sendSMS(to: string, message: string) {
  return client.messages.create({
    body: message,
    from: process.env.TWILIO_PHONE_NUMBER,
    to
  });
}

// Batch SMS
async function sendBatchSMS(
  recipients: string[],
  messageTemplate: string
) {
  return Promise.all(
    recipients.map(to =>
      sendSMS(to, messageTemplate)
    )
  );
}
```

### Firebase Push Notifications

```typescript
import admin from 'firebase-admin';

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://project.firebaseio.com'
});

async function sendPushNotification(
  deviceToken: string,
  title: string,
  body: string
) {
  const message = {
    notification: { title, body },
    android: {
      priority: 'high',
      notification: {
        sound: 'default'
      }
    },
    apns: {
      payload: {
        aps: {
          sound: 'default',
          alert: {
            title,
            body
          }
        }
      }
    },
    token: deviceToken
  };

  return admin.messaging().send(message);
}

// Topic-based
async function sendTopicNotification(
  topic: string,
  title: string,
  body: string
) {
  const message = {
    notification: { title, body },
    topic
  };

  return admin.messaging().send(message);
}

// Multicast
async function sendMulticastNotification(
  deviceTokens: string[],
  title: string,
  body: string
) {
  const message = {
    notification: { title, body },
    android: { priority: 'high' },
    apns: { payload: { aps: { sound: 'default' } } }
  };

  return admin.messaging().sendMulticast({
    tokens: deviceTokens,
    ...message
  });
}
```

---

## 🗂️ Cloud Storage

### AWS S3

```typescript
import AWS from 'aws-sdk';

const s3 = new AWS.S3({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
});

// Upload file
async function uploadFile(
  bucket: string,
  key: string,
  body: Buffer | string
) {
  return s3.putObject({
    Bucket: bucket,
    Key: key,
    Body: body,
    ServerSideEncryption: 'AES256',
    Metadata: {
      'uploaded-at': new Date().toISOString()
    }
  }).promise();
}

// Generate signed URL
function getSignedUrl(bucket: string, key: string, expiresIn: number = 3600) {
  return s3.getSignedUrl('getObject', {
    Bucket: bucket,
    Key: key,
    Expires: expiresIn
  });
}

// Multipart upload
async function uploadLargeFile(
  bucket: string,
  key: string,
  filePath: string
) {
  const fileSize = fs.statSync(filePath).size;
  const partSize = 5 * 1024 * 1024; // 5MB
  const parts: any[] = [];

  const multipartUpload = await s3.createMultipartUpload({
    Bucket: bucket,
    Key: key
  }).promise();

  for (let i = 0; i < Math.ceil(fileSize / partSize); i++) {
    const start = i * partSize;
    const end = Math.min(start + partSize, fileSize);
    const data = fs.readFileSync(filePath, { flag: 'r' }).slice(start, end);

    const result = await s3.uploadPart({
      Bucket: bucket,
      Key: key,
      PartNumber: i + 1,
      UploadId: multipartUpload.UploadId,
      Body: data
    }).promise();

    parts.push({
      ETag: result.ETag,
      PartNumber: i + 1
    });
  }

  return s3.completeMultipartUpload({
    Bucket: bucket,
    Key: key,
    UploadId: multipartUpload.UploadId,
    MultipartUpload: { Parts: parts }
  }).promise();
}
```

### Google Cloud Storage

```typescript
import { Storage } from '@google-cloud/storage';

const storage = new Storage({
  projectId: process.env.GCP_PROJECT_ID,
  keyFilename: process.env.GCP_KEY_FILE
});

const bucket = storage.bucket(process.env.GCP_BUCKET_NAME);

// Upload file
async function uploadToGCS(fileName: string, localPath: string) {
  await bucket.upload(localPath, { destination: fileName });
  return `gs://${process.env.GCP_BUCKET_NAME}/${fileName}`;
}

// Public download
async function makePublic(fileName: string) {
  await bucket.file(fileName).makePublic();
  return `https://storage.googleapis.com/${process.env.GCP_BUCKET_NAME}/${fileName}`;
}
```

---

## 🔐 Payment Processing

### Stripe Integration

```typescript
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

// Create payment intent
async function createPaymentIntent(
  amount: number,
  currency: string = 'usd',
  metadata: any = {}
) {
  return stripe.paymentIntents.create({
    amount: amount * 100, // Convert to cents
    currency,
    metadata
  });
}

// Handle webhook
app.post('/webhooks/stripe', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];

  try {
    const event = stripe.webhooks.constructEvent(
      req.body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET
    );

    switch (event.type) {
      case 'payment_intent.succeeded':
        handlePaymentSuccess(event.data.object);
        break;
      case 'payment_intent.payment_failed':
        handlePaymentFailed(event.data.object);
        break;
    }

    res.json({ received: true });
  } catch (error) {
    res.status(400).send(`Webhook error: ${error.message}`);
  }
});

// Create subscription
async function createSubscription(
  customerId: string,
  priceId: string
) {
  return stripe.subscriptions.create({
    customer: customerId,
    items: [{ price: priceId }],
    payment_behavior: 'default_incomplete',
    expand: ['latest_invoice.payment_intent']
  });
}
```

---

## 🗂️ Document Processing

### PDF Generation

```typescript
import PDFDocument from 'pdfkit';
import { createWriteStream } from 'fs';

async function generatePDF(
  fileName: string,
  content: { title: string; body: string }
) {
  const doc = new PDFDocument();
  const stream = createWriteStream(`./uploads/${fileName}`);

  doc.pipe(stream);

  doc.fontSize(25).text(content.title, 100, 100);
  doc.fontSize(12).text(content.body, 100, 150);

  doc.end();

  return new Promise((resolve, reject) => {
    stream.on('finish', resolve);
    stream.on('error', reject);
  });
}

// Using a library
import { renderToStream } from '@react-pdf/renderer';

const PdfDocument = () => (
  <Document>
    <Page>
      <Text>Hello World</Text>
    </Page>
  </Document>
);

async function generateReportPDF() {
  const stream = await renderToStream(<PdfDocument />);
  return stream;
}
```

### Excel Generation

```typescript
import ExcelJS from 'exceljs';

async function generateReport(data: any[], fileName: string) {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet('Report');

  // Headers
  worksheet.columns = [
    { header: 'ID', key: 'id', width: 10 },
    { header: 'Name', key: 'name', width: 30 },
    { header: 'Priority', key: 'priority', width: 10 }
  ];

  // Data
  data.forEach(item => {
    worksheet.addRow(item);
  });

  // Styling
  worksheet.getRow(1).font = { bold: true };
  worksheet.getRow(1).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFD3D3D3' } };

  // Save
  await workbook.xlsx.writeFile(fileName);
}
```

---

## 🔍 Analytics

### Google Analytics

```typescript
import { BetaAnalyticsDataClient } from '@google-analytics/data';

const analyticsDataClient = new BetaAnalyticsDataClient({
  projectId: process.env.GA_PROJECT_ID,
  keyFilename: process.env.GA_KEY_FILE
});

async function getPageViews(propertyId: string, startDate: string) {
  const response = await analyticsDataClient.runReport({
    property: `properties/${propertyId}`,
    dateRanges: [
      {
        startDate,
        endDate: new Date().toISOString().split('T')[0]
      }
    ],
    dimensions: [{ name: 'pagePath' }],
    metrics: [{ name: 'screenPageViews' }]
  });

  return response[0].rows;
}
```

### Mixpanel Events

```typescript
import Mixpanel from 'mixpanel';

const mixpanel = Mixpanel.init(process.env.MIXPANEL_TOKEN);

// Track event
mixpanel.track('Feature Created', {
  featureName: 'OAuth',
  userId: user.id,
  timestamp: new Date()
});

// User profile
mixpanel.people_set(user.id, {
  $first_name: user.firstName,
  $last_name: user.lastName,
  $email: user.email,
  plan: 'premium'
});

// Batch track
const batch = [
  { event: 'Feature Created', properties: { id: '1' } },
  { event: 'Feature Updated', properties: { id: '2' } }
];

batch.forEach(item => mixpanel.track(item.event, item.properties));
```

---

## 📚 Related Documents

- API Integration (api_integration.md)
- Real-time Communication (real_time_communication.md)
- Message Queues (message_queues.md)

---

**END OF THIRD-PARTY SERVICES INTEGRATION DOCUMENT**
