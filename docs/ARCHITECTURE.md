# LMS Portal - Basic Architecture Diagram

> Frontend + Backend + Database (Simple & Student Friendly)

## Tech Stack (Chosen)

| Layer      | Technology                          |
| ---------- | ----------------------------------- |
| Frontend   | React.js + Tailwind CSS + Framer Motion + Three.js (R3F) |
| Backend    | Python - Django                     |
| Database   | PostgreSQL                          |

## Users

- **Admin**
- **Instructor**
- **Student**

## Frontend (User Interface)

- Built with **React.js** (HTML / CSS / JavaScript)
- Styling: **Tailwind CSS** (design system, utility-first)
- Animations: **Framer Motion** (page transitions, scroll reveals, micro-interactions)
- 3D: **Three.js + React Three Fiber** (animated 3D hero background on landing page)
- What Users Do:
  - Landing page (animated UI + animated 3D background)
  - Register / Login (animated sign-in page)
  - View Courses
  - Watch Lessons
  - Take Quizzes
  - Submit Assignments
  - Track Progress
- Role-based access control (RBAC) enforced at the route level:
  - Guest → Landing, Login, Register, Catalog
  - Student → Dashboard, Learn, Quizzes, Assignments, Progress
  - Instructor → Course/Lesson/Quiz/Assignment management, Grading
  - Admin → User management, platform reports

## Backend (Server Logic)

- Built with **Python - Django** (Django REST Framework for APIs)
- What Backend Does:
  - Handle Requests
  - User Authentication
  - Course Management
  - Lesson Management
  - Assignments & Quiz Logic
  - Store / Fetch Data from DB

## Database (Data Storage)

- Built with **PostgreSQL**
- Stores All Data:
  - Users (Students, Instructors, Admins)
  - Courses
  - Lessons
  - Quizzes
  - Assignments
  - Progress / Results

## Core Features of LMS Portal

1. **User Management** (Students, Instructors, Admins)
2. **Course Management** (Create & Manage Courses)
3. **Lesson Management** (Upload & Watch Lessons)
4. **Quiz & Assignment** (Evaluate Students)
5. **Progress Tracking** (Reports & Analytics)

## How It Works (Flow)

1. User lands on animated landing page (3D background via Three.js/R3F, motion UI via Framer Motion)
2. User signs in (animated auth page) → JWT issued → RBAC redirects by role
3. User interacts with UI (React.js)
4. Frontend sends request to Backend (Django REST API over HTTP/JSON)
5. Backend verifies JWT + role permissions, processes the request
6. Backend fetches / stores data in Database (PostgreSQL)
7. Response sent back to Frontend
