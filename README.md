# LMS_DJANGO - Learning Management System

A full-featured Learning Management System (LMS) built with Django REST Framework backend and React frontend, designed for online education platforms.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Database Schema](#database-schema)
- [API Documentation](#api-documentation)
- [Installation](#installation)
- [Configuration](#configuration)
- [Features](#features)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview

LMS_DJANGO is a comprehensive Learning Management System that enables:
- **Students** to browse, enroll in courses, track progress, and earn certificates
- **Instructors** to create and manage courses, assessments, and track student performance
- **Administrators** to manage users, courses, and platform analytics

The system supports course management, quizzes, assignments, reviews, certificates, real-time chat, and detailed analytics.

## Architecture

```
LMS_DJANGO/
├── lms_api/                      # Backend API (Django REST Framework)
│   ├── lms_backend/              # Django project configuration
│   │   ├── settings.py           # Project settings
│   │   ├── urls.py               # Main URL routing
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── users/                    # User management & authentication
│   │   ├── models.py             # Custom User model (AbstractUser)
│   │   ├── views.py              # User ViewSets
│   │   ├── auth_views.py         # JWT authentication endpoints
│   │   ├── serializers.py        # User serializers
│   │   └── urls.py
│   │
│   ├── courses/                  # Course management
│   │   ├── models.py             # Course, Section, Lesson models
│   │   ├── views.py              # Public course views
│   │   ├── teacher_views.py      # Teacher course management
│   │   ├── serializers.py        # Course serializers
│   │   └── urls.py
│   │
│   ├── enrollments/              # Course enrollment & progress
│   │   ├── models.py             # Enrollment, LessonProgress, Certificate, Cart, Payment
│   │   ├── views.py              # Enrollment management
│   │   ├── cart_views.py         # Shopping cart functionality
│   │   ├── serializers.py        # Enrollment serializers
│   │   └── urls.py
│   │
│   ├── assessments/              # Quizzes & assignments
│   │   ├── models.py             # Quiz, Question, Choice, Assignment, Submission
│   │   ├── views.py              # Quiz & assignment views
│   │   ├── serializers.py        # Assessment serializers
│   │   └── urls.py
│   │
│   ├── reviews/                  # Course reviews & ratings
│   │   ├── models.py             # CourseReview model
│   │   ├── views.py              # Review endpoints
│   │   ├── serializers.py        # Review serializers
│   │   └── urls.py
│   │
│   ├── analytics/                # Analytics & statistics
│   │   ├── views.py              # Teacher analytics endpoints
│   │   ├── serializers.py        # Analytics serializers
│   │   └── urls.py
│   │
│   ├── chat/                     # Real-time messaging
│   │   ├── models.py             # Conversation, Message models
│   │   ├── views.py              # Chat endpoints
│   │   ├── serializers.py        # Chat serializers
│   │   └── urls.py
│   │
│   ├── common/                   # Shared utilities
│   │   └── permissions.py        # Custom permissions (IsTeacher, IsOwnerOrReadOnly)
│   │
│   ├── media/                    # User-uploaded files
│   ├── manage.py
│   └── .env.example
│
└── lms_frontend/                 # Frontend (React + Vite + TailwindCSS)
    ├── src/
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── postcss.config.js
```

## Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| Django | 5.2.7 | Web framework |
| Django REST Framework | 3.16.1 | RESTful API |
| SimpleJWT | 5.5.1 | JWT authentication |
| MySQL | - | Primary database |
| django-cors-headers | 4.9.0 | CORS handling |
| python-dotenv | 1.0.0 | Environment management |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.2.0 | UI library |
| React Router DOM | 6.20.0 | Client-side routing |
| Axios | 1.6.2 | HTTP client |
| Vite | 5.0.8 | Build tool |
| TailwindCSS | 3.4.0 | CSS framework |
| Recharts | 3.5.1 | Data visualization |

## Database Schema

### Core Models

#### Users
- **User** (Custom AbstractUser)
  - Fields: email, username, first_name, last_name, role (student/teacher/admin), avatar, bio, social_links
  - Email-based authentication

#### Courses
- **Course**
  - Fields: title, slug, description, thumbnail, instructor, category, price, level, status
  - Relations: ManyToMany with students (through Enrollment)
  
- **Section**
  - Fields: title, order, course
  - Contains multiple lessons
  
- **Lesson**
  - Fields: title, content, video_url, document, duration, order, section
  - Tracks completion via LessonProgress

#### Enrollments
- **Enrollment**
  - Fields: student, course, enrolled_at, completed_at, is_completed
  
- **LessonProgress**
  - Fields: student, lesson, is_completed, completed_at
  
- **Certificate**
  - Fields: student, course, certificate_number, issued_at
  - Auto-generates certificate number on save
  
- **CartItem**
  - Fields: user, course, added_at
  
- **Payment**
  - Fields: user, course, amount, payment_method, transaction_id, status, paid_at

#### Assessments
- **Quiz**
  - Fields: title, description, course, time_limit, passing_score, is_published
  
- **Question**
  - Fields: quiz, text, question_type (multiple_choice/true_false), points, order
  
- **Choice**
  - Fields: question, text, is_correct
  
- **StudentQuizAttempt**
  - Fields: student, quiz, score, passed, started_at, completed_at
  
- **StudentAnswer**
  - Fields: attempt, question, selected_choice, is_correct
  
- **Assignment**
  - Fields: title, description, course, due_date, total_points, file_types
  
- **Submission**
  - Fields: assignment, student, file, text, grade, feedback, submitted_at, graded_at

#### Reviews
- **CourseReview**
  - Fields: course, student, rating (1-5), comment, created_at, updated_at
  - Unique constraint: one review per student per course

#### Chat
- **Conversation**
  - Fields: created_at, updated_at
  
- **ConversationParticipant**
  - Fields: conversation, user, joined_at
  
- **Message**
  - Fields: conversation, sender, content, created_at, is_read

## API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### Authentication

All authenticated endpoints require Bearer token in Authorization header:
```
Authorization: Bearer <access_token>
```

#### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login (returns JWT tokens) |
| POST | `/api/auth/refresh/` | Refresh access token |
| GET | `/api/auth/me/` | Get current user info |
| POST | `/api/auth/change-password/` | Change password |

### User Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users/` | List all users (admin) |
| GET | `/api/users/{id}/` | Get user details |
| PUT/PATCH | `/api/users/{id}/` | Update user |
| GET | `/api/users/me/profile/` | Get own profile |
| PUT | `/api/users/me/profile/` | Update own profile |
| GET | `/api/instructors/top/` | Get top instructors |
| GET | `/api/instructors/{id}/profile/` | Get instructor public profile |
| GET | `/api/students/{id}/profile/` | Get student public profile |

### Courses

#### Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses/` | List all published courses |
| GET | `/api/courses/{id}/` | Get course details |
| GET | `/api/courses/categories/` | Get all course categories |
| GET | `/api/courses/{id}/curriculum/` | Get course curriculum (sections & lessons) |
| GET | `/api/lessons/{id}/` | Get lesson details |

#### Teacher Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/teacher/courses/` | Create course |
| GET | `/api/teacher/courses/` | List own courses |
| GET | `/api/teacher/courses/{id}/` | Get course details |
| PUT/PATCH | `/api/teacher/courses/{id}/` | Update course |
| DELETE | `/api/teacher/courses/{id}/` | Delete course |
| POST | `/api/teacher/sections/` | Create section |
| PUT/PATCH | `/api/teacher/sections/{id}/` | Update section |
| DELETE | `/api/teacher/sections/{id}/` | Delete section |
| POST | `/api/teacher/lessons/` | Create lesson |
| PUT/PATCH | `/api/teacher/lessons/{id}/` | Update lesson |
| DELETE | `/api/teacher/lessons/{id}/` | Delete lesson |

### Enrollments

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/courses/{id}/enroll/` | Enroll in free course |
| POST | `/api/courses/{id}/purchase/` | Purchase paid course |
| GET | `/api/enrollments/me/` | Get my enrollments |
| GET | `/api/student/my-courses/` | Get student's courses |
| POST | `/api/lessons/{id}/complete/` | Mark lesson as complete |
| GET | `/api/enrollments/me/certificates/` | Get my certificates |
| POST | `/api/courses/{id}/certificate/issue/` | Issue certificate |
| GET | `/api/courses/{id}/certificate/me/` | Get my certificate for course |
| GET | `/api/enrollments/me/payments/` | Get payment history |

### Cart

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/enrollments/cart/` | Get cart items |
| POST | `/api/enrollments/cart/add/` | Add course to cart |
| DELETE | `/api/enrollments/cart/items/{id}/` | Remove item from cart |
| POST | `/api/enrollments/cart/checkout/` | Checkout cart |

### Assessments

#### Quizzes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses/{id}/quizzes/` | List course quizzes |
| GET | `/api/quizzes/{id}/` | Get quiz details |
| POST | `/api/quizzes/{id}/start/` | Start quiz attempt |
| POST | `/api/quizzes/{id}/submit/` | Submit quiz |
| GET | `/api/quizzes/{id}/attempts/me/` | Get my attempts |

**Teacher Quiz Management:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/teacher/quizzes/` | Create quiz |
| GET | `/api/teacher/quizzes/` | List own quizzes |
| PUT/PATCH | `/api/teacher/quizzes/{id}/` | Update quiz |
| DELETE | `/api/teacher/quizzes/{id}/` | Delete quiz |
| POST | `/api/teacher/quizzes/{id}/questions/` | Add question |
| PUT/PATCH | `/api/teacher/questions/{id}/` | Update question |
| DELETE | `/api/teacher/questions/{id}/` | Delete question |
| POST | `/api/teacher/questions/{id}/choices/` | Add choice |
| PUT/PATCH | `/api/teacher/choices/{id}/` | Update choice |
| DELETE | `/api/teacher/choices/{id}/` | Delete choice |

#### Assignments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses/{id}/assignments/` | List course assignments |
| GET | `/api/assignments/{id}/` | Get assignment details |
| POST | `/api/assignments/{id}/submit/` | Submit assignment |
| GET | `/api/assignments/{id}/my-submission/` | Get my submission |

**Teacher Assignment Management:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/teacher/assignments/` | Create assignment |
| GET | `/api/teacher/assignments/` | List own assignments |
| PUT/PATCH | `/api/teacher/assignments/{id}/` | Update assignment |
| DELETE | `/api/teacher/assignments/{id}/` | Delete assignment |
| GET | `/api/teacher/assignments/{id}/submissions/` | Get all submissions |
| PATCH | `/api/teacher/submissions/{id}/grade/` | Grade submission |

### Reviews

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/courses/{id}/reviews/` | List course reviews |
| POST | `/api/courses/{id}/reviews/` | Create/update review |
| GET | `/api/courses/{id}/rating-summary/` | Get rating summary |
| GET | `/api/courses/{id}/my-review/` | Get my review |
| GET | `/api/reviews/{id}/` | Get review details |
| PUT/PATCH | `/api/reviews/{id}/` | Update review |
| DELETE | `/api/reviews/{id}/` | Delete review |

### Analytics (Teacher Only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/teacher/analytics/summary/` | Get analytics summary |
| GET | `/api/teacher/analytics/courses/` | Get course statistics |
| GET | `/api/teacher/analytics/timeseries/` | Get time series data |
| GET | `/api/teacher/analytics/engagement/` | Get engagement metrics |

### Chat

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/chat/conversations/` | List conversations |
| POST | `/api/chat/conversations/` | Create conversation |
| GET | `/api/chat/conversations/{id}/` | Get conversation details |
| GET | `/api/chat/conversations/{id}/messages/` | Get messages |
| POST | `/api/chat/conversations/{id}/messages/` | Send message |
| GET | `/api/chat/unread-count/` | Get unread message count |

### Teacher Course Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/teacher/courses/{id}/students/` | Get enrolled students |
| DELETE | `/api/teacher/courses/{id}/students/{student_id}/` | Remove student |

## Installation

### Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- pip, npm/yarn

### Backend Setup

```bash
# Clone repository
git clone https://github.com/chienvoxn/LMS_DJANGO.git
cd LMS_DJANGO/lms_api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r ../requirements.txt

# Configure environment variables
cp .env.example .env.local
# Edit .env.local with your database credentials and settings

# Create MySQL database
mysql -u root -p
CREATE DATABASE lms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Run migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Collect static files (for production)
python manage.py collectstatic

# Run development server
python manage.py runserver
```

Backend will be available at: `http://127.0.0.1:8000`

### Frontend Setup

```bash
cd LMS_DJANGO/lms_frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at: `http://localhost:5173`

## Configuration

### Environment Variables

Create `.env.local` in `lms_api/` directory:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=lms
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306

# JWT (optional, uses SECRET_KEY by default)
JWT_SECRET_KEY=your-jwt-secret
```

### Database Configuration

The project uses MySQL with SSL support. Configure in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("DB_NAME"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    }
}
```

### CORS Configuration

For development:
```python
CORS_ALLOW_ALL_ORIGINS = True
```

For production, specify allowed origins:
```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

### JWT Configuration

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

## Features

### For Students

- User registration and authentication (JWT)
- Browse and search courses
- Enroll in free courses or purchase paid courses
- Shopping cart functionality
- View course curriculum (sections & lessons)
- Track lesson completion progress
- Take quizzes and assignments
- Submit assignments with file uploads
- Earn certificates upon course completion
- Write and read course reviews
- View payment history
- Real-time chat with instructors
- View public instructor profiles

### For Instructors/Teachers

- Create and manage courses (CRUD operations)
- Organize courses into sections and lessons
- Upload lesson documents and videos
- Create quizzes with multiple-choice questions
- Create assignments with file submissions
- Grade student submissions
- View enrolled students per course
- Remove students from courses
- Issue certificates to students
- Respond to course reviews
- View detailed analytics:
  - Enrollment statistics
  - Student performance metrics
  - Time series data
  - Engagement analytics
- Real-time chat with students

### For Administrators

- Full user management (CRUD)
- Manage all courses across platform
- View platform-wide analytics
- Manage course categories
- Access Django admin panel

## Development

### Project Structure

The backend follows Django's app-based architecture:

- **users**: Authentication, user profiles, public profiles
- **courses**: Course catalog, curriculum management
- **enrollments**: Enrollment tracking, progress, certificates, payments
- **assessments**: Quizzes, assignments, submissions, grading
- **reviews**: Course ratings and reviews
- **analytics**: Teacher and admin analytics
- **chat**: Real-time messaging system
- **common**: Shared permissions and utilities

### Adding New Features

```bash
# Create new Django app
python manage.py startapp <app_name>

# Add to INSTALLED_APPS in settings.py

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Running Tests

```bash
python manage.py test
```

### Code Style

- Follow PEP 8 for Python code
- Use Django REST Framework conventions
- Document API endpoints with docstrings
- Write unit tests for new features

## Deployment

### Production Checklist

1. **Security**
   - Set `DEBUG = False`
   - Update `SECRET_KEY` to a strong random value
   - Configure `ALLOWED_HOSTS` with your domain
   - Disable `CORS_ALLOW_ALL_ORIGINS`
   - Set up proper CORS origins
   - Enable HTTPS/SSL

2. **Database**
   - Use production MySQL instance
   - Configure database backups
   - Run `python manage.py migrate`

3. **Static & Media Files**
   - Configure `STATIC_ROOT` and run `collectstatic`
   - Set up CDN for media files (AWS S3, CloudFlare R2, etc.)
   - Configure `MEDIA_ROOT` and `MEDIA_URL`

4. **WSGI Server**
   - Use Gunicorn or uWSGI
   - Configure with systemd or supervisor

5. **Reverse Proxy**
   - Use Nginx or Apache
   - Configure SSL certificates (Let's Encrypt)

### Example Gunicorn Command

```bash
gunicorn lms_backend.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
```

### Example Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    client_max_body_size 100M;

    # Frontend
    location / {
        root /path/to/lms_frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Media files
    location /media/ {
        alias /path/to/lms_api/media/;
    }
}
```

## API Response Format

### Success Response

```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response

```json
{
  "success": false,
  "error": "Error message",
  "details": { ... }
}
```

### Pagination

List endpoints return paginated responses:

```json
{
  "count": 100,
  "next": "http://api.example.com/courses/?page=2",
  "previous": null,
  "results": [
    { ... }
  ]
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

**Database Connection Error**
- Verify MySQL is running
- Check database credentials in `.env.local`
- Ensure database exists

**CORS Errors**
- Check `CORS_ALLOWED_ORIGINS` in production
- Verify frontend URL is whitelisted

**Media Files Not Loading**
- Check `MEDIA_URL` and `MEDIA_ROOT` settings
- Ensure media directory has proper permissions
- Configure web server to serve media files

**JWT Token Issues**
- Verify `SIMPLE_JWT` settings
- Check token expiration times
- Ensure `Authorization` header format is correct

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**GitHub**: [@chienvoxn](https://github.com/chienvoxn)

## Support

For issues and questions, please open an issue on GitHub.