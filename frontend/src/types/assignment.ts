export interface Assignment {
  id: number;
  title: string;
  description: string;
  due_date: string;
  max_points: number;
  course: number;
  course_title: string;
  created_at: string;
}

export interface Submission {
  id: number;
  assignment: number;
  student: number;
  student_name: string;
  content: string;
  file: string | null;
  grade: number | null;
  feedback: string;
  submitted_at: string;
  graded_at: string | null;
}
