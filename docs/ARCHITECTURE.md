# LMS Portal - Architecture Diagram

> Production-Grade: Security, Performance, Observability, Scalability

## Tech Stack (Chosen)

| Layer                  | Technology                                                              | Purpose |
| ---------------------- | ----------------------------------------------------------------------- | ------- |
| **Frontend Framework** | React 19 + TypeScript                                                   | Concurrent features, strict typing |
| **Build Tool**         | Vite 8                                                                  | Fast HMR, optimized production builds |
| **Styling**            | Tailwind CSS v4                                                         | Zero-runtime, JIT, design tokens |
| **Animation**          | Framer Motion 13                                                        | Declarative, WAAPI, reduced-motion |
| **3D**                 | React Three Fiber + Drei + Three.js                                     | React-native Three.js, tree-shakable |
| **State (Server)**     | TanStack Query (React Query)                                            | Caching, deduping, retries, prefetch |
| **State (Client)**     | Zustand                                                                 | Minimal, typed UI state |
| **Forms**              | React Hook Form + Zod                                                   | Performant, schema validation shared |
| **UI Primitives**      | shadcn/ui (Radix UI + Tailwind)                                         | Accessible, copy-paste, no runtime dep |
| **Backend**            | Django 6.1 + DRF + SimpleJWT                                            | Mature, secure, batteries-included |
| **Database**           | PostgreSQL (Neon serverless)                                            | ACID, JSONB, scaling |
| **Auth Tokens**        | httpOnly cookies (access 15m, refresh 7d, rotating)                     | Secure, CSRF-protected |
| **Rate Limiting**      | django-ratelimit / django-axes                                          | Auth endpoint protection |
| **Error Tracking**     | Sentry (frontend + backend)                                             | Source maps, release tracking |
| **Perf Monitoring**    | Web Vitals + Sentry/DataDog                                             | LCP, INP, CLS |
| **Testing**            | Vitest + Playwright + pytest                                            | Unit, E2E, backend |
| **CI/CD**              | GitHub Actions (lint, typecheck, test, build, security, deploy)         | Automated quality gates |

## Users

- **Admin**
- **Instructor**
- **Student**

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
