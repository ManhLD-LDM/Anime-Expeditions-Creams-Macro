---
name: performance-profiling-and-optimization
description: Engineering workflow for diagnosing memory leaks, profiling CPU/memory bottlenecks, eliminating database N+1 queries, and optimizing frontend/backend latency.
---

# Performance Profiling & Memory Optimization Workflow

This skill defines the methodology for identifying memory leaks, profiling execution bottlenecks, and optimizing high-throughput systems.

---

## 1. Memory Leak Diagnostics & Prevention

### Common Memory Leak Antipatterns:
1. **Uncleaned Event Listeners / Subscriptions**:
   - *Problem*: Attaching `emitter.on('event', fn)` or `window.addEventListener` without corresponding `removeListener` / `removeEventListener` keeps the enclosing scope retained in memory forever.
   - *Solution*: Always return a cleanup/dispose function (e.g. in React `useEffect`, or class destructor/dispose pattern).

2. **Unbounded In-Memory Caches**:
   - *Problem*: Storing items in a plain `Map()` or `dict` without size limits or TTL causes gradual heap growth until Out-Of-Memory (OOM) crashes.
   - *Solution*: Use an explicit LRU (Least Recently Used) cache with hard size constraints (e.g. `lru-cache`, `functools.lru_cache(maxsize=1000)`) or `WeakMap` / `WeakSet` where keys can be garbage-collected.

3. **Closure Scope Capture**:
   - *Problem*: Retaining large objects in an outer scope referenced by long-lived inner callback functions.
   - *Solution*: Nullify large variables after processing (`largeBuffer = null`) or pass only primitive identifiers into callbacks.

4. **Streaming vs. Buffering**:
   - *Problem*: Reading an entire 500MB file or 100,000 database rows into a single memory buffer (`await file.read()` or `SELECT * FROM table`).
   - *Solution*: Process data using streams (`fs.createReadStream`, Python generators `yield`, database cursors `find().stream()`).

---

## 2. Database Query Profiling & N+1 Elimination

### The N+1 Problem:
```
// ❌ N+1 Antipatter: 1 query for users + 100 queries for orders
const users = await db.users.findMany(); // Query 1
for (const user of users) {
  user.orders = await db.orders.findMany({ where: { userId: user.id } }); // N Queries
}

// ✅ Eager Loading: 2 queries total
const users = await db.users.findMany({
  include: { orders: true }
});
```

### EXPLAIN ANALYZE Checklist:
- [ ] Are queries performing `Seq Scan` (Sequential Table Scans) on tables with > 1,000 rows? If yes, add targeted indexes.
- [ ] Is `Index Scan` or `Bitmap Index Scan` utilized for all filtering `WHERE` clauses?
- [ ] Are multi-column filters covered by composite indexes with correct column ordering?

---

## 3. Frontend & Network Performance Checklist

- **Bundle Size**: Split routes via dynamic imports (`React.lazy()` / `import()`).
- **DOM Virtualization**: Use virtualized lists (`react-window`, `tanstack-virtual`) for rendering lists with > 100 rows.
- **Image Optimization**: Serve modern formats (WebP, AVIF) with responsive `srcset` and explicit `aspect-ratio` to avoid Cumulative Layout Shift (CLS).
- **HTTP Compression**: Enable Gzip or Brotli compression on reverse proxies / CDNs.
