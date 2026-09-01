---
name: devops-and-containerization
description: Engineering workflow for Docker, multi-stage container builds, Docker Compose local topology, container security hardening, and resource optimization.
---

# DevOps, Docker & Containerization Workflow

This skill guides the design, configuration, and optimization of production-grade Docker containers and local development orchestration.

---

## 1. Multi-Stage Dockerfile Architecture

Always use **Multi-Stage Builds** to separate the compilation/build environment from the lightweight runtime image.

### Production Node.js / TypeScript Example:
```dockerfile
# -------------------------------------------------------------
# Stage 1: Build & Compilation
# -------------------------------------------------------------
FROM node:20-alpine AS builder
WORKDIR /app

# Leverage Docker cache by copying lockfiles first
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build
RUN npm prune --production

# -------------------------------------------------------------
# Stage 2: Minimal Production Runtime
# -------------------------------------------------------------
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Security: Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser

# Copy built assets & production dependencies only
COPY --from=builder --chown=appuser:nodejs /app/dist ./dist
COPY --from=builder --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:nodejs /app/package.json ./package.json

USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

CMD ["node", "dist/main.js"]
```

### Production Python (FastAPI / Flask) Example:
```dockerfile
# -------------------------------------------------------------
# Stage 1: Builder
# -------------------------------------------------------------
FROM python:3.12-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# -------------------------------------------------------------
# Stage 2: Runtime
# -------------------------------------------------------------
FROM python:3.12-slim AS runner
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/appuser/.local/bin:$PATH"

RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m appuser

COPY --from=builder --chown=appuser:appgroup /root/.local /home/appuser/.local
COPY --chown=appuser:appgroup . .

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 2. Docker Compose Topology for Local Development

Define a deterministic, reproducible local environment with `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      target: runner
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/app_dev
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgrespassword
      POSTGRES_DB: app_dev
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - app-network

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

---

## 3. Mandatory `.dockerignore`

Always keep build contexts minimal and prevent credential leakage:
```
.git
.gitignore
.agents/
.env*
*.log
node_modules
__pycache__
.venv
dist
build
coverage
.DS_Store
```
