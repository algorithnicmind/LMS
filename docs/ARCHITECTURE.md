# LMS Portal - Basic Architecture Diagram

> Frontend + Backend + Database (Simple & Student Friendly)

## Tech Stack (Chosen)

| Layer      | Technology        |
| ---------- | ----------------- |
| Frontend   | React.js          |
| Backend    | Python - Django   |
| Database   | PostgreSQL        |

## Users

- **Admin**
- **Instructor**
- **Student**

## Frontend (User Interface)

- Built with **React.js** (HTML / CSS / JavaScript)
- What Users Do:
  - Register / Login
  - View Courses
  - Watch Lessons
  - Take Quizzes
  - Submit Assignments
  - Track Progress

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

1. User interacts with UI (React.js)
2. Frontend sends request to Backend (Django REST API over HTTP/JSON)
3. Backend processes the request
4. Backend fetches / stores data in Database (PostgreSQL)
5. Response sent back to Frontend
