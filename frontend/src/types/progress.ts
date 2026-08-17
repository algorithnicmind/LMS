export interface LessonCompletion {
  id: number;
  lesson: number;
  lesson_title: string;
  completed_at: string;
}

export interface CourseProgress {
  id: number;
  course: number;
  course_title: string;
  course_thumbnail: string | null;
  completed_lessons: number;
  total_lessons: number;
  percent: number;
  updated_at: string;
}

export interface PlatformStats {
  total_users: number;
  total_students: number;
  total_instructors: number;
  total_courses: number;
  total_enrollments: number;
  avg_completion_rate: number;
}
