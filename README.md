<div align="center">

# LMS_DJANGO

**Hệ thống quản lý học tập full-stack xây dựng bằng Django REST Framework và React**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.7-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![MySQL](https://img.shields.io/badge/MySQL-8%2B-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)

</div>

## Giới thiệu

**LMS_DJANGO** là một hệ thống quản lý học tập (_Learning Management System — LMS_) sử dụng kiến trúc tách biệt frontend và backend:

- **Backend:** Django REST Framework.
- **Frontend:** React, Vite và Tailwind CSS.
- **Database:** MySQL.
- **Authentication:** JSON Web Token (JWT).

Hệ thống hỗ trợ học viên, giảng viên và quản trị viên trong việc quản lý khóa học, nội dung học tập, đăng ký học, tiến độ, bài kiểm tra, bài tập, đánh giá, chứng chỉ, thanh toán mô phỏng, thống kê và nhắn tin.

> Dự án được phát triển chủ yếu cho mục đích học tập và thực hành xây dựng ứng dụng web full-stack.

## Tính năng

### Học viên

- Đăng ký, đăng nhập và quản lý hồ sơ.
- Duyệt, tìm kiếm và đăng ký khóa học.
- Xem chương học, bài học và theo dõi tiến độ.
- Làm quiz, nộp bài tập và xem kết quả.
- Quản lý giỏ hàng và lịch sử thanh toán.
- Đánh giá khóa học và nhận chứng chỉ.
- Nhắn tin trực tiếp hoặc theo nhóm.

### Giảng viên

- Tạo và quản lý khóa học, chương học và bài học.
- Tạo quiz, câu hỏi, đáp án và bài tập.
- Xem bài nộp và chấm điểm học viên.
- Quản lý danh sách học viên.
- Xem thống kê khóa học và mức độ tương tác.

### Quản trị viên

- Quản lý người dùng và vai trò.
- Quản lý dữ liệu hệ thống qua Django Admin.
- Giám sát khóa học và các tài nguyên liên quan.

## Công nghệ

### Backend

| Công nghệ             |      Phiên bản |
| --------------------- | -------------: |
| Python                |          3.10+ |
| Django                |          5.2.7 |
| Django REST Framework |         3.16.1 |
| Simple JWT            |          5.5.1 |
| MySQL                 | 8+ khuyến nghị |
| mysqlclient           |          2.2.7 |
| django-cors-headers   |          4.9.0 |
| python-dotenv         |          1.2.2 |

### Frontend

| Công nghệ        | Phiên bản |
| ---------------- | --------: |
| React            |    18.2.0 |
| React Router DOM |    6.20.0 |
| Axios            |     1.6.2 |
| Vite             |     5.0.8 |
| Tailwind CSS     |     3.4.0 |
| Recharts         |     3.5.1 |

## Kiến trúc

```text
React Client
    │ HTTP/JSON + Bearer JWT
    ▼
Django REST Framework
    │ Django ORM
    ▼
MySQL
```

## Cấu trúc dự án

```text
LMS_DJANGO/
├── lms_api/
│   ├── lms_backend/       # Cấu hình Django
│   ├── users/             # Người dùng và xác thực
│   ├── courses/           # Khóa học, chương và bài học
│   ├── enrollments/       # Đăng ký, tiến độ, giỏ hàng, thanh toán
│   ├── assessments/       # Quiz, câu hỏi, bài tập, bài nộp
│   ├── reviews/           # Đánh giá khóa học
│   ├── analytics/         # Thống kê giảng viên
│   ├── chat/              # Hội thoại và tin nhắn
│   ├── common/            # Thành phần dùng chung
│   ├── cert/              # Chứng chỉ CA cho database
│   ├── media/             # Tệp tải lên
│   ├── .env.example
│   └── manage.py
├── lms_frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── config/
│   │   ├── context/
│   │   ├── pages/
│   │   └── routes/
│   └── package.json
├── requirements.txt
└── README.md
```

Các model chính:

```text
User
├── Course → Section → Lesson
├── Enrollment → LessonProgress → Certificate
├── Quiz → Question → Choice → StudentQuizAttempt
├── Assignment → Submission
├── CartItem
├── Payment
├── CourseReview
└── Conversation → Message
```

## Bắt đầu

### Yêu cầu

- Git
- Python 3.10+
- Node.js 18+
- npm
- MySQL Server

### 1. Clone repository

```bash
git clone https://github.com/chienvoxn/LMS_DJANGO.git
cd LMS_DJANGO
```

### 2. Tạo database

```sql
CREATE DATABASE lms_backend
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
```

### 3. Cài đặt backend

```bash
cd lms_api
python -m venv venv
```

Kích hoạt môi trường ảo:

```powershell
# Windows
venv\Scripts\activate
```

```bash
# Linux/macOS
source venv/bin/activate
```

Cài dependencies:

```bash
python -m pip install --upgrade pip
pip install -r ../requirements.txt
```

### 4. Cấu hình môi trường

Backend đọc biến môi trường từ `lms_api/.env.local`.

Tạo tệp từ mẫu:

```powershell
# Windows
copy .env.example .env.local
```

```bash
# Linux/macOS
cp .env.example .env.local
```

Nội dung mẫu:

```dotenv
SECRET_KEY=your_secure_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=lms_backend
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306

CORS_ALLOWED_ORIGINS=http://localhost:5173
```

Tạo `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

> Không commit `.env.local`, mật khẩu hoặc khóa bí mật lên GitHub.

### 5. Chạy backend

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- API: `http://127.0.0.1:8000`
- Django Admin: `http://127.0.0.1:8000/admin/`

### 6. Chạy frontend

Mở terminal mới:

```bash
cd LMS_DJANGO/lms_frontend
npm install
npm run dev
```

Frontend mặc định chạy tại `http://localhost:5173`.

## Xác thực

Các API được bảo vệ sử dụng JWT:

```http
Authorization: Bearer <access_token>
```

- Access token: 1 giờ.
- Refresh token: 7 ngày.

## API chính

| Nhóm            | Prefix/Endpoint                     |
| --------------- | ----------------------------------- |
| Authentication  | `/api/auth/`                        |
| Users           | `/api/users/`                       |
| Courses         | `/api/courses/`                     |
| Teacher courses | `/api/teacher/courses/`             |
| Enrollments     | `/api/enrollments/`                 |
| Cart            | `/api/enrollments/cart/`            |
| Quizzes         | `/api/quizzes/`                     |
| Assignments     | `/api/assignments/`                 |
| Reviews         | `/api/courses/{course_id}/reviews/` |
| Analytics       | `/api/teacher/analytics/`           |
| Chat            | `/api/chat/`                        |

Endpoint xác thực tiêu biểu:

| Method | Endpoint                     | Mô tả               |
| ------ | ---------------------------- | ------------------- |
| `POST` | `/api/auth/register/`        | Đăng ký             |
| `POST` | `/api/auth/login/`           | Đăng nhập           |
| `POST` | `/api/auth/refresh/`         | Làm mới token       |
| `GET`  | `/api/auth/me/`              | Người dùng hiện tại |
| `POST` | `/api/auth/change-password/` | Đổi mật khẩu        |

## Kiểm thử

Backend:

```bash
cd lms_api
python manage.py check
python manage.py test
python manage.py makemigrations --check
```

Frontend:

```bash
cd lms_frontend
npm run lint
npm run build
```

## Lưu ý

- `settings.py` hiện có cấu hình MySQL SSL. Khi dùng MySQL local không yêu cầu SSL, cần điều chỉnh `DATABASES["default"]["OPTIONS"]`.
- Kiểm tra đường dẫn chứng chỉ CA trong `settings.py` có khớp với thư mục `lms_api/cert/`.
- `CORS_ALLOW_ALL_ORIGINS=True` chỉ nên dùng trong development.
- Không sử dụng `DEBUG=True` trong production.
- Media upload hiện được lưu trong `lms_api/media/`.
