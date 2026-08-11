# LMS Portal - Wireframes (Low-Fidelity)

> ASCII wireframes for key screens. React components map 1:1 to these blocks.

---

## 1. Landing Page `/`

```
┌────────────────────────────────────────────────────┐
│ [Logo] LMS Portal   Features  Courses  [Login][Sign│
│                                             Up]    │
├────────────────────────────────────────────────────┤
│  ◄── 3D ANIMATED BACKGROUND (Three.js) ──►         │
│  ┌──────────────────────────────────────────────┐  │
│  │   Learn Anything,                          │  │
│  │   Anytime, Anywhere.                       │  │
│  │   [Explore Courses]  [Create Account]      │  │
│  │   (staggered text reveal, glow CTAs)       │  │
│  └──────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────┤
│  Stats (animated counters):                        │
│  ▓ 120+ Courses   ▓ 5k Students   ▓ 98% Complete   │
├────────────────────────────────────────────────────┤
│  Features (scroll-reveal cards):                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Video    │ │ Quizzes  │ │ Progress │           │
│  │ Lessons  │ │ Auto-    │ │ Reports  │           │
│  │          │ │ graded   │ │          │           │
│  └──────────┘ └──────────┘ └──────────┘           │
├────────────────────────────────────────────────────┤
│  Popular Courses (motion cards)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │ Python   │ │ Django   │ │ React    │           │
│  │ ★★★★★   │ │ ★★★★    │ │ ★★★★    │           │
│  └──────────┘ └──────────┘ └──────────┘           │
├────────────────────────────────────────────────────┤
│  Footer                                            │
└────────────────────────────────────────────────────┘
```

**Animation notes:** hero text staggered reveal on load · 3D scene moves subtly on mouse move · stats count up on scroll into view · feature cards slide/fade in · course cards lift on hover.

## 2. Sign In / Register (Animated)

```
┌────────────────────────────────────────────────────┐
│ ◄─ AnimatedBackground (gradient/particles) ─►      │
│  ┌───────────────────────────┐  (card: scale+fade  │
│  │  Welcome back!            │   enter)            │
│  │ ┌───────────────────────┐ │                    │
│  │ │ Email [____________]  │ │ (focus ring glow)  │
│  │ │ Password [_________]  │ │ (error shake)      │
│  │ │ [Sign In →]           │ │ (loading spinner)  │
│  │ │ New here? [Register]  │ │                    │
│  │ └───────────────────────┘ │                    │
│  └───────────────────────────┘                    │
└────────────────────────────────────────────────────┘

RBAC: success → animated redirect to role dashboard
  Student → /dashboard · Instructor → /instructor · Admin → /admin
```

## 3. Course Catalog `/courses`

```
┌────────────────────────────────────────────────────┐
│ [Logo] LMS Portal      Search [____]  [Login] [Reg]│
├────────────────────────────────────────────────────┤
│  Courses                                            │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│ │ [thumb]  │ │ [thumb]  │ │ [thumb]  │             │
│ │ Python 101│ │ Django  │ │ Math     │             │
│ │ ★★★★★    │ │ ★★★★    │ │ ★★★     │             │
│ │ [View]   │ │ [View]   │ │ [View]   │             │
│ └──────────┘ └──────────┘ └──────────┘            │
│ ┌──────────┐ ┌──────────┐                          │
│ │ [thumb]  │ │ [thumb]  │                          │
│ │ React    │ │ SQL      │                          │
│ │ ★★★★    │ │ ★★★★    │                          │
│ │ [View]   │ │ [View]   │                          │
│ └──────────┘ └──────────┘                          │
└────────────────────────────────────────────────────┘
```

## 4. Course Detail (Student, enrolled)

```
┌────────────────────────────────────────────────────┐
│ < Back        Course: Python 101      [My Courses] │
├────────────────────────────┬───────────────────────┤
│ [Thumbnail / Intro video]  │ Lessons               │
│ Title + Description        │  1. Intro        ✓    │
│ Instructor: Jane           │  2. Setup        ✓    │
│                            │  3. Variables   ▶    │
│ Progress ▓▓▓▓░░░░ 40%      │  4. Loops             │
│ [Take Quiz] [Assignment]   │  5. Functions         │
│ [Resume Lesson]            │                       │
└────────────────────────────┴───────────────────────┘
```

## 5. Lesson Player

