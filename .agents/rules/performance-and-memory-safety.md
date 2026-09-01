---
description: Rules for memory leak prevention, stream processing, CPU optimization, and database query efficiency
globs: ["**/*.{py,js,ts,go,java,cs,rs,php,sql}"]
---

# Performance & Memory Safety Rules

## 1. Memory Leak Prevention
- **Cleanup Listeners**: Always pair event subscriptions, webhooks, and DOM listeners with explicit unmount/dispose cleanup logic.
- **Bound Caches**: In-memory caches must declare a maximum capacity (`maxSize`) and eviction policy (LRU / TTL). Never use unbounded objects or maps for caching.
- **Stream Heavy Data**: Stream files and large database query results chunk-by-chunk using streams/generators. Never buffer multi-megabyte payloads entirely in RAM.

## 2. Query & CPU Efficiency
- **No N+1 Queries**: Never execute database queries inside iteration loops. Use eager loading (`include` / `joinedload` / `DataLoader`) or batch queries.
- **Index All Filter Columns**: Any column queried in `WHERE`, `JOIN`, or `ORDER BY` on tables with > 1,000 records must have an index.
- **Async I/O**: Never perform synchronous blocking I/O on main event loops (e.g. `fs.readFileSync` in request handlers).
