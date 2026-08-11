# LMS Portal - Master TODO

> Ordered build plan. Check off items as completed.

Legend: [ ] = pending, [x] = done

## Phase 0 - Project Setup

- [ ] Create `backend/` Django project (config app, virtualenv)
- [ ] Create `frontend/` React + Vite app
- [ ] Add `requirements.txt` (django, djangorestframework, simplejwt, django-cors-headers, psycopg2, python-dotenv)
- [ ] Add `.env.example` and `.gitignore` (venv, node_modules, .env, media, static)
- [ ] Configure PostgreSQL connection (`lms_db`) + initial migration
- [ ] Install `django-cors-headers`, allow Vite origin
- [ ] Health endpoint `GET /health/`

## Phase 1 - User Management (Auth)

- [ ] Custom User model (email, name, role) + migration
- [ ] Register API (student), Login API (JWT access/refresh)
- [ ] RBAC permissions (`IsInstructorOrAdmin`)
- [ ] Profile endpoint `GET /api/v1/users/me/`
- [ ] Admin: create instructor account endpoint
- [ ] React: login/register pages, AuthContext, route guards
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
- [ ] Seed data script (demo admin/instructor/student, sample course)
- [ ] README setup instructions (run backend + frontend)

## Phase 7 - Deployment (Optional)

- [ ] Collect static, media config
- [ ] gunicorn + Nginx config (serve SPA, proxy /api)
- [ ] docker-compose (postgres + backend + frontend)
- [ ] Production `.env` checklist
