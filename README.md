# LMS - Learning Management System

Learning Management System (LMS) is a comprehensive platform for managing and delivering educational courses, assessments, and progress tracking. It serves as a bridge between instructors and learners, providing tools for creating, enrolling in, and completing courses.

## 🚀 Features

### For Learners
- **Course Discovery**: Browse and search available courses.
- **Enrollment**: Easily enroll in courses that match your interests and goals.
- **Progress Tracking**: Monitor your course completion status.
- **Access Materials**: View course content including videos, documents, and other resources.
- **Quizzes & Assignments**: Take auto-graded quizzes and submit assignments.

### For Instructors
- **Course Creation**: Create and manage course content with ease.
- **Structure Management**: Organize courses into modules and lessons.
- **Content Delivery**: Upload and manage various types of course materials.
- **Assessment & Grading**: Create quizzes and assignments, grade student submissions.

### For Admins
- **User Management**: Create instructor accounts, manage all users.
- **Platform Reports**: Platform-wide analytics on users, enrollments, and completion.

## 🛠️ Tech Stack

| Layer      | Technology                        |
| ---------- | --------------------------------- |
| Frontend   | React.js (Vite)                   |
| Backend    | Python - Django (DRF, JWT)        |
| Database   | PostgreSQL                        |

## 📚 Documentation

| Document                    | Description                          |
| --------------------------- | ------------------------------------ |
| [ARCHITECTURE](docs/ARCHITECTURE.md) | Base architecture spec        |
| [PRD](docs/PRD.md)          | Product Requirements Document        |
| [TRD](docs/TRD.md)          | Technical Requirements Document      |
| [USER_FLOW](docs/USER_FLOW.md) | User flows per role              |
| [HLD](docs/HLD.md)          | High Level Design                    |
| [LLD](docs/LLD.md)          | Low Level Design (schema, classes)   |
| [MASTER_TODO](docs/MASTER_TODO.md) | Ordered build plan            |
| [WIREFRAME](docs/WIREFRAME.md) | Low-fidelity screen wireframes     |

## 📂 Planned Project Structure

```
backend/        # Django (users, courses, assessments, progress apps)
frontend/       # React + Vite SPA
docs/           # Project documentation
```

## 📦 Prerequisites

- **Python 3.10+**
- **Node.js 18+** and npm
- **PostgreSQL** (database `lms_db`)

## 🚀 Getting Started

1. Clone the repository.
2. Follow [docs/MASTER_TODO.md](docs/MASTER_TODO.md) build plan.
3. Backend: `cd backend && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver`
4. Frontend: `cd frontend && npm install && npm run dev`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
