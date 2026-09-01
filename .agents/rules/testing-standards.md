---
description: Test structure, naming conventions, assertion hygiene, and mocking rules across all test files
globs: ["**/*.{test,spec}.{js,ts,jsx,tsx,py,go}", "**/tests/**", "**/test_*.py", "*_test.go"]
---

# Testing Standards & Assertion Hygiene

## 1. Naming Conventions
- **JavaScript / TypeScript**:
  - `describe('ComponentNameOrService', () => { it('should [expected behavior] when [condition/input]', () => { ... }) })`
- **Python (Pytest)**:
  - `test_[function_or_scenario]_[condition]_[expected_outcome]()` (e.g. `test_transfer_funds_insufficient_balance_raises_error()`)
- **Go**:
  - `Test[FunctionName]_[Scenario](t *testing.T)` (e.g. `TestCalculateTax_ZeroIncome`)

## 2. Assertion Hygiene & Readability
- **One Logical Concept per Test**: Focus each test on validating a single behavior or acceptance criterion.
- **Specific Error Assertions**: When testing exceptions, verify the exact error class or error code, not just that an error was thrown:
  ```python
  # ✅ Good
  with pytest.raises(InsufficientFundsError, match="Balance cannot be negative"):
      account.withdraw(500)
  
  # ❌ Bad
  with pytest.raises(Exception):
      account.withdraw(500)
  ```
- **Clear Failure Messages**: Provide diagnostic messages for custom assertions.

## 3. Mocking & Test Isolation
- **Mock Boundaries**: Only mock external systems (Network, Database, Clock/Time, Filesystem, 3rd-party SDKs). Never mock internal domain models or math calculations.
- **Fresh State**: Never share mutable state between tests. Reset all mocks in `beforeEach` / `setup_method`.
- **Avoid Over-Mocking**: If a test requires mocking 10 different internal functions, the unit under test is violating the Single Responsibility Principle and should be refactored.
- **Deterministic Time**: Inject or freeze time (using `freezegun`, `vi.useFakeTimers()`, or `timekeeper`) when testing expiration, tokens, or scheduled intervals.
