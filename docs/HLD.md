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
- **Auth module**: login, register, JWT storage, route guards.
- **Catalog**: course list/search/detail.
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

- Passwords: Django's default PBKDF2 hashing.
- Tokens: JWT access (short-lived) + refresh (long-lived) via simplejwt.
- RBAC: `IsAuthenticated`, `IsInstructorOrAdmin`, owner checks.
- CORS: allow only frontend origin(s) from env.
- Sensitive data in `.env` (SECRET_KEY, DB credentials), never committed.

## 6. Non-Functional Design

- **Performance**: DB indexes (`course.status`, `enrollment.student`, `lesson.order`), select_related/prefetch_related in list endpoints.
- **Scalability**: stateless Django API → scale horizontally; PostgreSQL connection pooling.
- **Availability**: single instance v1; restart policies; health check endpoint `GET /health/`.
- **Observability**: Django logging to console/file; request-id middleware.

## 7. Deployment (Target)

- Backend: gunicorn + Django on a VPS/container; media served via static/media config.
- Frontend: static build served by Nginx (reverse proxy `/api/` → Django).
- DB: managed PostgreSQL.
- Optional: `docker-compose.yml` (db, backend, frontend-nginx).
