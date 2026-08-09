# Security Hardening Architecture

This document describes the security policies, headers, payload sanitization, and data protection measures in place for the **ABTalks AI Interview Agent**.

---

## 🛡️ Security Layers

### 1. HTTP Security Response Headers
Configured via `SecurityHeadersMiddleware` in `backend/app/core/security_middleware.py`:
- `X-Content-Type-Options: nosniff` — Prevents MIME-type sniffing attacks.
- `X-Frame-Options: DENY` — Protects against clickjacking.
- `X-XSS-Protection: 1; mode=block` — Enables browser XSS filtering.
- `Strict-Transport-Security` — Enforces HSTS HTTPS connections.
- `Content-Security-Policy` — Restricts script execution to trusted self domains.

### 2. Request Payload Size Guard
Configured via `RequestSizeLimitMiddleware`:
- Maximum HTTP request payload size cap enforced at **2MB**.
- Requests exceeding 2MB automatically return HTTP `413 Payload Too Large`.

### 3. Cross-Origin Resource Sharing (CORS)
- Strict methods permitted: `GET`, `POST`, `OPTIONS`.
- Explicit origins specified via environment configuration (`settings.CORS_ORIGINS`).

### 4. Input Sanitization & XSS Prevention
- Frontend client utility `sanitizeInput` in `frontend/src/services/apiClient.js`:
  - Escapes special HTML characters (`<`, `>`, `&`, `"`, `'`) before rendering user content.

### 5. Memory & Data Encryption
- Sensitive candidate responses stored in session memory are encrypted via AES-256 equivalent wrappers in `MemorySecurity`.
