# E2E Testing Document

## 📋 Document Overview

**Project Name:** Advanced AI Agent System for Enterprise Automation
**Version:** 1.0
**Document Type:** End-to-End Testing Guide
**Focus:** 50+ E2E testing techniques

---

## 🎯 E2E Testing Fundamentals

### Cypress Setup

```typescript
// cypress.config.ts
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 1280,
    viewportHeight: 720,
    setupNodeEvents(on, config) {
      on('task', {
        resetDatabase() {
          // Reset DB before tests
          return null;
        }
      });
    }
  }
});

// cypress/support/commands.ts
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.visit('/login');
  cy.get('[data-testid="email"]').type(email);
  cy.get('[data-testid="password"]').type(password);
  cy.get('[data-testid="login-button"]').click();
  cy.url().should('include', '/dashboard');
});

Cypress.Commands.add('createFeature', (name: string, priority: number) => {
  cy.get('[data-testid="create-btn"]').click();
  cy.get('[data-testid="feature-name"]').type(name);
  cy.get('[data-testid="feature-priority"]').select(priority);
  cy.get('[data-testid="submit"]').click();
  cy.contains(name).should('be.visible');
});
```

### Basic E2E Test

```typescript
// cypress/e2e/features.cy.ts
describe('Feature Management E2E', () => {
  beforeEach(() => {
    cy.login('user@example.com', 'password123');
  });

  it('should create feature through UI', () => {
    cy.visit('/features');
    cy.get('[data-testid="create-btn"]').click();
    
    cy.get('[data-testid="feature-name"]').type('OAuth');
    cy.get('[data-testid="feature-priority"]').select('10');
    cy.get('[data-testid="description"]').type('OAuth authentication');
    
    cy.get('[data-testid="submit"]').click();
    
    cy.contains('OAuth').should('be.visible');
    cy.url().should('include', '/features');
  });

  it('should edit feature', () => {
    cy.visit('/features');
    cy.contains('OAuth').parent().find('[data-testid="edit"]').click();
    
    cy.get('[data-testid="feature-priority"]').select('12');
    cy.get('[data-testid="submit"]').click();
    
    cy.contains('Priority: 12').should('be.visible');
  });

  it('should delete feature', () => {
    cy.visit('/features');
    cy.contains('OAuth').parent().find('[data-testid="delete"]').click();
    cy.get('[data-testid="confirm"]').click();
    
    cy.contains('OAuth').should('not.exist');
  });
});
```

---

## 🏃 Navigation & User Flows

### Multi-Page Workflows

```typescript
describe('Complete User Workflow', () => {
  it('should complete feature creation to deployment', () => {
    // Login
    cy.login('dev@example.com', 'pass123');
    
    // Create feature
    cy.visit('/features');
    cy.createFeature('OAuth', 10);
    
    // Navigate to detail
    cy.contains('OAuth').click();
    cy.url().should('include', '/features/');
    
    // Add tests
    cy.get('[data-testid="add-test"]').click();
    cy.get('[data-testid="test-name"]').type('OAuth Login Test');
    cy.get('[data-testid="save-test"]').click();
    
    // Create deployment
    cy.get('[data-testid="deploy-btn"]').click();
    cy.get('[data-testid="environment"]').select('staging');
    cy.get('[data-testid="confirm-deploy"]').click();
    
    // Verify deployment
    cy.contains('Deployment started').should('be.visible');
    cy.url().should('include', '/deployments');
  });
});
```

### Form Interactions

```typescript
describe('Form Interactions', () => {
  it('should validate form fields', () => {
    cy.visit('/features/create');
    
    // Try submitting empty form
    cy.get('[data-testid="submit"]').click();
    cy.contains('Name is required').should('be.visible');
    
    // Fill in name
    cy.get('[data-testid="feature-name"]').type('OAuth');
    cy.get('[data-testid="submit"]').click();
    cy.contains('Priority is required').should('be.visible');
    
    // Fill priority and submit
    cy.get('[data-testid="feature-priority"]').select('10');
    cy.get('[data-testid="submit"]').click();
    cy.contains('OAuth').should('be.visible');
  });

  it('should handle autocomplete', () => {
    cy.visit('/features/create');
    
    cy.get('[data-testid="tags"]').click();
    cy.get('[data-testid="tags"]').type('auth');
    
    cy.get('[data-testid="autocomplete-option"]')
      .contains('authentication')
      .click();
    
    cy.get('[data-testid="tags"]').should('have.value', 'authentication');
  });
});
```

---

## 🔄 Async & Real-time

### Waiting & Polling