```
┌────────────────────────────────────────────────────┐
│ < Course             Lesson 3/5: Variables  [Done] │
├────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────┐  │
│  │                                              │  │
│  │               VIDEO / CONTENT                │  │
│  │                                              │  │
│  └──────────────────────────────────────────────┘  │
│  [◀ Previous]                      [Next ▶]       │
└────────────────────────────────────────────────────┘
```

## 5. Quiz Player

```
┌────────────────────────────────────────────────────┐
│ Quiz: Variables Basics          Q 2 of 5            │
├────────────────────────────────────────────────────┤
│ Which keyword defines a variable?                   │
│  ( ) var      ( ) def      ( ) x = 5  ( ) import   │
│                                                     │
│                  [Submit Quiz]                      │
├────────────────────────────────────────────────────┤
│  [Cancel]                                           │
└────────────────────────────────────────────────────┘

--- After submit: ---
│ Score: 80%  (4/5 correct)   [Back to Course]       │
```

## 6. Student Dashboard

```
┌────────────────────────────────────────────────────┐
│ [Logo]  Hi, Alex ▼            [Logout]             │
├────────────────────────────────────────────────────┤
│  My Courses               Assignments: 2 due        │
│ ┌──────────┐ ┌──────────┐  ┌────────────────────┐  │
│ │ Python  │ │ Django   │  │ SQL Basics - Due Fri│  │
│ │ ▓▓▓░░ 50%│ │ ▓▓▓▓▓ 90%│  │ [Open]             │  │
│ │ [Learn] │ │ [Learn]  │  │ Math HW - Due Mon   │  │
│ └──────────┘ └──────────┘  │ [Open]             │  │
│  Quiz scores: 88, 100      └────────────────────┘  │
│  Overall progress: 65%                              │
└────────────────────────────────────────────────────┘
```

## 7. Instructor - Course Management

```
┌────────────────────────────────────────────────────┐
│ Instructor Panel   [+ New Course]   [Reports]      │
├────────────────────────────────────────────────────┤
│ Course: Django Masterclass  [Edit] [Publish]      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Lessons:                                     │  │
│  │  1. Intro               [↑][↓][Edit][Del]    │  │
│  │  2. Models              [↑][↓][Edit][Del]    │  │
│  │  3. Views               [↑][↓][Edit][Del]    │  │
│  │  [+ Add Lesson]                             │  │
│  ├──────────────────────────────────────────────┤  │
│  │ Quizzes: [Add]  Assignments: [Add]          │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────┘
```

## 8. Instructor - Grading

```
┌────────────────────────────────────────────────────┐
│ Submissions - Assignment: SQL Basics                │
├────────────────────────────────────────────────────┤
│ Student     Submitted     Grade  Feedback  [Action]│
│ Alex        2 days ago    90    Great job  [Edit]  │
│ Priya       yesterday     75    Good      [Edit]   │
│ Sam         today         –      –         [Grade] │
└────────────────────────────────────────────────────┘
```

## 9. Admin Dashboard

```
┌────────────────────────────────────────────────────┐
│ Admin Panel        Users | Courses | Reports       │
├────────────────────────────────────────────────────┤
│  Stats:                                           │
│  Students 120  Instructors 8  Courses 25           │
│  Enrollments 340  Avg completion 61%               │
├────────────────────────────────────────────────────┤
│  Users table: [search]                            │
│  Name        Email            Role      Status    │
│  Jane Doe    jane@lms.io      Instructor Active   │
│  Alex Smith  alex@lms.io      Student   Active   │
│  ...                                              │
└────────────────────────────────────────────────────┘
```

## 10. Mobile (Responsive) - Catalog

```
┌──────────────┐
│ LMS  [☰]    │
├──────────────┤
│ [thumb]      │
│ Python 101   │
│ ★★★★★       │
│ [View]       │
│ [thumb]      │
│ Django       │
│ ★★★★        │
│ [View]       │
└──────────────┘
```

---

## Wireframe → Page Mapping

| Screen                | Route                 | Wireframe |
| --------------------- | --------------------- | --------- |
| Landing (animated)    | `/`                   | 1, 10     |
| Login / Register (animated) | `/login`, `/register` | 2     |
| Catalog               | `/courses`            | 3         |
| Course Detail         | `/courses/:id`        | 4         |
| Lesson Player         | `/courses/:id/learn`  | 5         |
| Quiz                  | `/courses/:id/quiz/:qid` | 6      |
| Student Dashboard     | `/dashboard`          | 7         |
| Instructor Course Mgmt | `/instructor/courses/:id` | 8     |
| Grading               | `/instructor/grading` | 9         |
| Admin Dashboard       | `/admin`              | 10        |
