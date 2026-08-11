# LMS Portal - Low Level Design (LLD)

---

## 1. Database Schema (PostgreSQL)

### 1.1 users_user (custom User extends AbstractUser)
| Column     | Type        | Notes                          |
| ---------- | ----------- | ------------------------------ |
| id         | bigserial PK |                                |
| email      | varchar(254) UNIQUE | username field           |
| name       | varchar(255)|                                |
| role       | varchar(10) | ADMIN / INSTRUCTOR / STUDENT  |
| password   | varchar(128)| hashed                         |
| is_active  | boolean     |                                |
| date_joined| timestamptz |                                |

### 1.2 courses_category
| Column | Type        | Notes     |
| ------ | ----------- | --------- |
| id     | bigserial PK|           |
| name   | varchar(100)| UNIQUE    |

### 1.3 courses_course
| Column      | Type        | Notes                              |
| ----------- | ----------- | ---------------------------------- |
| id          | bigserial PK|                                    |
| title       | varchar(255)|                                    |
| description | text        |                                    |
| category    | FK categories | nullable                        |
| instructor  | FK users (role=INSTRUCTOR) | |
| thumbnail   | image field |                                    |
| status      | varchar(10) | DRAFT / PUBLISHED (indexed)        |
| created_at  | timestamptz |                                    |

### 1.4 courses_lesson
| Column     | Type        | Notes                           |
| ---------- | ----------- | ------------------------------- |
| id         | bigserial PK|                                 |
| course     | FK courses (CASCADE) |                     |
| title      | varchar(255)|                                 |
| content    | text        |                                 |
| video_url  | URLField / FileField |                     |
| order      | positiveint | ordering (indexed with course)  |

### 1.5 courses_enrollment
| Column     | Type        | Notes                          |
| ---------- | ----------- | ------------------------------ |
| id         | bigserial PK|                                |
| student    | FK users    | (indexed)                      |
| course     | FK courses  |                                |
| status     | varchar(10) | ACTIVE / COMPLETED             |
| enrolled_at| timestamptz |                                |
| unique_together | (student, course) |                    |

### 1.6 assessments_quiz
| Column     | Type        | Notes                     |
| ---------- | ----------- | ------------------------- |
| id         | bigserial PK|                           |
| course     | FK courses  |                           |
| title      | varchar(255)|                           |
| time_limit_minutes | int, nullable |               |

### 1.7 assessments_question
| Column | Type        | Notes                    |
| ------ | ----------- | ------------------------ |
| id     | bigserial PK|                          |
| quiz   | FK quizzes  |                          |
| text   | text        |                          |
| order  | positiveint |                          |

### 1.8 assessments_option
| Column    | Type       | Notes                          |
| --------- | ---------- | ------------------------------ |
| id        | bigserial PK|                                |
| question  | FK questions|                                |
| text      | varchar(255)|                               |
| is_correct| boolean    | only exposed to instructor     |

### 1.9 assessments_quizattempt
| Column    | Type       | Notes                          |
| --------- | ---------- | ------------------------------ |
| id        | bigserial PK|                                |
| student   | FK users   |                                |
| quiz      | FK quizzes |                                |
| score     | decimal    | auto-computed                  |
| answers   | JSONB      | {question_id: option_id}       |
| submitted_at | timestamptz |                           |
| unique_together | (student, quiz) |                     |

### 1.10 assessments_assignment
| Column   | Type        | Notes                  |
| -------- | ----------- | ---------------------- |
| id       | bigserial PK|                        |
| course   | FK courses  |                        |
| title    | varchar(255)|                        |
| description | text     |                        |
| due_date | timestamptz |                       |

### 1.11 assessments_submission
| Column    | Type        | Notes                |
| --------- | ----------- | -------------------- |
| id        | bigserial PK|                      |
| assignment| FK assignments|                    |
| student   | FK users    |                      |
| content   | text / FileField |                 |
| grade     | decimal, null |                     |
| feedback  | text, null  |                      |
| submitted_at | timestamptz |                   |
| unique_together | (assignment, student) |          |

### 1.12 progress_lessoncompletion
| Column   | Type       | Notes                     |
| -------- | ---------- | ------------------------- |
| id       | bigserial PK|                           |
| student  | FK users   |                           |
| lesson   | FK lessons |                           |
| completed_at | timestamptz |                      |
| unique_together | (student, lesson) |               |