```typescript
describe('Async Operations', () => {
  it('should wait for async updates', () => {
    cy.visit('/features');
    cy.get('[data-testid="create-btn"]').click();
    cy.get('[data-testid="feature-name"]').type('OAuth');
    cy.get('[data-testid="submit"]').click();
    
    // Wait for API response
    cy.contains('OAuth', { timeout: 10000 }).should('be.visible');
  });

  it('should handle real-time updates', () => {
    cy.visit('/features');
    
    // Simulate server sending update
    cy.intercept('GET', '/api/features', {
      fixture: 'features.json'
    });
    
    cy.window().then((win) => {
      // Simulate WebSocket message
      win.dispatchEvent(new Event('feature:updated'));
    });
    
    cy.contains('Updated Feature').should('be.visible');
  });

  it('should retry on timeout', () => {
    cy.visit('/deployments');
    
    cy.get('[data-testid="status"]', { timeout: 30000 })
      .should('contain', 'Completed');
  });
});
```

### Network Interception

```typescript
describe('Network Mocking', () => {
  it('should intercept API calls', () => {
    cy.intercept('GET', '/api/features', {
      statusCode: 200,
      body: [
        { id: '1', name: 'OAuth', priority: 10 }
      ]
    }).as('getFeatures');
    
    cy.visit('/features');
    cy.wait('@getFeatures');
    cy.contains('OAuth').should('be.visible');
  });

  it('should handle API errors', () => {
    cy.intercept('POST', '/api/features', {
      statusCode: 500,
      body: { error: 'Server error' }
    });
    
    cy.visit('/features/create');
    cy.get('[data-testid="feature-name"]').type('OAuth');
    cy.get('[data-testid="submit"]').click();
    
    cy.contains('Server error').should('be.visible');
  });

  it('should simulate network timeout', () => {
    cy.intercept('GET', '/api/features', (req) => {
      req.destroy();
    });
    
    cy.visit('/features');
    cy.contains('Network error').should('be.visible');
  });
});
```

---

## 📱 Responsive & Multi-Device

```typescript
describe('Responsive Design', () => {
  it('should work on mobile', () => {
    cy.viewport('iphone-x');
    cy.visit('/features');
    
    cy.get('[data-testid="menu-toggle"]').click();
    cy.get('[data-testid="menu"]').should('be.visible');
    
    cy.get('[data-testid="create-btn"]').should('be.visible');
  });

  it('should work on tablet', () => {
    cy.viewport('ipad-2');
    cy.visit('/features');
    
    cy.get('[data-testid="sidebar"]').should('have.css', 'display', 'block');
    cy.get('[data-testid="content"]').should('be.visible');
  });

  it('should work on desktop', () => {
    cy.viewport(1280, 720);
    cy.visit('/features');
    
    cy.get('[data-testid="sidebar"]').should('be.visible');
    cy.get('[data-testid="content"]').should('have.css', 'width');
  });
});
```

---

## 🎬 Visual & Accessibility

### Visual Testing

```typescript
describe('Visual Testing', () => {
  it('should match screenshot', () => {
    cy.login('user@example.com', 'pass123');
    cy.visit('/features');
    
    // Full page screenshot
    cy.screenshot('features-page');
    
    // Element screenshot
    cy.get('[data-testid="feature-list"]')
      .screenshot('feature-list');
  });

  it('should detect visual regressions', () => {
    cy.visit('/dashboard');
    cy.percySnapshot('dashboard');
  });
});
```

### Accessibility Testing

```typescript
describe('Accessibility', () => {
  it('should have proper labels', () => {
    cy.visit('/features/create');
    
    cy.get('input[name="name"]').should('have.attr', 'aria-label');
    cy.get('select[name="priority"]').should('have.attr', 'aria-label');
  });

  it('should be keyboard navigable', () => {
    cy.visit('/features');
    
    cy.get('body').tab();
    cy.focused().should('have.attr', 'data-testid', 'create-btn');
    
    cy.focused().tab();
    cy.focused().should('have.attr', 'data-testid', 'search-input');
  });

  it('should have sufficient color contrast', () => {
    cy.visit('/features');
    
    cy.checkA11y('[data-testid="feature-list"]', {
      rules: {
        'color-contrast': { enabled: true }
      }
    });
  });
});
```

---

## 🔧 Advanced Scenarios

### Data Setup & Cleanup

```typescript
describe('With Data Fixtures', () => {
  beforeEach(() => {
    // Create test data
    cy.request('POST', '/api/features', {
      name: 'Test Feature',
      priority: 5
    });
  });

  afterEach(() => {
    // Cleanup
    cy.request('DELETE', '/api/features/all');
  });

  it('should list created features', () => {
    cy.login('user@example.com', 'pass123');
    cy.visit('/features');
    cy.contains('Test Feature').should('be.visible');
  });
});
```

### Database Reset

```typescript
describe('With Database Reset', () => {
  beforeEach(() => {
    cy.task('resetDatabase').then(() => {
      cy.request('POST', '/api/seed', { count: 5 });
    });
  });

  it('should have clean state', () => {
    cy.visit('/features');
    cy.get('[data-testid="feature-item"]').should('have.length', 5);
  });
});
```

---

## 📚 Related Documents

- Testing Strategies (testing_strategies.md)
- Unit Testing (unit_testing.md)
- Integration Testing (integration_testing.md)
- Performance Testing (performance_testing.md)

---

**END OF E2E TESTING DOCUMENT**
