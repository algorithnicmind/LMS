# LMS Portal - High Level Design (HLD)

---

## 1. System Context

```
┌──────────────────────────┐
│   Student (Browser)      │
├──────────────────────────┤
│   Instructor (Browser)   │
├──────────────────────────┤
│   Admin (Browser)        │
└────────────┬─────────────┘
             │ HTTPS / JSON
┌────────────▼─────────────┐
│   React.js Frontend      │
│   (Vite, SPA)            │
└────────────┬─────────────┘
             │ REST API (JWT)
┌────────────▼─────────────┐
│   Django Backend         │
│   (DRF, apps)            │
└────────────┬─────────────┘
             │ ORM
┌────────────▼─────────────┐
│   PostgreSQL             │
└──────────────────────────┘
```

## 2. Logical Components

### Frontend (React.js)
- **Design system layer**: Tailwind tokens, theme (light/dark), shared UI primitives.
- **Animation layer**: Framer Motion primitives (`PageTransition`, `RevealOnScroll`, `AnimatedCounter`, `MotionCard`); Three.js/R3F `ThreeHeroCanvas` (lazy-loaded, with fallback `AnimatedBackground`).
- **Auth & RBAC layer**: `AuthContext` (JWT state) + `ProtectedRoute` route guard per role; role redirects after login.
- **Landing**: animated hero with 3D background, animated stats, feature cards, course showcase, CTAs.
- **Auth pages**: animated login/register with motion feedback.
- **Learning**: lesson player, progress bar, quiz player, assignment submission.
- **Instructor module**: course/lesson/quiz/assignment management, grading.
- **Admin module**: user management, platform reports.

### Backend (Django)
- **users app**: custom User, auth views, JWT issuance, RBAC.
- **courses app**: Category, Course, Enrollment, Lesson.
- **assessments app**: Quiz, Question, Option, QuizAttempt, Assignment, Submission, grading logic.
- **progress app**: LessonCompletion, CourseProgress, report endpoints.

### Database (PostgreSQL)
- Single database `lms_db`, normalized schema, indexes on hot paths.

## 3. Data Flow (Request Lifecycle)

1. React component → Axios call with `Authorization: Bearer <JWT>`.
2. Django middleware: CORS → JWT authentication → permission check.
3. View/Serializer validates input → business logic in service layer.
4. ORM queries PostgreSQL → response serialized → JSON back to React.

> Frontend motion note: landing/3D scene renders client-side only (no data dependency);
> page transitions and micro-interactions do not block API requests.

## 3b. Frontend Runtime Layers

```
React App
 ├─ Providers: AuthProvider, ThemeProvider, ReducedMotionContext
 ├─ Router (AnimatePresence wrapper → PageTransition)
 │    ├─ PublicRoutes      (Landing, Login, Register, Catalog)
 │    ├─ StudentRoutes     (ProtectedRoute role=STUDENT)
 │    ├─ InstructorRoutes  (ProtectedRoute role=INSTRUCTOR)
 │    └─ AdminRoutes       (ProtectedRoute role=ADMIN)
 ├─ Animation primitives: RevealOnScroll, AnimatedCounter, MotionCard, Skeleton
 └─ ThreeHeroCanvas (lazy chunk) ──fallback──> AnimatedBackground (gradient/particles)
```

## 4. API Design Summary

| Resource        | Verbs                        | Auth                    |
| --------------- | ---------------------------- | ----------------------- |
| `/auth/*`       | POST                         | Public / token refresh |
| `/courses`      | GET, POST, PUT, DELETE       | Public read; write = Instr/Admin |
| `/enroll`       | POST                         | Student                 |
| `/lessons`      | GET, POST, PUT, DELETE       | Enrolled read; write = Instr/Admin |
| `/quizzes`      | GET, POST, attempt           | Student attempt         |
| `/assignments`  | GET, POST, submit, grade     | Student submit; Instr grade |
| `/progress`, `/reports` | GET                 | Owner / Instr / Admin   |

## 5. Security Design

- **Passwords**: Django's default PBKDF2 hashing (iterations=600000).
- **Tokens**: JWT access (15min) + refresh (7d rotating) via simplejwt, stored in **httpOnly cookies** (`SameSite=Strict`, `Secure`).
- **CSP**: `django-csp` with strict policy (see TRD §2.1.1).
- **HSTS**: `django-secure` → `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`.
- **RBAC**: `IsAuthenticated`, `IsInstructorOrAdmin`, owner checks on object-level permissions.
- **CORS**: Allow only frontend origin(s) from env (`CORS_ALLOWED_ORIGINS`).
- **Rate Limiting**: `django-ratelimit` (10/min on `/auth/token/`, 5/min on `/auth/register/`).
- **Brute Force**: `django-axes` lockout after 5 failed logins.
- **Sensitive Data**: `.env` for all secrets (SECRET_KEY, DB, JWT, SENTRY_DSN), never committed.
- **Dependency Scanning**: `npm audit` + `pip-audit` in CI, Dependabot alerts.
- **Error Tracking**: Sentry (frontend + backend) with source maps uploaded in CI.

## 6. Non-Functional Design

### 6.1 Performance Targets
| Metric | Target | Strategy |
|--------|--------|----------|
| LCP (Landing) | < 1.5s | Preload fonts, critical CSS inline, lazy 3D chunk |
| INP | < 200ms | Minimize main-thread work, code-split routes |
| CLS | < 0.1 | Reserve space for images/3D canvas |
| Lighthouse | ≥ 90 | All categories (Perf, A11y, BP, SEO) |
| API p95 | < 200ms | `select_related`/`prefetch_related`, DB indexes, caching |
| Bundle (gz) | < 150KB | Tree-shaking, dynamic imports for heavy libs |
| 3D FPS | 60fps mid-range | Shader-based, dpr clamp [1, 1.75], pause on hidden |

### 6.2 Scalability
- Stateless Django API → horizontal scaling behind load balancer
- PostgreSQL connection pooling (PgBouncer) for high concurrency
- CDN for static assets (Cloudflare, CloudFront)
- Redis cache for session data, rate limits, query results

### 6.3 Availability
- Health: `/health/` (liveness) + `/ready/` (readiness: DB, migrations, cache)
- Graceful shutdown handling (SIGTERM)
- Rolling deployments with zero-downtime

### 6.4 Observability
| Layer | Tool | Implementation |
|-------|------|----------------|
| Frontend Errors | Sentry | `ErrorBoundary` per route, `captureException` |
| Backend Errors | Sentry | Django integration, request context |
| Performance | Web Vitals + Sentry | `web-vitals` lib, custom metrics |
| Logs | Structured JSON | `python-json-logger`, correlation IDs |
| Metrics | Prometheus/Grafana | `/metrics` endpoint (django-prometheus) |

### 6.5 Accessibility (WCAG 2.1 AA)
- Semantic HTML, proper heading hierarchy
- Focus visible outlines (Tailwind `focus-visible:ring`)
- ARIA labels on icon buttons, live regions for toasts
- Color contrast ≥ 4.5:1 (Tailwind tokens verified)
- Keyboard navigation for all interactive elements
- `prefers-reduced-motion` respected globally (`ReducedMotionContext`)

## 7. Deployment (Target)

- Backend: gunicorn + Django on a VPS/container; media served via static/media config.
- Frontend: static build served by Nginx (reverse proxy `/api/` → Django).
- DB: managed PostgreSQL.
- Optional: `docker-compose.yml` (db, backend, frontend-nginx).
