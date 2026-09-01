# AI Assistant Master Constitution & Engineering Standards (Antigravity)

This document defines the strict, non-negotiable engineering mandates for Frontend (UI/UX), Backend (API & Architecture), Testing (TDD & QA), Documentation, DevOps (CI/CD & Containerization), Git Workflow, Performance/DevSecOps, and AI Engineering across the workspace.

---

## 1. Frontend & UI/UX Engineering Mandates

1. **Never Output Generic / MVP-Looking Designs**:
   - Avoid generic AI color defaults (e.g. plain neon blue/purple gradients, gray-on-gray low contrast).
   - Always use cohesive color tokens, high-quality typography (Inter, Outfit, Plus Jakarta Sans, DM Sans), and clean visual depth (subtle shadows, borders, glassmorphism).

2. **Follow Strict UX & Design Principles**:
   - **Accessibility (WCAG 2.1 AA)**: 4.5:1 text contrast minimum, 44x44px minimum touch targets, visible focus states, full keyboard navigation.
   - **Icons**: NEVER use emojis as icons. Always use SVG icons (Lucide, Heroicons, Phosphor, FontAwesome).
   - **Micro-Interactions**: All clickable elements must have hover, active, and focus states with smooth transitions (`150ms-300ms ease-out`).
   - **State Completeness**: Every component/page MUST handle 5 core states: **Loading**, **Empty**, **Error**, **Success**, and **Active**.

3. **Responsive & Mobile-First**:
   - Implement fluid layouts with CSS Grid and Flexbox.
   - Never cause horizontal scrollbars on mobile viewport (`overflow-x: hidden` / container constraints).
   - Use standard breakpoints: Mobile (<640px), Tablet (640-1023px), Desktop (1024px+).

---

## 2. Backend, API & System Architecture Mandates

1. **Clean & Hexagonal Architecture (Layer Separation)**:
   - Separate code into: `interfaces/controllers` → `application/use-cases` → `domain/entities` → `infrastructure/repositories`.
   - Domain layer must remain pure (no direct DB, ORM, or HTTP imports).
   - Never call database queries directly from HTTP controllers.

2. **API Design & Standard Envelopes (REST & GraphQL)**:
   - Use plural kebab-case nouns for REST resources (`/api/v1/user-profiles`).
   - Always return standardized response envelopes with `success`, `data`/`error`, and `meta` (timestamps, request IDs).
   - Enforce strict input validation (Zod, Pydantic) on every incoming payload before business logic execution.

3. **Security & OWASP Top 10 API Protections**:
   - **No Raw SQL Concatenation**: Always use parameterized queries.
   - **Prevent BOLA / IDOR**: Verify user and tenant ownership for every resource mutation/query.
   - **Zero Secrets in Code**: Load configurations through strictly validated environment variables.
   - **Passwords & Keys**: Hash user credentials using `argon2id` or `bcrypt` (cost >= 12).

4. **Database Modeling & Caching**:
   - Time-sortable IDs (UUIDv7/ULID) or auto-incrementing BigInt; UTC timestamps on all tables.
   - Index all foreign keys and frequently filtered columns.
   - Implement Cache-Aside with explicit TTLs on Redis; invalidate cache synchronously upon entity mutation.

---

## 3. Testing, TDD & Quality Assurance Mandates

1. **Test-Driven Development (TDD) & Regression Prevention**:
   - Always follow the **Red-Green-Refactor** cycle.
   - When fixing a bug, write a reproducing test first (**RED**), fix the root cause (**GREEN**), and ensure zero regressions.
   - Never skip tests or mark failing tests as ignored without explicit reason.

2. **Test Structure & AAA Pattern**:
   - Every test MUST cleanly separate **Arrange**, **Act**, and **Assert**.
   - Use explicit, descriptive test names (`should [behavior] when [condition]`).

3. **Isolation & Flakiness Elimination**:
   - NEVER use arbitrary time delays (`sleep()`, `waitForTimeout(3000)`). Use deterministic event/locator waiters.
   - Mock external boundaries (Network, Filesystem, Clock, 3rd-party APIs); NEVER mock pure internal business logic.
   - Reset and isolate state between test cases (`beforeEach` / teardown hooks).

---

## 4. Documentation & Codebase Exploration Mandates

1. **Grounded Codebase Analysis**:
   - Trace symbol definitions, references, and manifests (`package.json`, `pyproject.toml`) before assuming behavior.
   - Consult test suites in `tests/` as living documentation of edge cases and business requirements.

2. **Standardized Technical Documentation**:
   - Document architecture decisions via ADRs (Nygard format).
   - Use GitHub alerts (`> [!NOTE]`, `> [!IMPORTANT]`, `> [!WARNING]`) and Mermaid diagrams for complex execution topologies.
   - Keep documentation synchronously updated with code changes to eliminate documentation drift.

---

## 5. DevOps, CI/CD & Containerization Mandates

1. **Container Security & Multi-Stage Builds**:
   - Always use Multi-Stage builds to keep production runtime images minimal.
   - Never run containers as `root` (enforce `USER appuser` / `USER node`).
   - Include explicit `HEALTHCHECK` instructions in all Dockerfiles.

