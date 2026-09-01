---
description: Clean Architecture, Hexagonal patterns, Layered Separation, and Dependency Inversion rules for backend systems
globs: ["**/*.{py,js,ts,go,java,cs,rs,php}"]
---

# Backend Clean Architecture & Code Organization Rules

## 1. Directory & Layer Organization
Structure the backend into clearly demarcated layers:
- `src/domain/`: Pure business models, entities, value objects, domain errors, and repository interfaces.
- `src/application/`: Use cases, DTO definitions, application services, and business workflows.
- `src/infrastructure/`: Database adapters, ORM mappings, external API clients, message queue producers/consumers, file storage.
- `src/interfaces/` (or `controllers/`): HTTP routers/controllers, GraphQL resolvers, CLI commands, background job handlers.

## 2. Strict Architectural Rules
- **No Direct DB Calls in Controllers**: Controllers must only receive HTTP requests, parse DTOs, invoke Application Use Cases, and format HTTP responses.
- **Dependency Inversion**: High-level modules must never depend on low-level modules. Both must depend on abstractions (interfaces).
- **Zero ORM Leakage**: Never pass database models (e.g. Prisma models, TypeORM entities, SQLAlchemy models) directly out to the frontend as API responses. Always transform them into explicit DTOs / serialization schemas.
- **Fail Fast & Validate Input**: All external input must be validated at the boundary before reaching application use cases.

## 3. Immutability & Pure Functions
- Business rules and calculations within Domain entities should be pure functions with zero side effects.
- Avoid hidden global state, singleton state mutations, and non-deterministic logic in domain entities.
