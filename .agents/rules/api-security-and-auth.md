---
description: Backend security, OWASP Top 10 API Security, Authentication, Authorization, and Secret handling rules
globs: ["**/*.{py,js,ts,go,java,cs,rs,php}"]
---

# API Security, Authentication & Secret Management Rules

## 1. OWASP Top 10 API Security Protections
- **Broken Object-Level Authorization (BOLA / IDOR)**: Never rely solely on an entity ID from user input. Always verify that the authenticated user/tenant owns the resource (`WHERE id = :id AND org_id = :org_id`).
- **SQL / NoSQL Injection**:
  - Always use parameterized queries or prepared statements provided by ORMs/Query builders.
  - NEVER construct SQL strings via raw string concatenation (`f"SELECT * FROM users WHERE email = '{email}'"` is strictly forbidden).
- **Mass Assignment**: Whitelist accepted input fields explicitly using strict schema validators (Zod, Pydantic, Marshmallow). Strip unknown keys.
- **Sensitive Data Exposure**: Exclude passwords, password hashes, API keys, internal IDs, and tokens from all serialization/responses.

## 2. Secrets & Environment Variables
- **Zero Hardcoded Secrets**: Never commit passwords, API secrets, private keys, or tokens to source code.
- **Environment Validation**: Validate environment variables at application startup (using Zod/Pydantic/Envalid) and crash early with a descriptive error if required keys are missing.
- **Credential Storage**: Use `argon2id` (or `bcrypt` with work factor >= 12) for user passwords. Never use MD5, SHA-1, or plain SHA-256 for passwords.

## 3. CORS & Network Security
- Restrict `Access-Control-Allow-Origin` to specific trusted domains in production. Never use `*` with credentials enabled (`credentials: true`).
- Enforce HTTPS across all environments outside local development.
- Implement rate limiting per IP / per user token to protect against brute force and DDoS.
