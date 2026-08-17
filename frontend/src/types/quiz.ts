export interface Quiz {
  id: number;
  title: string;
  description: string;
  time_limit_minutes: number | null;
  course: number;
  course_title: string;
  questions_count: number;
  created_at: string;
}

export interface Question {
  id: number;
  text: string;
  order: number;
  options: Option[];
}

export interface Option {
  id: number;
  text: string;
  order: number;
}

export interface QuizAttempt {
  id: number;
  quiz: number;
  score: number;
  answers: Record<string, number>;
  submitted_at: string;
}

export interface QuizAttemptSubmit {
  answers: Record<string, number>;
}
