---
description: Test-Driven Development (TDD), regression prevention, and test coverage mandates
globs: ["**/*.{py,js,ts,jsx,tsx,go,java,cs}"]
---

# TDD & Regression Prevention Mandates

## 1. Test-Driven Development (TDD) Discipline
- **Bug Fix Workflow**:
  1. Write a failing test that reproduces the reported bug / edge case (**RED**).
  2. Implement the fix (**GREEN**).
  3. Verify that the bug is resolved and all existing tests continue to pass (**REFACTOR**).
- **New Feature Workflow**:
  1. Define user stories as test scenarios before writing business logic.
  2. Implement the smallest code change needed to pass.
  3. Refactor with full safety.

## 2. Coverage Targets & Priorities
- **Domain & Business Logic Layer**: Minimum **85%+** branch and line coverage.
- **Financial, Cryptographic, & Security Functions**: **100%** branch coverage required.
- **Controllers & API Routers**: Focus on integration coverage (status codes, headers, DTO validation).

## 3. Pre-Commit / Pre-PR Verification
Before marking a coding task complete:
1. Run the entire test suite locally (e.g. `pytest`, `npm test`, `go test ./...`).
2. Verify zero regressions or broken tests.
3. Remove temporary debug statements, `console.log`, or `print()` statements.
