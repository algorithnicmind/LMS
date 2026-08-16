# LMS Portal - Security Documentation

## Overview
This document outlines the security measures implemented in the LMS Portal to protect user data, prevent common vulnerabilities, and ensure compliance with security best practices.

## Authentication & Authorization

### JWT Token Strategy
- **Access Tokens**: 15-minute lifetime, stored in httpOnly cookies
- **Refresh Tokens**: 7-day lifetime, rotating (new refresh token on each use), blacklisted after rotation
- **Cookie Settings**: `Secure`, `HttpOnly`, `SameSite=Strict`
- **Storage**: Never in localStorage/sessionStorage

### Password Security
- Django's PBKDF2 with 600,000 iterations (default in Django 6.1)
- Minimum length: 8 characters
- Common password validation enabled
- Numeric password validation enabled

### Rate Limiting
| Endpoint | Limit | Window |
|----------|-------|--------|
| `/api/v1/auth/token/` | 10 requests | 1 minute |
| `/api/v1/auth/token/refresh/` | 20 requests | 1 minute |
| `/api/v1/auth/register/` | 5 requests | 1 minute |
| `/api/v1/auth/password/reset/` | 3 requests | 1 hour |

### Brute Force Protection
- `django-axes` tracks failed login attempts
- Lockout after 5 failed attempts for 1 hour
- Admin can unlock via Django admin

## Content Security Policy (CSP)

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline';  # Tailwind JIT
  img-src 'self' data: https:;
  font-src 'self' data:;
  object-src 'none';
  base-uri 'self';
  frame-ancestors 'none';
  form-action 'self';
```

## HTTP Security Headers

| Header | Value |
|--------|-------|
| Strict-Transport-Security | max-age=31536000; includeSubDomains; preload |
| X-Content-Type-Options | nosniff |
| X-Frame-Options | DENY |
| Referrer-Policy | strict-origin-when-cross-origin |
| Permissions-Policy | camera=(), microphone=(), geolocation=() |
| Cross-Origin-Opener-Policy | same-origin |
| Cross-Origin-Resource-Policy | same-origin |

## CORS Configuration

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Dev
    "https://app.yourdomain.com",  # Production
]
CORS_ALLOW_CREDENTIALS = True
```

## Input Validation & Sanitization

### Backend
- DRF serializers validate all input
- Custom validators for file uploads (type, size)
- SQL injection prevention via Django ORM (parameterized queries)
- XSS prevention via Django template auto-escaping

### Frontend
- React auto-escapes JSX content
- Zod schemas validate forms before submission
- DOMPurify for any user-generated HTML content
- File upload validation (client + server)

## Data Protection

### At Rest
- PostgreSQL TLS encryption (Neon managed)
- Database credentials in environment variables
- Secrets never logged (Sentry scrubbers configured)

### In Transit
- TLS 1.3 enforced (HSTS)
- All API calls over HTTPS in production
- Secure cookies only over HTTPS

### PII Handling
- Email, name stored (minimal PII)
- No SSN, payment info, or sensitive docs
- Right to deletion via admin panel
- Data retention: 7 years for enrollment records

## File Upload Security

- Allowed types: PDF, DOCX, MP4, WebM, JPG, PNG, WebP
- Max size: 100MB (configurable)
- Virus scanning: ClamAV in CI/CD pipeline
- Storage: S3-compatible with signed URLs (expiry: 1 hour)
- No direct execution permissions on upload directory

## API Security

### Versioning
- All endpoints under `/api/v1/`
- Deprecation policy: 6 months notice

### Request Validation
- DRF throttling classes per endpoint
- Request size limits (10MB default)
- JSON parser strict mode

### Error Handling
- Generic error messages in production (no stack traces)
- Structured error codes for frontend handling
- Correlation IDs for tracing

## Dependency Management

### Scanning
- `npm audit` on every PR (GitHub Actions)
- `pip-audit` on every PR
- Dependabot alerts for CVE notifications
- Trivy container scanning for Docker images

### Pinning
- Exact versions in `requirements.txt` and `package-lock.json`
- No floating versions (`^`, `~`)
- Regular updates (monthly) with testing

## Incident Response

### Detection
- Sentry alerts for error spikes
- Log monitoring for anomalous patterns
- Rate limit breach alerts

### Response Plan
1. **Identify**: Confirm breach, assess scope
2. **Contain**: Rotate secrets, revoke tokens, block IPs
3. **Eradicate**: Patch vulnerability, remove malicious code
4. **Recover**: Restore from clean backup, verify integrity
5. **Postmortem**: Document, improve defenses

### Key Contacts
- Security team: security@yourdomain.com
- On-call: PagerDuty rotation
- Legal: legal@yourdomain.com

## Compliance Considerations

| Standard | Status | Notes |
|----------|--------|-------|
| GDPR | Designed for compliance | Data minimization, right to deletion, DPA ready |
| CCPA | Designed for compliance | Opt-out mechanisms, data inventory |
| SOC 2 Type II | Future | Logging, access controls, monitoring in place |
| ISO 27001 | Future | Risk assessment, policies documented |

## Security Checklist for Deployments

- [ ] All secrets rotated from development values
- [ ] CSP headers verified in production
- [ ] HSTS preload submitted (after testing)
- [ ] Rate limits tuned for production traffic
- [ ] Sentry DSN configured for production
- [ ] Backup encryption verified
- [ ] SSL certificate valid (Let's Encrypt auto-renewal)
- [ ] Security headers scanned (securityheaders.com)
- [ ] Dependency audit clean (no critical CVEs)
- [ ] Penetration test scheduled (annual)

## Reporting Security Issues

**Responsible Disclosure**: Email security@yourdomain.com with:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (optional)

**Response Time**: Acknowledgment within 24 hours, fix timeline based on severity.

---

*Last updated: 2026-08-16*
*Version: 1.0*