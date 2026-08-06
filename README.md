<<<<<<< HEAD
# LMS - Learning Management System

Learning Management System (LMS) is a comprehensive platform for managing and delivering educational courses, assessments, and progress tracking. It serves as a bridge between instructors and learners, providing tools for creating, enrolling in, and completing courses.

## 🚀 Features

### For Learners
- **Course Discovery**: Browse and search available courses.
- **Enrollment**: Easily enroll in courses that match your interests and goals.
- **Progress Tracking**: Monitor your course completion status.
- **Access Materials**: View course content including videos, documents, and other resources.

### For Instructors
- **Course Creation**: Create and manage course content with ease.
- **Structure Management**: Organize courses into modules and lessons.
- **Content Delivery**: Upload and manage various types of course materials.

## 🛠️ Tech Stack

### Backend
- **Language**: Java (Version 17)
- **Framework**: Spring Boot
- **Database**: PostgreSQL
- **Security**: Spring Security with JWT (JSON Web Tokens)
- **Documentation**: Springdoc OpenAPI (Swagger UI)

### Frontend
- **Framework**: Angular (Version 16)
- **UI Components**: Angular Material
- **State Management**: NgRx
- **HTTP Client**: Angular HttpClient Module
- **Build Tool**: Angular CLI

## 📂 Project Structure

### Backend (`backend`)
```
backend/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/lms/
│   │   │       ├── config/        # Security and Configuration
│   │   │       ├── controller/    # REST API Controllers
│   │   │       ├── dto/         # Data Transfer Objects
│   │   │       ├── exception/     # Custom Exception Handling
│   │   │       ├── model/         # JPA Entities
│   │   │       ├── repository/    # Spring Data Repositories
│   │   │       ├── service/       # Business Logic
│   │   │       └── LmsApplication.java  # Main Application Class
│   │   └── resources/
│   │       ├── application.properties  # Application Configuration
│   │       └── schema-postgres.sql   # Database Schema
│   └── test/
└── pom.xml
```

### Frontend (`frontend`)
```
frontend/
├── src/
│   ├── app/
│   │   ├── core/
│   │   │   ├── auth/             # Authentication Module
│   │   │   ├── interceptors/     # HTTP Interceptors (JWT)
│   │   │   └── services/       # API Services
│   │   ├── features/             # Feature Modules
│   │   │   ├── courses/          # Course Management
│   │   │   ├── dashboard/        # Dashboard Views
│   │   │   └── layout/           # UI Layout Components
│   │   ├── shared/               # Shared Components
│   │   ├── app.component.ts
│   │   ├── app.module.ts
│   │   ├── app-routing.module.ts
│   │   └── store/                # NgRx Store
│   ├── environments/           # Environment Configurations
│   └── assets/
└── package.json
```

## 📦 Prerequisites

- **Java 17** or higher
- **Maven 3.6** or higher
- **Node.js 16** or higher
- **npm** (comes with Node.js)
- **PostgreSQL** Database

## 🚀 Getting Started

### 1. Backend Setup

1.  **Clone the repository** (if you haven't already).
2.  **Database Setup**:
    -   Ensure PostgreSQL is running.
    -   Create a database named `lms_db` (or update `application.properties`).
    -   Run the schema script: `src/main/resources/schema-postgres.sql`
3.  **Build the project**:
    ```bash
    cd backend
    mvn clean package
    ```
4.  **Run the application**:
    ```bash
    mvn spring-boot:run
    ```
    -   The API will be available at `http://localhost:8080`.
    -   Swagger UI: `http://localhost:8080/swagger-ui.html`

### 2. Frontend Setup

1.  **Navigate to the frontend directory**:
    ```bash
    cd frontend
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Run the application**:
    ```bash
    npm start
    ```
    -   The application will open at `http://localhost:4200`.

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Register

### Courses
- `GET /api/courses` - Get all courses
- `GET /api/courses/{id}` - Get course by ID
- `POST /api/courses` - Create a new course
- `PUT /api/courses/{id}` - Update course
- `DELETE /api/courses/{id}` - Delete course

### Enrollments
- `POST /api/enrollments` - Enroll in a course
- `GET /api/enrollments/user/{userId}` - Get user's enrollments

### Modules
- `GET /api/courses/{courseId}/modules` - Get modules for a course
- `POST /api/modules` - Create a new module

## 🔐 Security

The application uses JWT-based authentication.
- **Roles**: `STUDENT`, `INSTRUCTOR`
- **Endpoints**: Some endpoints require authentication (check Swagger UI).

## 🤝 Contributing

1.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
2.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
3.  Push to the branch (`git push origin feature/AmazingFeature`).
4.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.   
=======
# LMS

Make it a private repository
>>>>>>> b5b821176c648685f118f0af0f95436c732290e0

