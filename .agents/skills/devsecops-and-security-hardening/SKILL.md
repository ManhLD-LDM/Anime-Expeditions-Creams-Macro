---
name: devsecops-and-security-hardening
description: Comprehensive workflow for software supply chain security, dependency auditing, SAST scanning, secret leak prevention, and application security hardening.
---

# DevSecOps & Security Hardening Workflow

This skill defines the methodology for embedding security practices throughout the software development lifecycle (Secure SDLC).

---

## 1. Software Supply Chain & Dependency Auditing

Regularly audit third-party libraries for known vulnerabilities (CVEs):

### Node.js / TypeScript:
```bash
# Check production dependencies for critical/high vulnerabilities
npm audit --omit=dev --audit-level=high
```

### Python:
```bash
# Scan active environment or requirements file for known CVEs
pip-audit -r requirements.txt
```

### Container Images:
```bash
# Scan Docker image filesystem for OS & package vulnerabilities
trivy image --severity HIGH,CRITICAL my-app:latest
```

---

## 2. Secret Scanning & Leak Prevention

Never allow credentials to enter Git history:

1. **Pre-Commit Secret Detection**:
   - Use `gitleaks` or `trufflehog` to scan staged files before commit.
2. **Environment Variable Rules**:
   - All secret variables (`DATABASE_URL`, `JWT_SECRET`, `STRIPE_KEY`) must be loaded from `.env` (ignored by Git) or secret managers (AWS Secrets Manager, HashiCorp Vault, Doppler).
3. **Accidental Leak Protocol**:
   - If a secret is accidentally committed, **immediately revoke/rotate the secret** on the provider platform. Rewriting Git history alone is NOT sufficient.

---

## 3. Defense-in-Depth Hardening Checklist

- [ ] **Input Sanitization**: Escape/sanitize all user-generated content before rendering HTML to prevent XSS (e.g. `DOMPurify.sanitize()`).
- [ ] **SQL Injection Prevention**: 100% parameterized queries or ORM query builders.
- [ ] **Strict Security Headers (Helmet / Nginx)**:
  - `Content-Security-Policy: default-src 'self'`
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- [ ] **Authentication Robustness**:
  - Store passwords using `argon2id` (memory >= 64MB, iterations >= 3) or `bcrypt` (cost >= 12).
  - Rate-limit login and password-reset endpoints to prevent brute-force attacks.
  - Store session tokens in `HttpOnly; Secure; SameSite=Strict` cookies.
