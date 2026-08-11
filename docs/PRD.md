# LMS Portal - Product Requirements Document (PRD)

| Item           | Detail                                     |
| -------------- | ------------------------------------------ |
| Product        | LMS Portal                                 |
| Version        | 1.0                                        |
| Status         | Draft                                      |
| Stack          | React.js / Django (Python) / PostgreSQL    |

---

## 1. Overview

LMS Portal is a learning management system that connects **Admin**, **Instructor**, and **Student** users. It provides course management, lesson delivery (video/content), quizzes, assignments, and progress tracking in one simple, student-friendly platform.

## 2. Goals

- Provide a simple and student-friendly learning experience.
- Allow instructors to create and manage courses, lessons, quizzes, and assignments.
- Allow students to enroll, learn, submit work, and track progress.
- Give admins full control over users, content, and reports.

## 3. Target Users

| Role         | Description                                   |
| ------------ | --------------------------------------------- |
| Admin        | Manages platform, users, content, and reports |
| Instructor   | Creates courses, lessons, quizzes, assignments |
| Student      | Enrolls in courses, learns, takes quizzes, submits assignments, tracks progress |

## 4. Functional Requirements

### FR-1 User Management
- FR-1.1 Registration: student can register with name, email, password.
- FR-1.2 Login / Logout (JWT-based).
- FR-1.3 Roles: Admin, Instructor, Student.
- FR-1.4 Admin can create/manage instructor accounts.
- FR-1.5 Profile view & edit (name, email, password change).

### FR-2 Course Management
- FR-2.1 Admin/Instructor can create, edit, delete courses.
- FR-2.2 Course fields: title, description, category, thumbnail, status (draft/published).
- FR-2.3 Students can browse and search published courses.

### FR-3 Lesson Management
- FR-3.1 Instructor can create lessons inside a course.
- FR-3.2 Lesson fields: title, content (text), video URL/file, order.
- FR-3.3 Students can view lessons after enrollment.
- FR-3.4 Mark lesson as completed (drives progress).

### FR-4 Quiz & Assignment
- FR-4.1 Instructor can create quizzes with multiple-choice questions.
- FR-4.2 Auto-grading of quizzes.
- FR-4.3 Instructor can create assignments with due dates.
- FR-4.4 Students can submit assignments; instructor grades them.

### FR-5 Progress Tracking
- FR-5.1 Track lesson completion percentage per course.
- FR-5.2 Track quiz scores.
- FR-5.3 Show report/analytics: per student, per course.
- FR-5.4 Admin dashboard with platform-wide stats.

## 5. Non-Functional Requirements

- **Security**: Passwords hashed (Django PBKDF2/bcrypt), JWT auth, role-based access control (RBAC).
- **Performance**: Page load < 2s, API responses < 500ms under normal load.
- **Scalability**: Stateless API; DB connection pooling; index on frequently queried fields.
- **Usability**: Mobile-friendly responsive React UI.
- **Reliability**: Validations on both frontend and backend; friendly error messages.

## 6. Out of Scope (v1)

- Payments / subscriptions
- Live classes / video conferencing
- Mobile apps
- Email notifications (deferred)

## 7. Success Metrics

- Students enroll and complete courses (completion rate > 60%).
- Instructor content creation active monthly.
- Zero critical bugs in auth and grading flows.

## 8. Assumptions & Dependencies

- PostgreSQL is available.
- Media storage (videos/thumbnails) on local filesystem (S3 later).
- Single language (English) UI.
