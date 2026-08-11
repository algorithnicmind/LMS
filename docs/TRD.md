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

### 1.2 Pages / Routes
| Route                    | Access | Purpose                          |
| ------------------------ | ------ | -------------------------------- |
| `/`                      | Public | Home / course catalog            |
| `/login`                 | Public | Login                            |
| `/register`              | Public | Student registration             |
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
- `CourseCard`, `LessonViewer`, `QuizPlayer`, `AssignmentForm`.
- `ProgressBar`, `ReportsTable`.

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
