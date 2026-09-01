---
description: Database design, schema migrations, indexing, transactions, and performance rules
globs: ["**/*.{sql,py,js,ts,go,java,cs,prisma,json}"]
---

# Database Modeling, Indexing & Migration Rules

## 1. Schema Conventions
- Table names: `snake_case` plural (e.g. `users`, `order_items`, `payment_transactions`).
- Column names: `snake_case` (e.g. `user_id`, `created_at`, `total_amount_cents`).
- Currencies / Monetary amounts: Store in smallest currency unit as integer (e.g. cents/cents as `BIGINT`) or use `NUMERIC(15, 2)` / `DECIMAL`. Never use `FLOAT` for money.
- Time fields: Always store timestamps in UTC with timezone (`TIMESTAMPTZ` in Postgres, `TIMESTAMP WITH TIME ZONE`).

## 2. Indexing Best Practices
- **Foreign Keys**: Every foreign key column MUST have an index.
- **Index Selectivity**: Place high-cardinality columns first in composite indexes `(status, created_at)`.
- **Query Alignment**: Index columns used in `WHERE`, `JOIN`, and `ORDER BY` clauses together where appropriate.
- **Do Not Over-Index**: Every index adds overhead to `INSERT`, `UPDATE`, and `DELETE` operations. Monitor unused indexes.

## 3. Migration Safety (Zero-Downtime)
- **Non-Destructive Changes**:
  - Step 1: Add new nullable columns or default values.
  - Step 2: Deploy backend code that writes to both old and new columns.
  - Step 3: Backfill historical data in background batches.
  - Step 4: Deploy backend code that reads exclusively from new column.
  - Step 5: Remove old column in a subsequent migration.
- **Locking Prevention**: In Postgres, avoid `ALTER TABLE ... ADD COLUMN ... DEFAULT (non-constant)` on large tables without `CONCURRENTLY` or version-aware safety checks.
