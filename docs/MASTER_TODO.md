# LMS Portal - Master TODO

> Ordered build plan. Check off items as completed.

Legend: [ ] = pending, [x] = done

## Phase 0 - Project Setup

- [x] Create `backend/` Django project (config app, virtualenv)
- [x] Create `frontend/` React + Vite app (React 19, Vite 8, TypeScript)
- [x] Add `requirements.txt` (django, djangorestframework, simplejwt, django-cors-headers, psycopg2, python-dotenv, dj-database-url)
- [x] Add `.env.example` and root `.gitignore` (venv, node_modules, .env, media, static, dist)
- [x] Configure PostgreSQL connection (Neon) + initial migration
- [x] Install `django-cors-headers`, allow Vite origin
- [x] Health endpoint `GET /health/`
- [x] Install Tailwind CSS (v4) + design tokens (colors, typography, spacing, shadows)
- [x] Install Framer Motion + `@react-three/fiber`, `@react-three/drei`, `three`
- [x] Build motion primitives: `PageTransition`, `RevealOnScroll`, `AnimatedCounter`, `MotionCard`, `Skeleton`
- [x] `ReducedMotionContext` (respects `prefers-reduced-motion` globally)

## Phase 1 - Landing Page + Auth + RBAC

- [ ] **Landing page**: hero section with staggered text reveal + CTAs
- [ ] **3D animated background**: `ThreeHeroCanvas` (lazy-loaded) + `AnimatedBackground` fallback (gradient/particles)
- [ ] Landing sections: animated stats, features grid (scroll reveals), course showcase, footer
- [ ] **Animated auth pages**: login + register with motion enter, focus rings, error shake, loading button states
- [ ] Custom User model (email, name, role) + migration
- [ ] Register API (student), Login API (JWT access/refresh)
- [ ] RBAC permissions (`IsInstructorOrAdmin`) on backend
- [ ] `ProtectedRoute` role guard + role-based redirects after login (Student/Instructor/Admin dashboards)
- [ ] Profile endpoint `GET /api/v1/users/me/`
- [ ] Admin: create instructor account endpoint
- [ ] Tests: auth happy path + role denials

## Phase 2 - Course & Lesson Management

- [ ] Models: Category, Course, Lesson, Enrollment + migrations
- [ ] Course CRUD API (write: instructor/admin)
- [ ] Lesson CRUD API (ordered within course)
- [ ] Enrollment API (student, unique per course)
- [ ] Publish/draft gating (students only see PUBLISHED)
- [ ] React: catalog, course detail, enroll button
- [ ] React: instructor course/lesson forms
- [ ] Media handling: thumbnails, video uploads
- [ ] Tests: CRUD + permission matrix

## Phase 3 - Quizzes

- [ ] Models: Quiz, Question, Option, QuizAttempt + migrations
- [ ] Instructor quiz builder API (options with `is_correct`)
- [ ] Student attempt API with auto-grading service
- [ ] Attempt result stored; score visible to student
- [ ] React: quiz player + result banner
- [ ] Tests: grading math, hidden correct answers

## Phase 4 - Assignments

- [ ] Models: Assignment, Submission + migrations
- [ ] Assignment CRUD API (instructor)
- [ ] Submission API (student) + grading API (instructor, grade + feedback)
- [ ] React: assignment list, submit form, grading page
- [ ] Tests: submission uniqueness, grade persistence

## Phase 5 - Progress & Reports

- [ ] Models: LessonCompletion, CourseProgress + migrations
- [ ] Lesson complete API → recompute progress service
- [ ] Student progress dashboard (per-course %)
- [ ] Instructor reports (per-student scores)
- [ ] Admin reports (platform stats: users, enrollments, completion)
- [ ] React: progress bars, report tables, admin dashboard
- [ ] Tests: progress math

## Phase 6 - Polish & Hardening

- [ ] Consistent error JSON + axios 401 interceptor
- [ ] Form validations (frontend + backend)
- [ ] Responsive/mobile-friendly UI pass
- [ ] Motion polish: tune durations/easings, hover/press states on all interactive elements
- [ ] Animated loading states: skeletons, spinners, progress bar fill animations
- [ ] 3D scene budget: lazy chunk size check, dpr clamp, pause on tab hidden, WebGL fallback
- [ ] Reduced-motion audit: verify all animations collapse under `prefers-reduced-motion`
- [ ] Performance budget: landing LCP < 1.5s, Lighthouse score ≥ 90 (Performance/A11y/Best Practices)
- [ ] Seed data script (demo admin/instructor/student, sample course)
- [ ] README setup instructions (run backend + frontend)

## Phase 7 - Deployment (Optional)

- [ ] Collect static, media config
- [ ] gunicorn + Nginx config (serve SPA, proxy /api)
- [ ] docker-compose (postgres + backend + frontend)
- [ ] Production `.env` checklist
