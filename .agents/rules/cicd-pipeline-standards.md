---
description: Rules for GitHub Actions workflows, CI/CD pipeline optimization, caching, and release automation
globs: [".github/workflows/**", ".gitlab-ci.yml", "Jenkinsfile"]
---

# CI/CD Pipeline & GitHub Actions Standards

## 1. Safety & Permissions
- **Least Privilege Principle**: Set top-level workflow permissions to `permissions: read-all` by default, granting write permissions (`contents: write`, `packages: write`) only to the specific jobs (e.g. release job) that require them.
- **Pin Action Versions**: Use specific version tags (e.g. `uses: actions/checkout@v4`) or commit SHAs for third-party actions to protect against supply-chain tampering.

## 2. Speed & Efficiency
- **Cancel In-Progress Runs**: Always define `concurrency` with `cancel-in-progress: true` on PR branches.
- **Dependency & Build Caching**: Utilize native action caching (`cache: 'npm'`, `cache: 'pip'`) or `actions/cache`.
- **Fail Fast Strategy**: Run lightweight linters and static checks before kicking off heavy integration/E2E test matrices.

## 3. Deployment Discipline
- Staging deployments must trigger automatically on push to the primary branch (`main`).
- Production deployments must require manual approvals or be triggered strictly by verified Semantic Version tags (`v*.*.*`).
