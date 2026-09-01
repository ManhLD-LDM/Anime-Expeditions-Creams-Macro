---
name: api-engineering-rest-graphql
description: Comprehensive workflow for designing, implementing, and securing production-grade REST and GraphQL APIs with standardized responses, validation, pagination, and auth.
---

# API Engineering (REST & GraphQL) Standards

This skill provides the authoritative standard for building clean, resilient, and secure APIs.

---

## 1. RESTful API Resource Naming & HTTP Methods

### URL Conventions:
- **Plural Nouns**: Use plural nouns for resources (`/api/v1/users`, `/api/v1/orders`).
- **Hierarchy & Relationships**: `/api/v1/organizations/:orgId/members/:memberId`.
- **Kebab-Case URLs**: `/api/v1/payment-methods`, not camelCase or snake_case in URL paths.
- **Versioning**: Mandatory version prefix in path (`/api/v1/`) or accept header.

### HTTP Verb Semantics:
| Method | Purpose | Idempotent | Success Code |
| :--- | :--- | :--- | :--- |
| **`GET`** | Read resource(s) | Yes | `200 OK` |
| **`POST`** | Create a new resource or trigger an action | No | `201 Created` (with `Location` header) |
| **`PUT`** | Full replacement of resource | Yes | `200 OK` |
| **`PATCH`** | Partial update of resource fields | No/Yes | `200 OK` |
| **`DELETE`** | Remove a resource | Yes | `200 OK` or `204 No Content` |

---

## 2. Standardized Response & Error Envelopes

### Success Envelope:
```json
{
  "success": true,
  "data": {
    "id": "usr_01HXYZ12345",
    "name": "Jane Doe",
    "email": "jane@example.com"
  },
  "meta": {
    "timestamp": "2026-09-02T04:00:00.000Z",
    "requestId": "req_abc123"
  }
}
```

### Paginated List Envelope:
```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "cursor": "eyJpZCI6MTIzfQ==",
    "hasMore": true,
    "limit": 20,
    "totalCount": 145
  }
}
```

### Standard Error Envelope (RFC 7807 Inspired):
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "The provided payload failed validation constraints.",
    "details": [
      {
        "field": "email",
        "issue": "Invalid email address format."
      },
      {
        "field": "age",
        "issue": "Age must be at least 18."
      }
    ],
    "requestId": "req_abc123"
  }
}
```

---

## 3. Pagination & Filtering Best Practices

1. **Cursor-Based Pagination (Recommended for large/real-time datasets)**:
   - Query: `GET /api/v1/posts?cursor=eyJjcmVhdGVkX2F0IjoiMjAyNi...&limit=20`
   - Prevents duplicate items when new records are inserted between page reads.
2. **Offset-Based Pagination (For small admin tables)**:
   - Query: `GET /api/v1/items?page=1&limit=20`
   - Enforce hard maximum limit (e.g. `limit <= 100`) to prevent DB exhaustion.
3. **Filtering & Sorting**:
   - Filter: `GET /api/v1/orders?status=completed&min_total=100`
   - Sort: `GET /api/v1/users?sort=-created_at,name` (prefix `-` indicates descending).

---

## 4. Request Validation & Schema Contracts

Every incoming payload must be validated before entering the business layer:
- **TypeScript**: Use `Zod` or `TypeBox`.
- **Python**: Use `Pydantic v2` with strict validation.
- **Go**: Use `go-playground/validator`.
- Strip unrecognized fields (`strict()` or `extra = 'forbid'`) to prevent **Mass Assignment Vulnerabilities**.

```typescript
// Example Zod Contract
export const CreateUserSchema = z.object({
  email: z.string().email().max(255).toLowerCase(),
  password: z.string().min(12).max(128),
  role: z.enum(['USER', 'ADMIN']).default('USER'),
}).strict();
```

---

## 5. Authentication & Authorization Patterns

1. **Token Strategy**:
   - Short-lived Access Token (JWT, 15m expiration, signed with asymmetric `RS256` or `EdDSA`).
   - Long-lived Refresh Token (stored in database with rotation on each use, hashed with SHA-256).
2. **Cookies & Transport**:
   - Store session/refresh tokens in `HttpOnly; Secure; SameSite=Strict` cookies to block XSS theft.
3. **RBAC & ABAC**:
   - Check permissions at the service layer, not just the router level.
   - Guard against **BOLA / IDOR** (Broken Object-Level Authorization):
     ```typescript
     // Always verify tenant/ownership scope
     const order = await orderRepo.findByIdAndOrg(orderId, currentUser.organizationId);
     if (!order) throw new NotFoundException('Order not found');
     ```

---

## 6. Rate Limiting & Security Headers

- Apply rate limiting on public and auth endpoints (`100 req/min` general, `5 req/min` for `/auth/login`).
- Always send standard security headers:
  - `Content-Security-Policy: default-src 'self'`
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Strict-Transport-Security: max-age=31536000; includeSubDomains`
