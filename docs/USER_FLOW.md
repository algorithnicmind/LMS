# LMS Portal - User Flow

---

## 1. Guest / Public Flow

```
Start
  │
  ├─ Visit Home → Browse course catalog
  ├─ View course details
  │     └─ "Enroll" → Redirect to Login (or Register)
  ├─ Login ──────────────┐
  └─ Register (Student) ─┘
          │
          ▼
      Enter Dashboard
```

## 2. Authentication Flow

```
Register:
  Name + Email + Password → Validate → Create Student → Auto-login → Dashboard

Login:
  Email + Password → Validate credentials → Issue JWT (access+refresh)
  → Store in localStorage → Redirect by role
```

Role redirects:
- Student → Student Dashboard
- Instructor → Instructor Dashboard
- Admin → Admin Dashboard

## 3. Student Flow

```
Dashboard
  ├─ Browse / Search Courses
  │     └─ Course Details → Enroll
  ├─ My Courses → Select course → Learn
  │     └─ Lesson list → Watch/read lesson → Mark Complete
  │           └─ Progress % updates
  ├─ Quizzes → Take Quiz → Submit → Instant auto-grade + score
  ├─ Assignments → View → Submit work → Wait for grade
  └─ Progress → Completion %, quiz scores, grades report
```

## 4. Instructor Flow

```
Login as Instructor → Instructor Dashboard
  ├─ Courses → Create/Edit/Delete course → Publish
  ├─ Course detail → Manage lessons (add/edit/reorder/delete)
  │     └─ Add quiz → Add questions & options
  ├─ Assignments → Create with due date
  ├─ Submissions → View student submissions → Grade → Feedback
  └─ Reports → Student progress for their courses
```

## 5. Admin Flow

```
Login as Admin → Admin Dashboard
  ├─ Users → View all / Create instructor / Deactivate user
  ├─ Courses → View all, edit/delete any content
  ├─ Reports → Platform stats (users, enrollments, completion)
  └─ Content moderation
```

## 6. Cross-Cutting Flows

### Enrollment
```
Course detail → POST /enroll → check auth → create Enrollment(active)
→ Student sees course under "My Courses" → lessons unlocked
```

### Quiz Attempt
```
Open quiz → Questions fetched → Submit answers
→ Backend auto-grades → QuizAttempt stored → Score returned → saved to progress
```

### Assignment Submission
```
Assignment detail → Upload/submit text → POST /submit
→ Instructor sees in Submissions → Grade + feedback → Student notified on dashboard
```

### Lesson Completion → Progress
```
Lesson view → Mark Complete → POST /complete
→ progress service recomputes CourseProgress = completed lessons / total lessons
```