### 1.13 progress_courseprogress (computed snapshot)
| Column      | Type       | Notes                      |
| ----------- | ---------- | -------------------------- |
| id          | bigserial PK|                            |
| student     | FK users   |                            |
| course      | FK courses |                            |
| completed_lessons | int |                      |
| total_lessons | int     |                            |
| percent     | decimal    | computed                   |
| unique_together | (student, course) |              |

---

## 2. Django App Structure

```
backend/
├── manage.py
├── requirements.txt
├── .env / .env.example
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
├── users/
│   ├── models.py        # CustomUser
│   ├── serializers.py   # RegisterSerializer, UserSerializer
│   ├── views.py         # RegisterView, MeView
│   ├── permissions.py   # IsInstructorOrAdmin
├── courses/
│   ├── models.py        # Category, Course, Lesson, Enrollment
│   ├── serializers.py
│   ├── views.py         # CourseViewSet, LessonViewSet, EnrollView
├── assessments/
│   ├── models.py        # Quiz, Question, Option, QuizAttempt, Assignment, Submission
│   ├── services.py      # grade_quiz(), grade_assignment()
│   ├── serializers.py   # QuizAttemptSerializer (hides is_correct)
│   ├── views.py
├── progress/
│   ├── models.py        # LessonCompletion, CourseProgress
│   ├── services.py      # recompute_course_progress()
│   ├── views.py         # ProgressView, ReportView
```

---

## 3. Key Classes & Responsibilities

### users.permissions
```python
class IsInstructorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated
                    and user.role in (ROLE_ADMIN, ROLE_INSTRUCTOR))
```

### assessments.services.grade_quiz
```python
def grade_quiz(attempt, answers: dict) -> Decimal:
    total = attempt.quiz.questions.count()
    correct = 0
    for q in attempt.quiz.questions.all():
        given = answers.get(str(q.id))
        if given and Option.objects.filter(id=given, question=q, is_correct=True).exists():
            correct += 1
    return (correct / total * 100) if total else 0
```

### progress.services.recompute_course_progress
```python
def recompute_course_progress(student, course):
    total = course.lessons.count()
    done = LessonCompletion.objects.filter(student=student, lesson__course=course).count()
    CourseProgress.objects.update_or_create(
        student=student, course=course,
        defaults={'completed_lessons': done, 'total_lessons': total,
                  'percent': (done / total * 100) if total else 0})
```

---

## 4. React Component Tree (Highlights)

```
App
└── AuthProvider
    ├── PublicRoutes
    │   ├── HomePage ── CourseCatalog ── CourseCard
    │   ├── LoginPage / RegisterPage
    │   └── CourseDetailPage ── EnrollButton
    ├── StudentRoutes (ProtectedRoute role=STUDENT)
    │   ├── Dashboard ── MyCourses ── CourseCard
    │   ├── LearnPage ── Sidebar(lesson list) ── LessonViewer ── CompleteButton
    │   ├── QuizPage ── QuizPlayer ── ResultBanner
    │   ├── AssignmentsPage ── AssignmentList ── SubmitForm
    │   └── ProgressPage ── ProgressBar ── ScoreTable
    ├── InstructorRoutes (ProtectedRoute role=INSTRUCTOR)
    │   ├── CourseFormPage / LessonFormPage / QuizFormPage / AssignmentFormPage
    │   └── GradingPage ── SubmissionsTable ── GradeForm
    └── AdminRoutes (ProtectedRoute role=ADMIN)
        ├── UserManagementPage
        ├── CourseOverviewPage
        └── ReportsPage ── StatsCards ── ReportsTable
```

---

## 5. API Contract Example (JSON)

### POST /api/v1/courses/{id}/enroll/
Request: `{}`
Response 201:
```json
{ "id": 12, "course": 3, "student": 7, "status": "ACTIVE" }
```

### POST /api/v1/quizzes/{id}/attempt/
Request:
```json
{ "answers": { "101": 402, "102": 405 } }
```
Response 200:
```json
{ "score": 83.33, "total_questions": 6, "correct": 5 }
```

---

## 6. Error Handling

- DRF default exception handler + custom handler returning consistent JSON:
```json
{ "error": { "code": "permission_denied", "message": "..." } }
```
- Frontend axios interceptor: 401 → refresh token → retry; on fail → redirect `/login`.

---

## 7. Tests (Pytest)

- `users`: register, login, token refresh, role permissions.
- `courses`: CRUD permissions, enrollment unique, publish gating.
- `assessments`: quiz auto-grade math, submission grade.
- `progress`: completion recompute math.
- `frontend`: vitest for auth context, quiz player, progress bars.
