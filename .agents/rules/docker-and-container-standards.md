---
description: Rules for writing secure, lightweight, production-grade Dockerfiles and container configurations
globs: ["**/Dockerfile*", "**/docker-compose*.{yml,yaml}", "**/.dockerignore"]
---

# Docker & Containerization Engineering Rules

## 1. Security First
- **Never Run as Root**: Always create and switch to a dedicated non-root user (`USER appuser` / `USER node`) in the runtime stage.
- **No Secrets in Images**: Never copy `.env` files or pass credentials via build `ARG` without Docker build secrets (`--mount=type=secret`).
- **Scan Vulnerabilities**: Keep base images updated to patched versions (e.g. `node:20-alpine`, `python:3.12-slim`).

## 2. Image Size & Layer Caching
- **Multi-Stage Builds**: Strictly mandatory for compiled or bundled applications. The runtime container must never contain compilers (gcc, g++, make), devDependencies, or build caches.
- **Copy Lockfiles First**: Copy `package.json` / `requirements.txt` / `go.mod` and install dependencies before copying the rest of the source code to maximize Docker build layer reuse.
- **Clean Package Manager Caches**: Always include `--no-cache` (apk) or `rm -rf /var/lib/apt/lists/*` in the same `RUN` step as package installation.

## 3. Container Observability & Health
- Every Dockerfile must declare an explicit `HEALTHCHECK` instruction.
- Support graceful shutdown: The application must handle `SIGTERM` and finish active tasks within 10-30s.
