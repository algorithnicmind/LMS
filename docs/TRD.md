# LMS Portal - Technical Requirements Document (TRD)

| Item           | Detail                                  |
| -------------- | --------------------------------------- |
| Product        | LMS Portal                              |
| Version        | 1.0                                     |
| Stack          | React 19 / TypeScript / Django 6.1 / PostgreSQL |

---

## Production-Grade Non-Functional Requirements

### Performance Targets
| Metric | Target | Measurement |
|--------|--------|-------------|
| LCP (Landing) | < 1.5s | Web Vitals (75th percentile) |
| INP | < 200ms | Web Vitals |
| CLS | < 0.1 | Web Vitals |
| Lighthouse Score | ≥ 90 | Performance / A11y / Best Practices / SEO |
| API p95 | < 200ms | Django + DRF (cached queries) |
| Bundle Size (gz) | < 150KB | Initial JS + CSS |
| 3D Scene FPS | 60fps mid-range | R3F, dpr clamp [1, 1.75] |

### Security Requirements
| Requirement | Implementation |
|-------------|----------------|
| CSP Headers | `django-csp`: `script-src 'self'; object-src 'none'; base-uri 'self'; img-src 'self' data: https:; font-src 'self' data:;` |
| HSTS | `django-secure`: `SECURE_HSTS_SECONDS=31536000`, `SECURE_HSTS_INCLUDE_SUBDOMAINS=True` |
| Cookie Security | `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `SAMESITE=Strict` |
| JWT | Access 15min, Refresh 7d rotating, stored in httpOnly cookies |
| Rate Limiting | `django-ratelimit`: 10 req/min on `/auth/token/`, 5 req/min on `/auth/register/` |
| Dependency Scanning | `npm audit` + `pip-audit` in CI, Dependabot alerts |
| XSS Protection | React auto-escape, Django templates auto-escape, CSP |
| CSRF Protection | Django CSRF middleware + `SameSite=Strict` cookies |

### Observability
| Layer | Tool | Key Signals |
|-------|------|-------------|
| Frontend Errors | Sentry | React error boundaries, source maps |
| Backend Errors | Sentry | Django integration, request context |
| Performance | Web Vitals + Sentry | LCP, INP, CLS, TTFB |
| Logs | Structured JSON | Correlation IDs, request tracing |
| Health | `/health/` + `/ready/` | DB pool, migrations, cache |

### Accessibility (WCAG 2.1 AA)
- Semantic HTML, proper heading hierarchy (h1 → h2 → h3)
- Focus visible: `focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2`
- ARIA labels on icon buttons, live regions for toasts
- Color contrast ≥ 4.5:1 (verified in Tailwind tokens)
- Keyboard navigation for all interactive elements
- `prefers-reduced-motion` respected globally (already implemented)

### Testing Strategy
| Type | Tool | Coverage Target |
|------|------|-----------------|
| Unit (FE) | Vitest + React Testing Library | 80% components |
| Unit (BE) | pytest + factory_boy | 85% services/serializers |
| Integration | RTK Query + MSW mocks | Critical API flows |
| E2E | Playwright (chromium, firefox, webkit) | Auth, enroll, quiz, progress |
| Visual Regression | Playwright snapshots | Key pages |
| Accessibility | axe-core in CI | 0 violations |

---

## 1. Frontend (React.js)

## 1. Frontend (React.js)

### 1.1 Tooling
- React 19 + TypeScript with Vite 8 (fast build, ES modules native).
- React Router v7 for routing (data loading, actions).
- **TanStack Query (React Query) v5** for server state: caching, deduping, retries, prefetch, optimistic updates.
- **Zustand** for client UI state (modals, sidebars, theme).
- **React Hook Form + Zod** for forms: performant, schema validation shared with backend.
- **shadcn/ui** (Radix UI primitives + Tailwind) for accessible UI components: Button, Input, Card, Dialog, Toast, Table, Select, etc.
- **Axios** (thin wrapper) for HTTP with interceptors (auth refresh, error normalization).
- **Tailwind CSS v4** for styling and design-system tokens (colors, spacing, radii, shadows, typography).
- **Framer Motion** for animations: route transitions (`AnimatePresence`), scroll reveals, hover/press micro-interactions, animated counters.
- **Three.js + @react-three/fiber + @react-three/drei** for the animated 3D hero background on the landing page.
- **RBAC**: `ProtectedRoute` wrapper component reading user role from AuthContext; redirects unauthorized users by role.
- **Error Boundaries**: Per-route React error boundaries with fallback UI.
- **Suspense Boundaries**: For code-split routes and async components.

### 1.2 Pages / Routes
| Route                    | Access | Purpose                          |
| ------------------------ | ------ | -------------------------------- |
| `/`                      | Public | **Animated landing page** (3D animated background, motion UI) |
| `/login`                 | Public | Animated login                   |
| `/register`              | Public | Animated student registration    |
| `/courses`               | Public | Browse courses                   |
| `/courses/:id`           | Public | Course details                   |
| `/courses/:id/learn`     | Student | Lesson player (enrolled)         |
| `/courses/:id/quiz/:qid` | Student | Take quiz                        |
| `/assignments`           | Student | My assignments                   |
| `/dashboard`             | Student | My progress                      |
| `/instructor/*`          | Instructor | Course/lesson/quiz/assignment CRUD |
| `/admin/*`               | Admin | Users, courses, reports          |

### 1.3 Key Components
- `AuthContext` – token storage, login/logout, route guards.
- `ProtectedRoute` – RBAC guard: takes `role` prop (STUDENT/INSTRUCTOR/ADMIN); redirects guests to `/login` and wrong-role users to their dashboard.
- `LandingPage` – animated hero, `ThreeHeroCanvas`, animated stats, feature cards, course showcase, CTAs.
- `ThreeHeroCanvas` – Three.js scene via R3F; lazy-loaded, renders behind hero; falls back to gradient-mesh animation while loading / when WebGL unavailable.
- `AnimatedBackground` – reusable animated gradient/particle layer (used by landing + auth).
- `AuthPage` – animated login/register: field focus rings, button loading/error shake states.
- `PageTransition` – Framer Motion `AnimatePresence` wrapper for route enter/exit animations.
- `RevealOnScroll`, `AnimatedCounter`, `MotionCard` – reusable motion primitives.
- `CourseCard`, `LessonViewer`, `QuizPlayer`, `AssignmentForm`.
- `ProgressBar`, `ReportsTable`, `Skeleton`, `EmptyState`, `ErrorState`.

### 1.4 Design System & Motion Spec
- **Styling**: Tailwind CSS utility classes + design tokens (colors, spacing, radii, shadows, typography) in `tailwind.config`.
- **Palette**: primary (brand), secondary, accent, success/warning/danger, neutrals (light/dark modes supported).
- **Typography**: 2 type scales (display + body), consistent heading hierarchy.
- **Motion tokens** (Framer Motion):
  - Durations: `fast = 0.15s`, `base = 0.3s`, `slow = 0.6s`.
  - Easings: `standard`, `decelerate` (exit), `spring` (hero/success).
  - Micro-interactions: hover lift + shadow, press scale `0.97`, focus ring transition.
  - Route transition: enter `fade + slideY 24px`, exit `fade` (300ms).
- **3D scene budget**: hero canvas ≤ 60fps on mid-range devices; auto-pause on tab hidden; `dpr` clamp `[1, 1.75]`; lazy-load chunk ~1.5MB max.
- **Accessibility**: global `useReducedMotion()` from Framer Motion; when reduced, all motion collapses to instant/static states.

## 2. Backend (Django)

### 2.1 Setup
- Django 6.1 + Django REST Framework (DRF).
- `djangorestframework-simplejwt` for JWT auth (access 15m, refresh 7d rotating).
- `psycopg2` driver, `dj-database-url` for DB config.
- `django-cors-headers` for frontend/backend CORS.
- `django-csp` for Content Security Policy headers.
- `django-secure` for HSTS, SSL redirect, secure cookies.
- `django-ratelimit` for rate limiting on auth endpoints.
- `django-axes` for brute-force protection on login.
- `sentry-sdk[django]` for error tracking.

### 2.1.1 Security Configuration
```python
# settings.py additions
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_SAMESITE = 'Strict'

# CSP
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # Tailwind JIT needs inline
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_FONT_SRC = ("'self'", "data:")
CSP_OBJECT_SRC = ("'none'",)
CSP_BASE_URI = ("'self'",)
CSP_FRAME_ANCESTORS = ("'none'",)

# SimpleJWT cookie settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_COOKIE': 'access_token',
    'AUTH_COOKIE_REFRESH': 'refresh_token',
    'AUTH_COOKIE_SECURE': True,
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_SAMESITE': 'Strict',
}

# Rate limiting
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'
```

### 2.2 Django Apps
| App          | Responsibility                             |
| ------------ | ------------------------------------------ |
| `users`      | Custom User model, auth, roles (admin/instructor/student) |
| `courses`    | Course, Category, Enrollment, Lesson       |
| `assessments`| Quiz, Question, Option, QuizAttempt, Assignment, Submission |
| `progress`   | LessonCompletion, CourseProgress, Reports  |

### 2.3 Custom User Model
- `email` (username field), `name`, `role` (choices: ADMIN/INSTRUCTOR/STUDENT), `is_active`.
- Extend `AbstractUser` from day one (avoids migration pain later).

### 2.4 REST API (v1)

**Auth**
- `POST /api/v1/auth/register/` – register student
- `POST /api/v1/auth/token/` – obtain JWT
- `POST /api/v1/auth/token/refresh/` – refresh JWT
- `GET /api/v1/users/me/` – current profile

**Courses**
- `GET /api/v1/courses/` – list published
- `GET /api/v1/courses/{id}/` – detail
- `POST /api/v1/courses/` – create (Instructor/Admin)
- `PUT/DELETE /api/v1/courses/{id}/`
- `POST /api/v1/courses/{id}/enroll/` – enroll
- `GET /api/v1/courses/{id}/lessons/`

**Lessons**
- `POST/PUT/DELETE /api/v1/lessons/`
- `POST /api/v1/lessons/{id}/complete/`

**Quizzes**
- `POST /api/v1/courses/{id}/quizzes/`
- `GET /api/v1/quizzes/{id}/` – questions + options
- `POST /api/v1/quizzes/{id}/attempt/` – submit answers → auto-grade

**Assignments**
- `POST/PUT/DELETE /api/v1/assignments/`
- `POST /api/v1/assignments/{id}/submit/`
- `POST /api/v1/submissions/{id}/grade/` – Instructor grades

**Progress / Reports (Admin/Instructor)**
- `GET /api/v1/progress/courses/{id}/` – course progress
- `GET /api/v1/reports/students/`
- `GET /api/v1/reports/courses/`

### 2.5 Permissions (RBAC)
- Default: `IsAuthenticated`.
- Course write: `IsInstructorOrAdmin`.
- Enrollment: students only.
- Grading: instructor of that course / admin.

## 3. Database (PostgreSQL)

### 3.1 Entities
- `User` (custom), `Category`, `Course`, `Lesson`, `Enrollment`, `Quiz`, `Question`, `Option`, `QuizAttempt`, `Assignment`, `Submission`, `LessonCompletion`.

### 3.2 Key Relations
- Course 1–N Lesson
- Course 1–N Quiz, Course 1–N Assignment
- User N–M Course via Enrollment (with status, enrolled_at)
- QuizAttempt 1–1 Quiz + User
- Submission 1–1 Assignment + User

### 3.3 Config
- DB: `lms_db`, user `lms_user`, port `5432`.
- Use Django migrations; add indexes on `course.status`, `enrollment.student`, `lesson.order`.

## 4. Environment & Tooling

### 4.1 Backend
- `backend/requirements.txt` + `.env` for secrets (SECRET_KEY, DB, JWT, SENTRY_DSN).
- **Required packages** (add to requirements.txt):
  ```
  django-csp
  django-secure
  django-ratelimit
  django-axes
  sentry-sdk
  ```

### 4.2 Frontend
- `frontend/package.json`, `.env` with `VITE_API_URL`, `VITE_SENTRY_DSN`.
- **Required packages** (add to package.json):
  ```
  @tanstack/react-query
  zustand
  react-hook-form
  @hookform/resolvers
  zod
  @radix-ui/react-dialog
  @radix-ui/react-dropdown-menu
  @radix-ui/react-select
  @radix-ui/react-toast
  @radix-ui/react-tooltip
  class-variance-authority
  clsx
  tailwind-merge
  lucide-react
  ```

### 4.3 CI/CD (GitHub Actions)
```yaml
# .github/workflows/ci.yml
stages:
  - lint: oxlint + ruff
  - typecheck: tsc --noEmit + pyright/mypy
  - test: vitest --coverage + pytest --cov
  - build: vite build + python -m build
  - e2e: playwright (chromium, firefox, webkit)
  - security: npm audit + pip-audit + trivy (container)
  - deploy: staging → production (manual approval)
```

### 4.4 Docker (Optional)
- `docker-compose.yml`: postgres, backend, frontend-nginx
- Multi-stage builds for minimal production images
- Health checks on all services

### 4.5 Dev Servers
- Django: `http://127.0.0.1:8000`
- Vite: `http://127.0.0.1:5173`
