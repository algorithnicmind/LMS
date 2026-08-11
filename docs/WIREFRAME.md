# LMS Portal - Wireframes (Low-Fidelity)

> ASCII wireframes for key screens. React components map 1:1 to these blocks.

---

## 1. Home / Course Catalog `/`

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

## 2. Login / Register

```
┌───────────────────────────┐
│  LMS Portal               │
│ ┌───────────────────────┐ │
│ │ Email [____________]  │ │
│ │ Password [_________]  │ │
│ │ [Sign In]             │ │
│ │ New here? [Register]  │ │
│ └───────────────────────┘ │
└───────────────────────────┘
```

## 3. Course Detail (Student, enrolled)

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

## 4. Lesson Player

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
| Catalog               | `/`                   | 1, 10     |
| Login / Register      | `/login`, `/register` | 2         |
| Course Detail         | `/courses/:id`        | 3         |
| Lesson Player         | `/courses/:id/learn`  | 4         |
| Quiz                  | `/courses/:id/quiz/:qid` | 5      |
| Student Dashboard     | `/dashboard`          | 6         |
| Instructor Course Mgmt | `/instructor/courses/:id` | 7     |
| Grading               | `/instructor/grading` | 8         |
| Admin Dashboard       | `/admin`              | 9         |
