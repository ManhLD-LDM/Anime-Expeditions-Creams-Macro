---
name: automated-code-review
description: Comprehensive framework for code reviews, code smell detection, security checks, cognitive complexity reduction, and Pull Request (PR) quality gates.
---

# Automated Code Review & Quality Gates Framework

This skill guides AI assistants and engineers through reviewing code diffs, identifying antipatterns, and generating structured Pull Request reviews.

---

## 1. The 5-Dimension Code Review Matrix

When reviewing a branch, PR, or code diff, systematically evaluate these 5 dimensions:

### 1. Correctness & Edge Cases
- Are null, undefined, or empty values handled gracefully?
- Are loop boundaries correct (no off-by-one errors)?
- Are async promises / goroutines / threads handled with proper error propagation?
- Are concurrent operations race-condition safe?

### 2. Security & OWASP Compliance
- Are user inputs strictly validated before processing?
- Are database queries parameterized (no SQL injection)?
- Are object-level permissions verified (BOLA / IDOR protection)?
- Are secrets or sensitive data leaked in logs or source code?

### 3. Performance & Resource Leaks
- Are file descriptors, database connections, and HTTP responses closed/disposed?
- Are frontend event listeners / timers removed upon component unmount?
- Are database queries optimized (no N+1 query loops, appropriate indexes)?
- Is memory allocated efficiently without unconstrained cache growth?

### 4. Clean Architecture & Maintainability
- Is business logic separated from presentation and transport layers?
- Does the code follow Single Responsibility Principle (SRP)?
- Is the code readable without unnecessary over-engineering or premature abstraction?
- Is cognitive complexity kept low (functions < 50 lines, nesting <= 3 levels)?

### 5. Testing & Quality Assurance
- Does the change include corresponding unit/integration tests?
- Do existing tests still pass with zero regressions?
- Are edge cases and failure modes explicitly covered?

---

## 2. Pull Request (PR) Template Standard

When generating PR descriptions, follow this standard structure:

```markdown
## Summary of Changes
- Briefly describe the problem solved or feature introduced.
- Highlight key architectural decisions or modified components.

## Type of Change
- [ ] 🐛 Bug fix (non-breaking change fixing an issue)
- [ ] ✨ New feature (non-breaking change adding functionality)
- [ ] 💥 Breaking change (fix or feature causing existing functionality to break)
- [ ] ♻️ Code refactoring (no functional change)
- [ ] 📝 Documentation update

## Verification & Testing Performed
- [x] Unit tests passed: `pytest tests/` (124 passed)
- [x] Linter passed: `ruff check .` (0 errors)
- [x] Manual verification steps executed: [Describe briefly]

## Checklist
- [x] My code follows the repository's coding style guidelines.
- [x] I have performed a self-review of my own code.
- [x] I have added tests that prove my fix is effective or feature works.
- [x] New and existing unit tests pass locally.
- [x] Documentation has been updated synchronously.
```
