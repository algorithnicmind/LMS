export interface Category {
  id: number;
  name: string;
  created_at: string;
}

export interface Course {
  id: number;
  title: string;
  description: string;
  thumbnail: string | null;
  status: 'DRAFT' | 'PUBLISHED' | 'ARCHIVED';
  category: number | null;
  category_name: string | null;
  instructor: number;
  instructor_name: string;
  lessons_count: number;
  created_at: string;
  updated_at?: string;
}

export interface CourseDetail extends Course {
  lessons: Lesson[];
}

export interface Lesson {
  id: number;
  title: string;
  content: string;
  video_url: string;
  order: number;
}

export interface Enrollment {
  id: number;
  course: number;
  course_title: string;
  status: 'ACTIVE' | 'COMPLETED' | 'DROPPED';
  enrolled_at: string;
  completed_at: string | null;
}
