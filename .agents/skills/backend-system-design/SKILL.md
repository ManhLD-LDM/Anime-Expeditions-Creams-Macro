---
name: backend-system-design
description: Architecture and engineering workflow for robust backend systems, Clean/Hexagonal architecture, database modeling, caching, asynchronous workers, and high-scalability design.
---

# Backend System & Architecture Design Workflow

This skill guides the architectural design, database modeling, caching strategy, and structural organization of backend applications across Node.js/TypeScript, Python, Go, Java, and C#.

---

## 1. Architectural Patterns & Layering

Always adhere to **Clean Architecture / Hexagonal Architecture (Ports & Adapters)**:

```
┌────────────────────────────────────────────────────────┐
│                   Presentation Layer                   │
│         (REST Controllers, GraphQL Resolvers, gRPC)     │
└───────────────────────────┬────────────────────────────┘
                            │ (Calls via DTOs)
┌───────────────────────────▼────────────────────────────┐
│                    Application Layer                   │
│             (Use Cases, Business Services)             │
└───────────────────────────┬────────────────────────────┘
                            │ (Implements domain logic)
┌───────────────────────────▼────────────────────────────┐
│                      Domain Layer                      │
│        (Entities, Value Objects, Domain Events)        │
│          *NO external framework or DB imports*         │
└───────────────────────────▲────────────────────────────┘
                            │ (Implements interfaces)
┌───────────────────────────┴────────────────────────────┐
│                  Infrastructure Layer                  │
│       (Repositories, ORMs, Redis, Message Queues)      │
└────────────────────────────────────────────────────────┘
```

### Key Architectural Rules:
1. **Dependency Rule**: Dependencies always point **inwards** toward the Domain layer.
2. **Domain Purity**: Domain entities must never import database drivers, ORM decorators, HTTP frameworks, or external APIs.
3. **Repository Pattern**: Define repository interfaces in the Domain/Application layer; implement them in the Infrastructure layer.
4. **Service Boundaries**: Keep services single-responsibility; orchestrate multi-step workflows using Domain Services or Saga orchestrators.

---

## 2. Database Schema & Data Modeling

### Relational Schema (PostgreSQL, MySQL):
- **Primary Keys**: Prefer time-sortable **UUIDv7** or **ULID** for distributed systems; use auto-incrementing `BIGINT` for simple internal datasets.
- **Indexes**:
  - Always index foreign keys and columns frequently queried with equality/filtering (`WHERE user_id = ?`).
  - Use composite indexes `(tenant_id, status, created_at DESC)` matching query ordering.
  - Add partial indexes for filtered queries (`WHERE is_deleted = false`).
- **Timestamps**: Every table must include `created_at TIMESTAMPTZ DEFAULT NOW()` and `updated_at TIMESTAMPTZ DEFAULT NOW()`.
- **Soft Deletion**: Use `deleted_at TIMESTAMPTZ NULL` or an explicit archive table for auditable records.
- **Transactions (`ACID`)**: Wrap multi-entity writes in database transactions with proper rollback handling.

### NoSQL & Document Modeling (MongoDB, DynamoDB):
- Model data by **access patterns** rather than relational normalization.
- Embed sub-documents when child entities are bounded (< 100 items) and always read together.
- Reference IDs when collections grow unboundedly or require independent querying.

---

## 3. Caching Strategy (Redis / Memory)

### Cache-Aside Pattern (Standard):
```
Client -> Service -> Cache Miss -> DB Query -> Set Cache (with TTL) -> Return Data
```

### Rules for Caching:
1. **Always Set a TTL (Time-To-Live)**: Never write persistent keys to cache without an expiration window (e.g. 5m, 1h, 24h).
2. **Deterministic Cache Keys**: Format: `<environment>:<service>:<entity>:<id/filter>` (e.g. `prod:users:profile:usr_123`).
3. **Cache Invalidation**: Invalidate or update cached keys immediately on entity mutation (`POST`, `PUT`, `DELETE`).
4. **Cache Stampede Prevention**: Use distributed locks (e.g., Redis Redlock) or probabilistic early expiration for hot keys.

---

## 4. Asynchronous Processing & Task Queues

- **Background Jobs**: Offload long-running operations (> 200ms) like email sending, report generation, image resizing, and webhook delivery to background workers (BullMQ, Celery, Temporal, RabbitMQ).
- **Idempotency**: All queue workers and webhook handlers must be **idempotent** (safe to execute multiple times with the same input using an `Idempotency-Key` or transaction token).
- **Dead Letter Queues (DLQ)**: Configure exponential backoff retry with a dedicated DLQ for failed messages after N attempts.

---

## 5. System Design Verification Checklist

Before deploying or approving backend architecture, verify:
- [ ] Layer boundaries are strictly respected (no DB calls directly in controllers).
- [ ] Sensitive fields (passwords, tokens, PII) are hashed (`argon2id` / `bcrypt`) or encrypted at rest.
- [ ] Database connections use pooling with bounded limits (`min`, `max`, `idle_timeout`).
- [ ] Heavy queries have `EXPLAIN ANALYZE` verified with appropriate indexes.
- [ ] Endpoints support graceful shutdown (`SIGTERM` / `SIGINT`) draining active requests.
