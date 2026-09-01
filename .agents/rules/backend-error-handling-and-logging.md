---
description: Structured JSON logging, tracing, error handling, and observability rules for backend services
globs: ["**/*.{py,js,ts,go,java,cs,rs,php}"]
---

# Backend Error Handling & Observability Rules

## 1. Structured JSON Logging
- Always emit logs in structured JSON format in production (using Winston, Pino, Structlog, Zap, Zerolog):
  ```json
  {
    "timestamp": "2026-09-02T04:00:00.123Z",
    "level": "error",
    "message": "Payment processing failed",
    "service": "billing-service",
    "trace_id": "c8a4df59-1f4a-4a2b-8a8b-1e2f3a4b5c6d",
    "user_id": "usr_9981",
    "error_code": "CARD_DECLINED",
    "http_status": 402
  }
  ```
- **Log Levels**:
  - `DEBUG`: Verbose internal state for local debugging.
  - `INFO`: Significant lifecycle milestones (server started, job completed, user registered).
  - `WARN`: Recoverable unexpected situations (cache miss fallback, rate limit reached, slow query).
  - `ERROR`: Unhandled exceptions, failed third-party dependencies, data corruption alerts.

## 2. Centralized Error Handling
- Use custom AppError / DomainError classes with HTTP status codes and domain error codes:
  ```typescript
  export class AppError extends Error {
    constructor(
      public readonly message: string,
      public readonly statusCode: number = 500,
      public readonly code: string = 'INTERNAL_SERVER_ERROR',
      public readonly isOperational: boolean = true,
      public readonly details?: any
    ) {
      super(message);
    }
  }
  ```
- **Zero Stack Traces to Clients**: In production responses, never leak database queries, internal file paths, or raw stack traces. Return a clean standardized error envelope.

## 3. Distributed Tracing & Correlation
- Pass `X-Request-Id` / `traceparent` headers through every downstream microservice or async worker.
- Tie all logs, database queries, and external API requests for a single request to the same `requestId`.
