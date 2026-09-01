---
name: automated-testing-workflow
description: End-to-end testing workflow for unit tests, integration tests, TDD cycles, test doubles (mocks/stubs/spies), boundary edge-case analysis, and code coverage across Python, TypeScript/JS, Go, and Java.
---

# Automated Testing & TDD Workflow

This skill defines the structured workflow for designing, writing, and executing automated tests to guarantee zero regressions, complete boundary coverage, and reliable software delivery.

---

## 1. The Testing Pyramid

Structure test suites according to the industry-standard pyramid:

```
        ▲
       / \         E2E Tests (10%)
      /   \        - Critical user journeys, browser automation (Playwright/Cypress)
     /─────\
    /       \      Integration Tests (20-30%)
   /         \     - API boundaries, database repositories (Testcontainers, Supertest, httpx)
  /───────────\
 /             \   Unit Tests (60-70%)
/               \  - Pure business logic, domain entities, utility functions, edge cases (pytest, Vitest, Jest)
─────────────────
```

---

## 2. Test-Driven Development (TDD) Cycle

When developing new features or fixing bugs, follow the **Red-Green-Refactor** loop:

```
┌─────────────────────────────────────────────────────────┐
│ 1. RED (Write Failing Test)                             │
│    - Define the expected behavior & acceptance criteria │
│    - Run the test to CONFIRM it fails as expected       │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ 2. GREEN (Make Test Pass)                               │
│    - Write the MINIMUM code necessary to satisfy test   │
│    - Run test suite to verify success                   │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ 3. REFACTOR (Clean Code)                                │
│    - Clean up code, remove duplication, optimize        │
│    - Ensure all tests STILL pass                        │
└─────────────────────────────────────────────────────────┘
```

---

## 3. The AAA Pattern (Arrange - Act - Assert)

Every test case must follow the AAA structure with explicit separation:

### TypeScript / Vitest / Jest Example:
```typescript
describe('CalculateDiscountUseCase', () => {
  it('should apply 20% discount when customer is VIP and cart exceeds $100', () => {
    // 1. Arrange
    const cart = new Cart({ totalAmount: 150, isVip: true });
    const service = new DiscountService();

    // 2. Act
    const finalAmount = service.calculate(cart);

    // 3. Assert
    expect(finalAmount).toBe(120);
  });
});
```

### Python / Pytest Example:
```python
def test_order_creation_deducts_inventory(mock_inventory_repo, order_service):
    # 1. Arrange
    product_id = "prod_123"
    quantity = 2
    mock_inventory_repo.get_stock.return_value = 10

    # 2. Act
    order = order_service.create_order(product_id=product_id, quantity=quantity)

    # 3. Assert
    assert order.status == "CONFIRMED"
    mock_inventory_repo.deduct_stock.assert_called_once_with(product_id, quantity)
```

---

## 4. Edge Cases & Boundary Analysis Checklist

For every function/endpoint under test, rigorously verify:
- [ ] **Zero / Empty**: `0`, `""`, `[]`, `{}`, `None` / `null` / `undefined`.
- [ ] **Single Element**: An array or string with exactly 1 item.
- [ ] **Boundary Limits**: `min - 1`, `min`, `max`, `max + 1` (e.g. pagination limits, password length).
- [ ] **Invalid Formats**: Malformed email, special characters, SQL/XSS strings, non-numeric strings where integers expected.
- [ ] **Concurrency & Race Conditions**: Simultaneous requests trying to claim the same seat/discount/inventory.
- [ ] **Failure Modes & Timeouts**: Simulated 3rd-party API failure (500, 503, 504), network disconnect, DB lock timeout.

---

## 5. Test Doubles (Mocks, Stubs, Spies, Fakes)

| Type | When to Use | Example |
| :--- | :--- | :--- |
| **Fake** | Working implementation unsuitable for prod | In-memory repository using a `Map()` / dictionary |
| **Stub** | Provides canned answers to calls | `mockRepo.findById.mockResolvedValue(user)` |
| **Mock** | Pre-programmed with expectations to verify calls | `expect(emailClient.send).toHaveBeenCalledWith(...)` |
| **Spy** | Wraps real object to record invocations | `vi.spyOn(logger, 'error')` |

### Rules for Mocking:
1. **Mock at the edges**: Mock external network calls, file system I/O, email services, payment gateways.
2. **Never mock internal pure logic**: Do not mock domain entities or math calculations.
3. **Always reset mocks**: Clear mock call history in `beforeEach` / teardown hooks to avoid cross-test contamination.
