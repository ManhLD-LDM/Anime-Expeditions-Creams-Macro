---
description: Code review rules, code smell elimination, cognitive complexity limits, and self-review quality gates
globs: ["**/*.{py,js,ts,jsx,tsx,go,java,cs,rs,php}"]
---

# Code Review & Quality Gate Rules

## 1. Cognitive Complexity & Code Smells
- **Function Length**: Keep functions under **50 lines** of focused code. Extract multi-step routines into private helper functions.
- **Nesting Depth**: Maximum **3 levels** of indentation. Use early returns (`guard clauses`) to flatten nested `if/else` blocks.
- **Dead Code**: Strictly remove commented-out code, unused imports, uncalled functions, and temporary debug statements before committing.
- **DRY vs. WET Balance**: Do not create premature abstractions for code duplicated only twice; abstract when a pattern repeats 3+ times with identical business invariants.

## 2. Pre-Commit Self-Review Checklist
Before requesting review or finalizing a PR:
- [ ] Have I run `git diff` to inspect every modified line?
- [ ] Have I removed all `console.log`, `print()`, or temporary debugging code?
- [ ] Have I verified all tests pass locally (`npm test` / `pytest`)?
- [ ] Have I verified that no secrets or API keys are present in the diff?
- [ ] Does every new public function have clear type definitions?
