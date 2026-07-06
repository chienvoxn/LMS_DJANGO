# LMS_DJANGO - Hệ thống Quản lý Học tập

## Tổng quan dự án

LMS_DJANGO là một hệ thống quản lý học tập (Learning Management System) được xây dựng với kiến trúc **Frontend分离**:
- **Backend**: Django REST Framework (Python)
- **Frontend**: React.js với Vite + TailwindCSS

## Kiến trúc dự án

```
LMS_DJANGO/
├── lms_api/                    # Backend API (Django)
│   ├── lms_backend/           # Cấu hình Django chính
│   │   ├── settings.py        # Cài đặt ứng dụng
│   │   ├── urls.py            # Routes chính
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── users/                 # Quản lý người dùng
│   ├── courses/               # Quản lý khóa học
│   ├── enrollments/           # Quản lý đăng ký khóa học
│   ├── assessments/           # Quản lý bài kiểm tra/đánh giá
│   ├── reviews/               # Quản lý đánh giá
│   ├── analytics/             # Thống kê và phân tích
│   ├── common/                # Chức năng chung
│   ├── media/                 # Thư mục lưu trữ media
│   └── manage.py
│
├── lms_frontend/              # Frontend (React)
│   ├── src/                   # Mã nguồn React
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
└── requirements.txt           # Dependencies Python
```

## Công nghệ sử dụng

### Backend
| Công nghệ | Phiên bản | Mục đích |
|-----------|-----------|----------|
| Django | 5.2.7 | Web framework |
| Django REST Framework | 3.16.1 | RESTful API |
| SimpleJWT | - | Xác thực JWT |
| MySQL | - | Cơ sở dữ liệu |
| django-cors-headers | - | CORS middleware |

### Frontend
| Công nghệ | Phiên bản | Mục đích |
|-----------|-----------|----------|
| React | 18.2.0 | UI Library |
| React Router DOM | 6.20.0 | Routing |
| Axios | 1.6.2 | HTTP Client |
| Vite | 5.0.8 | Build tool |
| TailwindCSS | 3.4.0 | CSS Framework |
| Recharts | 3.5.1 | Biểu đồ/Thống kê |

## Cài đặt và chạy dự án

### Yêu cầu hệ thống
- Python 3.10+
- Node.js 18+
- MySQL Server

### Backend Setup

```bash
# Clone repository
git clone https://github.com/chienvoxn/LMS_DJANGO.git
cd LMS_DJANGO/lms_api

# Tạo virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/Mac

# Cài dependencies
pip install -r ../requirements.txt

# Tạo database MySQL
mysql -u root -p
CREATE DATABASE lms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Chạy migrations
python manage.py migrate

# Tạo superuser
python manage.py createsuperuser

# Chạy server
python manage.py runserver
```

Backend sẽ chạy tại: `http://127.0.0.1:8000`

### Frontend Setup

```bash
cd LMS_DJANGO/lms_frontend

# Cài dependencies
npm install

# Chạy development server
npm run dev
```

Frontend sẽ chạy tại: `http://localhost:5173`

## Các mô hình dữ liệu

### 1. Users (Người dùng)
- **User Model**: Mô hình tùy chỉnh kế thừa từ AbstractUser
- **Roles**: Student (Học viên), Teacher (Giảng viên), Admin
- **Fields**: username, email, first_name, last_name, role, avatar...

### 2. Courses (Khóa học)
- **Course**: Khóa học chính
- **Category**: Danh mục khóa học
- **Lesson**: Bài học trong khóa học

### 3. Enrollments (Đăng ký)
- **Enrollment**: Đăng ký khóa học của học viên
- **Cart**: Giỏ hàng đăng ký

### 4. Assessments (Đánh giá)
- **Quiz/Bai_kiem_tra**: Các bài kiểm tra
- **Question**: Câu hỏi
- **Answer**: Đáp án

### 5. Reviews (Đánh giá)
- **Review**: Đánh giá khóa học từ học viên

### 6. Analytics (Thống kê)
- **Statistics**: Thống kê khóa học, người dùng

## API Endpoints

### Xác thực (Authentication)
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/auth/register/` | Đăng ký tài khoản |
| POST | `/api/auth/login/` | Đăng nhập (JWT) |
| POST | `/api/auth/refresh/` | Làm mới access token |
| GET | `/api/auth/me/` | Lấy thông tin người dùng hiện tại |
| POST | `/api/auth/change-password/` | Đổi mật khẩu |

### Quản lý người dùng
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/PUT | `/api/users/` | Danh sách/Cập nhật người dùng |

### Khóa học
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/api/courses/` | Danh sách/Tạo khóa học |
| GET/PUT/DELETE | `/api/courses/{id}/` | Chi tiết/Sửa/Xóa khóa học |

### Đăng ký khóa học
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/api/enrollments/` | Danh sách/Tạo đăng ký |
| GET | `/api/student/my-courses/` | Khóa học của học viên |
| GET | `/api/teacher/courses/{id}/students/` | DS học viên theo khóa |

### Đánh giá
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET/POST | `/api/reviews/` | Danh sách/Tạo đánh giá |

### Thống kê
| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/analytics/` | Thống kê tổng quan |

## Cấu hình JWT

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

## Cấu hình CORS

```python
CORS_ALLOW_ALL_ORIGINS = True  # Chỉ dùng cho development
CORS_ALLOW_CREDENTIALS = True
```

## Chức năng chính

### Cho Học viên
- Đăng ký/đăng nhập tài khoản
- Duyệt và tìm kiếm khóa học
- Đăng ký khóa học
- Xem bài học
- Làm bài kiểm tra
- Đánh giá khóa học
- Xem thống kê tiến độ

### Cho Giảng viên
- Tạo và quản lý khóa học
- Tạo bài học và bài kiểm tra
- Xem danh sách học viên theo khóa học
- Xem thống kê khóa học
- Quản lý đánh giá

### Cho Admin
- Quản lý người dùng
- Quản lý tất cả khóa học
- Xem thống kê tổng quan
- Quản lý danh mục

## Phát triển

### Thêm ứng dụng mới
```bash
python manage.py startapp <app_name>
```

### Tạo Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### Chạy Test
```bash
python manage.py test
```

## Ghi chú quan trọng

1. **Bảo mật**: Thay đổi `SECRET_KEY` trong `settings.py` khi deploy production
2. **Database**: Cấu hình MySQL trong `settings.py` với thông tin thực tế
3. **CORS**: Tắt `CORS_ALLOW_ALL_ORIGINS` và cấu hình đúng domain trong production
4. **Media Files**: Cấu hình lại `MEDIA_ROOT` và `MEDIA_URL` cho production

## License

MIT License

## Tác giả

- GitHub: [chienvoxn](https://github.com/chienvoxn)
