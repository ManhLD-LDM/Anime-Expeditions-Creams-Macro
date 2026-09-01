---
name: git-workflow-and-release-management
description: Comprehensive workflow for Git branching, Conventional Commits specification, Semantic Versioning (SemVer 2.0), automated release tagging, and changelog generation.
---

# Git Workflow & Release Management Standards

This skill provides the authoritative standard for managing Git branches, formatting atomic Conventional Commits, executing semantic version releases, and automating changelogs.

---

## 1. Branching Strategies

### A. Trunk-Based Development (Recommended for Web & SaaS):
- Single long-lived branch: `main`.
- Short-lived feature branches (< 1-2 days) created from `main`:
  - `feat/feature-name` (e.g. `feat/oauth-google-login`)
  - `fix/bug-description` (e.g. `fix/cart-item-count`)
  - `docs/topic-name` (e.g. `docs/api-reference`)
  - `refactor/scope` (e.g. `refactor/auth-middleware`)
- Merged back into `main` via Pull Request with linear history (`Squash and merge` or `Rebase and merge`).

### B. Gitflow (For Packaged / Desktop / Embedded Releases):
- `main`: Production releases (tagged with `v*.*.*`).
- `develop`: Integration branch for next release.
- `release/vX.Y.Z`: Staging branch for final QA before merging to `main` and `develop`.
- `hotfix/vX.Y.Z`: Critical bug fixes branched directly from `main`.

---

## 2. Conventional Commits 1.0.0 Specification

Every commit message MUST adhere to the following schema:

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Commit Types:
| Type | Purpose | SemVer Bump |
| :--- | :--- | :--- |
| **`feat`** | A new feature or capability | **MINOR** (`0.X.0`) |
| **`fix`** | A bug fix in existing code | **PATCH** (`0.0.X`) |
| **`perf`** | Code change that improves performance | **PATCH** (`0.0.X`) |
| **`refactor`**| Code change that neither fixes a bug nor adds a feature | **PATCH** or None |
| **`test`** | Adding missing tests or correcting existing tests | None |
| **`docs`** | Documentation only changes | None |
| **`style`**| Code formatting, whitespace, semicolons (no code change) | None |
| **`build`** | Build system, toolchain, or external dependencies | None |
| **`ci`** | CI/CD configuration and workflow files | None |
| **`chore`** | Maintenance, updating dependencies, tool scripts | None |

### Breaking Changes:
- Append `!` after type/scope and include `BREAKING CHANGE:` in the footer:
```
feat(auth)!: replace legacy session cookie with bearer JWT tokens

BREAKING CHANGE: The /api/v1/auth/session endpoint has been removed. All clients must authenticate via the Authorization header.
```
*Triggers a **MAJOR** version bump (`X.0.0`).*

### Formatting Rules:
1. **Imperative Mood**: Use "add", "fix", "change", NOT "added", "fixes", "changing".
2. **Character Limit**: Keep the subject line <= **72 characters** (ideal <= 50).
3. **No Period**: Do not end the subject line with a period (`.`).
4. **Atomic Commits**: Group related changes into single, focused commits. Never combine unrelated features and bug fixes in one commit.

---

## 3. Semantic Versioning (SemVer 2.0) & Release Workflow

Version numbers follow `MAJOR.MINOR.PATCH` (`v1.4.2`):
- `MAJOR`: Incompatible API changes.
- `MINOR`: Backward-compatible new functionality.
- `PATCH`: Backward-compatible bug fixes.

### Step-by-Step Release Protocol:
1. **Verify Clean Working Tree**:
   ```bash
   git status --porcelain
   ```
2. **Run Full Quality Gate (Lint + Tests)**:
   ```bash
   npm test && npm run lint
   # or
   pytest tests/ && ruff check .
   ```
3. **Update Version in Project Manifest**:
   - Update `package.json`, `VERSION`, `pyproject.toml`, or `Cargo.toml`.
4. **Update `CHANGELOG.md`**:
   - Move unreleased items under the new version header `## [vX.Y.Z] - YYYY-MM-DD`.
5. **Create Annotated Git Tag**:
   ```bash
   git add .
   git commit -m "chore(release): vX.Y.Z"
   git tag -a vX.Y.Z -m "Release vX.Y.Z"
   git push origin main --tags
   ```
