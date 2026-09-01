---
name: cicd-workflow-engineering
description: Enterprise CI/CD pipeline design, GitHub Actions workflows, matrix testing, dependency caching, security scanning, and automated semantic releases.
---

# CI/CD Workflow & Pipeline Engineering Standards

This skill provides production templates and standards for automated Continuous Integration and Continuous Deployment (CI/CD) pipelines.

---

## 1. Production GitHub Actions Pipeline Structure

Every enterprise repository should implement a tiered pipeline:

```
┌─────────────────────────────────────────────────────────┐
│ Job 1: Linting & Code Quality (Fast fail < 1 min)       │
│ - ESLint / Ruff / golangci-lint / Prettier check        │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ Job 2: Test Matrix & Coverage (Parallel execution)      │
│ - Unit & Integration tests across multiple OS / Versions│
│ - Upload coverage report (Codecov / LCOV)               │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ Job 3: Security & Vulnerability Scan                     │
│ - Dependency audit (npm audit / pip-audit)              │
│ - Container scan (Trivy)                                │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ Job 4: Build & Semantic Release (On Tag/Main only)      │
│ - Multi-arch Docker build (amd64 / arm64)               │
│ - Push image to ECR/GHCR or create GitHub Release       │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Production GitHub Actions Workflow Template

Create `.github/workflows/ci.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
    tags: [ 'v*.*.*' ]
  pull_request:
    branches: [ main, develop ]

# Cancel in-progress runs on same PR branch when new commits are pushed
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    name: Lint & Format Check
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install Dependencies
        run: npm ci

      - name: Run Linter
        run: npm run lint

  test:
    name: Test Suite (Matrix)
    needs: lint
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ ubuntu-latest, windows-latest ]
        node-version: [ 18, 20, 22 ]

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install Dependencies
        run: npm ci

      - name: Run Unit & Integration Tests
        run: npm test -- --coverage

  security:
    name: Security Vulnerability Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Run Trivy Vulnerability Scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          ignore-unfixed: true
          severity: 'CRITICAL,HIGH'

  release:
    name: Publish Release & Docker Image
    needs: [ test, security ]
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      packages: write

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and Push Docker Image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.ref_name }},ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## 3. Best Practices for CI Performance

1. **Dependency Caching**: Always use `cache: 'npm'`, `cache: 'pip'`, or `actions/cache` to cut build times by 70%+.
2. **Branch Concurrency**: Always include `concurrency.cancel-in-progress: true` to prevent wasting CI compute on obsolete PR commits.
3. **Secret Isolation**: Never print or echo `secrets.*` in bash scripts or build args.