2. **CI/CD Pipeline Optimization**:
   - Implement fast-fail tiering: Lint -> Test Matrix -> Security Scan -> Build/Release.
   - Utilize dependency caching (`actions/cache`) and branch concurrency cancellation (`cancel-in-progress: true`).
   - Restrict action permissions to least-privilege (`permissions: read-all`).

---

## 6. Git Workflow, Code Review & Release Mandates

1. **Conventional Commits 1.0.0**:
   - Strictly format all commit messages: `<type>(<scope>): <subject>` (`feat`, `fix`, `refactor`, `docs`, `perf`, `test`, `chore`).
   - Imperative mood, <= 72 characters, no trailing period. Atomic single-purpose commits.

2. **Code Review & Quality Gates**:
   - Limit cognitive complexity: Functions <= 50 lines, max 3 levels of nesting (use early guard clauses).
   - Zero dead code, unused imports, or loose debugging logs in committed code.
   - Self-review diffs before finalizing tasks.

3. **Semantic Versioning & Releases**:
   - Follow SemVer 2.0 (`vMAJOR.MINOR.PATCH`).
   - Create annotated tags (`git tag -a vX.Y.Z -m "Release vX.Y.Z"`) and keep `CHANGELOG.md` updated synchronously.

4. **Mandatory Post-Task Commit Output**:
   - After EVERY task that modifies code or project files, provide a concise, ready-to-copy Git Commit **Summary** and **Description** formatted in Conventional Commits style.

---

## 7. Performance, Memory Management & DevSecOps Mandates

1. **Memory Leak Elimination**:
   - Always clean up event listeners, timers, and streams on unmount/dispose.
   - Bound all in-memory caches with explicit TTLs and maximum capacity limits (LRU).
   - Stream large files and database query cursors; never buffer unbounded multi-megabyte payloads in RAM.

2. **Query Optimization & Profiling**:
   - Zero N+1 queries; use eager loading and batch queries (`DataLoader`).
   - Index all filter and foreign key columns.

3. **DevSecOps & Software Supply Chain**:
   - Zero secrets committed to version control.
   - Audit dependencies continuously for High/Critical CVEs (`npm audit`, `pip-audit`, Trivy).

---

## 8. AI Engineering, LLM Application & Agent Design Mandates

1. **Agent Architecture & ReAct Loops**:
   - Structure autonomous agents around Thought -> Action (Tool) -> Observation -> Reflection.
   - Cap tool retry loops at <= 3 attempts on error to prevent compute exhaustion.
   - Require Human-in-the-Loop (HITL) approval before executing irreversible mutations.

2. **Advanced RAG & Grounding**:
   - Implement Hybrid Search (BM25 + Dense Vector embeddings) with Cross-Encoder Reranking.
   - Prevent hallucinations by forcing strict context attribution; return explicit fallback if context lacks answer.

3. **Prompt Engineering & Evals**:
   - Structure system prompts with XML tags (`<role>`, `<operational_constraints>`, `<context>`, `<instructions>`).
   - Benchmark prompts against automated evaluation metrics (Faithfulness, Relevance, Precision via Ragas/DeepEval).

---

## 9. Available Skills in Workspace

- **Frontend & UI/UX**:
  - `ui-ux-pro-max`: Design intelligence, 79 styles, 192 palettes, 74 font pairings, 119 UX guidelines.
  - `frontend-ui-engineering`: Design tokens, 5-state UI workflow, responsive layouts.
- **Backend & System Design**:
  - `backend-system-design`: Clean architecture, database modeling, Redis caching, async task queues.
  - `api-engineering-rest-graphql`: Standardized REST/GraphQL API design, validation contracts, auth patterns.
- **Testing & QA**:
  - `automated-testing-workflow`: TDD cycles, test doubles (mocks/stubs/spies), boundary edge cases.
  - `e2e-and-integration-testing`: API integration testing, Playwright/Cypress browser E2E, anti-flakiness.
- **Codebase & Documentation**:
  - `codebase-exploration-and-onboarding`: 4-phase codebase discovery, topological mapping, call graphs.
  - `technical-documentation-writer`: Production READMEs, ADRs, Mermaid diagrams, API references.
- **DevOps & CI/CD**:
  - `devops-and-containerization`: Multi-stage Dockerfiles, non-root security, Docker Compose topologies.
  - `cicd-workflow-engineering`: Tiered GitHub Actions, matrix testing, dependency caching, semantic release.
- **Git & Release Management**:
  - `git-workflow-and-release-management`: Trunk-based/Gitflow strategies, Conventional Commits, SemVer 2.0.
  - `automated-code-review`: 5-dimension review matrix, code smell detection, PR templates.
- **Performance & DevSecOps**:
  - `performance-profiling-and-optimization`: Memory leak diagnosis, N+1 query elimination, CPU/RAM profiling.
  - `devsecops-and-security-hardening`: Dependency auditing, secret leak prevention, defense-in-depth.
- **AI Engineering & Autonomous Agents**:
  - `ai-agent-and-system-design`: ReAct loops, multi-agent manager-worker topologies, tool calling safety, HITL.
  - `rag-and-vector-search-engineering`: Hybrid search (BM25 + Vector RRF), semantic chunking, cross-encoder reranking.
  - `prompt-engineering-and-evals`: XML prompt structuring, few-shot exemplars, Ragas eval metrics.
