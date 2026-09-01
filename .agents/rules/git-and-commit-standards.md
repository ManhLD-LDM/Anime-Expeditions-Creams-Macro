---
description: Git hygiene, Conventional Commits formatting, atomic commit rules, post-task commit message output, and branch naming conventions
globs: ["**/*"]
---

# Git Hygiene & Conventional Commit Standards

## 1. Commit Message Conventions
- Always follow the **Conventional Commits 1.0.0** format:
  `feat(scope): add user profile avatar upload`
  `fix(payment): handle Stripe card declined error gracefully`
  `refactor(auth): simplify JWT verification middleware`
  `test(order): add edge case tests for zero-quantity items`
  `docs(readme): add docker-compose local setup guide`
- Subject line must start with lowercase, use imperative mood ("add", "fix", not "added", "fixing"), and contain **NO trailing period**.
- Subject line length must not exceed **72 characters**.

## 2. Mandatory Post-Task Commit Output (Critical)
- **At the end of EVERY response where code or files were modified**, the assistant MUST provide a ready-to-copy Git Commit Summary and Description formatted as follows:
  ```markdown
  ### 📦 Git Commit Message:
  - **Summary**: `type(scope): concise subject <= 72 chars`
  - **Description**:
    - Bullet 1 describing what was changed
    - Bullet 2 describing why or what effect it has
  ```

## 3. Atomic Commits & Clean History
- Every commit must represent **one cohesive logical change**. Do not mix refactoring with feature development or bug fixes in a single commit.
- Never commit broken code that fails unit tests or linters.
- Avoid committing temporary files, editor configs (`.vscode`, `.idea`), `.env`, build artifacts (`dist/`, `build/`), or OS files (`.DS_Store`, `Thumbs.db`).

## 4. Branch Naming Conventions
- Format: `<type>/<short-kebab-description>`
  - `feat/user-onboarding-modal`
  - `fix/memory-leak-websocket`
  - `refactor/clean-architecture-controllers`
  - `chore/upgrade-dependencies`
