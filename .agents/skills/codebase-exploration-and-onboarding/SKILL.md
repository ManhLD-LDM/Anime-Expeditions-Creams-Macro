---
name: codebase-exploration-and-onboarding
description: Systematic workflow for analyzing, mapping, exploring, and onboarding to unfamiliar codebases, architectures, and large repositories.
---

# Codebase Exploration & Onboarding Workflow

This skill guides AI assistants and developers through understanding, navigating, and building mental models of unfamiliar repositories without getting lost in large codebases.

---

## 1. The 4-Phase Discovery Workflow

```
┌─────────────────────────────────────────────────────────┐
│ Phase 1: Repository Inventory & Manifest Inspection     │
│ - Identify tech stack, framework versions, build tools  │
│ - Inspect package.json / pyproject.toml / go.mod / Cargo│
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ Phase 2: Entry Point & Lifecycle Mapping                │
│ - Locate main entry file (main.py, index.ts, main.go)   │
│ - Trace bootstrap lifecycle: config -> DB -> server/app │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ Phase 3: Core Domain & Data Flow Tracing                │
│ - Inspect Database Schemas, Entities, and DTOs          │
│ - Trace an end-to-end request from Router -> DB -> Client│
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│ Phase 4: Test Suite as Living Documentation             │
│ - Inspect unit & integration tests in tests/ / __tests__│
│ - Verify real-world edge cases & expected behaviors     │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Targeted Grep & Exploration Techniques

Instead of reading massive files blindly, follow these efficient investigation steps:

1. **Find Entry Points**:
   - Look for `main.py`, `app.py`, `src/index.ts`, `src/main.ts`, `cmd/server/main.go`, `App.tsx`.
2. **Trace Symbol Definitions & References**:
   - Search for function/class definitions: `class UserProfile`, `def execute_job`, `export interface Order`.
   - Search for call sites: find where an interface or helper is actually invoked.
3. **Inspect Configuration & Environment Variables**:
   - Look for `.env.example`, `config.py`, `src/config/`, `settings.json`.
4. **Identify External Boundaries**:
   - Check third-party API clients, database connection managers, message queue consumers.

---

## 3. Creating a "System Architecture Map"

When onboarding to a project, synthesize the architecture into this structured summary:

```markdown
### Project Anatomy Summary:
- **Primary Stack**: [e.g., Python 3.12 + PyWebView / FastAPI / React + TypeScript]
- **Architectural Style**: [e.g., Modular Monolith / Clean Architecture / Event-Driven]
- **Key Directories**:
  - `core/` or `src/domain/`: Core business logic and automation routines.
  - `ui/` or `src/interfaces/`: Frontend presentation and webview templates.
  - `tests/`: Automated unit and regression test suite.
- **Data Persistence**: [e.g., SQLite / PostgreSQL / Local JSON Store / Redis]
- **Core Execution Flow**: Entry point -> Config initialization -> Window/Service Docking -> Event Loop.
```
