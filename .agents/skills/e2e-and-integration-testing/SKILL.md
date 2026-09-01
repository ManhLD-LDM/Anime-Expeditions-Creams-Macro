---
name: e2e-and-integration-testing
description: Guidelines and patterns for robust API integration testing, browser E2E automation with Playwright/Cypress, containerized test databases (Testcontainers), and eliminating test flakiness.
---

# E2E & API Integration Testing Standards

This skill guides the implementation of integration and end-to-end (E2E) tests that validate system interaction across databases, network boundaries, and user interfaces without flakiness.

---

## 1. API Integration Testing

API integration tests verify the complete HTTP request-response cycle, including routing, middleware (auth, rate limiting, validation), and database persistence.

### Best Practices:
1. **Real or Containerized Database**: Prefer ephemeral test databases (Docker / Testcontainers / SQLite in-memory) over mocking ORMs.
2. **Database Isolation**: Roll back transactions or truncate tables between test runs to ensure test independence.
3. **Assert Contracts & Status Codes**: Check HTTP status codes, headers, and exact response schema shape.

### TypeScript / Supertest Example:
```typescript
describe('POST /api/v1/auth/register', () => {
  it('should create a new user and return 201 with auth tokens', async () => {
    const payload = {
      email: 'test.user@example.com',
      password: 'SecurePassword123!',
      name: 'Test User'
    };

    const res = await request(app)
      .post('/api/v1/auth/register')
      .send(payload)
      .expect(201);

    expect(res.body).toMatchObject({
      success: true,
      data: {
        id: expect.any(String),
        email: payload.email,
        name: payload.name
      }
    });
    expect(res.headers['set-cookie']).toBeDefined();
  });
});
```

---

## 2. Browser E2E Testing (Playwright / Cypress)

### Accessibility & Role-Based Locators:
Avoid brittle CSS selectors (`.btn-primary > div > span`). Use accessible, user-facing locators:
```typescript
// ✅ Good: Resilient and accessible
await page.getByRole('button', { name: /submit order/i }).click();
await page.getByLabel('Email address').fill('user@example.com');
await page.getByTestId('order-confirmation-modal').waitFor();

// ❌ Bad: Fragile CSS structure
await page.locator('div.container > form > div:nth-child(3) > button').click();
```

---

## 3. Flakiness Elimination Rules

Flaky tests erode trust in CI/CD pipelines. Follow these strict anti-flakiness rules:

1. **NEVER use arbitrary sleep/delay**:
   - ❌ `await page.waitForTimeout(3000)` or `time.sleep(3)` is strictly forbidden.
   - ✅ Use deterministic event-driven wait: `await expect(page.getByText('Payment Succeeded')).toBeVisible()`.
2. **Wait for Network Idle / Specific Response**:
   - `await page.waitForResponse(resp => resp.url().includes('/api/v1/orders') && resp.status() === 200)`
3. **Mock Third-Party External APIs (MSW / WireMock)**:
   - Never call live external payment processors (Stripe/PayPal) or email providers (SendGrid) in automated CI tests. Use Mock Service Worker (MSW) to intercept and return deterministic payloads.

---

## 4. Visual Regression Testing

When testing critical UI components, snapshot screenshots against a baseline:
```typescript
test('homepage matches visual snapshot', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixelRatio: 0.02,
    animations: 'disabled'
  });
});
```
