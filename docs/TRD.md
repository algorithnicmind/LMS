# LMS Portal - Technical Requirements Document (TRD)

| Item           | Detail                                  |
| -------------- | --------------------------------------- |
| Product        | LMS Portal                              |
| Version        | 1.0                                     |
| Stack          | React.js / Django / PostgreSQL          |

---

## 1. Frontend (React.js)

### 1.1 Tooling
- React 18+ with Vite (fast build).
- React Router for routing.
- Axios for HTTP requests to Django API.
- Context API or Redux Toolkit for auth/user state.
- **Tailwind CSS** (v4) for styling and design-system tokens.
- **Framer Motion** for animations: route transitions (`AnimatePresence`), scroll reveals, hover/press micro-interactions, animated counters.
- **Three.js + @react-three/fiber + @react-three/drei** for the animated 3D hero background on the landing page.
- **RBAC**: `ProtectedRoute` wrapper component reading user role from AuthContext; redirects unauthorized users by role.

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
- Django 5.x + Django REST Framework (DRF).
- `djangorestframework-simplejwt` for JWT auth.
- `psycopg2` driver, `dj-database-url` for DB config.
- `django-cors-headers` for frontend/backend CORS.

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

- `backend/requirements.txt` + `.env` for secrets (SECRET_KEY, DB, JWT).
- `frontend/package.json`, `.env` with `VITE_API_URL`.
- Docker (optional): `docker-compose.yml` for postgres service.
- Dev servers: Django `http://127.0.0.1:8000`, Vite `http://127.0.0.1:5173`.
