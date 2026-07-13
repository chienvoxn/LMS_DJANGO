<div align="center">

# LMS_DJANGO

**Nền tảng học tập trực tuyến full-stack với trợ lý AI thông minh**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.7-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![MySQL](https://img.shields.io/badge/MySQL-8%2B-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![RAG](https://img.shields.io/badge/RAG-Ollama%20%7C%20ChromaDB-6DB33F?logo=ollama&logoColor=white)](https://ollama.ai/)

</div>

## Giới thiệu

**LMS_DJANGO** là một nền tảng học tập trực tuyến toàn diện, cho phép giảng viên xây dựng và quản lý khóa học, học viên đăng ký học, theo dõi tiến độ, làm bài kiểm tra, nộp bài tập và nhận chứng chỉ. Hệ thống tích hợp trợ lý AI (RAG) cho phép người dùng tải tài liệu cá nhân và hỏi đáp trực tiếp dựa trên nội dung tài liệu.

Kiến trúc tách biệt giữa frontend và backend:

- **Backend:** Django 5.2.7 + Django REST Framework 3.16.1
- **Frontend:** React 18 + Vite + Tailwind CSS 3
- **Database:** MySQL 8+ (SSL)
- **Authentication:** JSON Web Token (SimpleJWT) — access token 1 giờ, refresh token 7 ngày
- **AI:** Ollama (bge-m3 embedding + qwen2.5:3b LLM) + ChromaDB vector store
- **Kiến trúc API:** RESTful API

## Tính năng chính

### Khách

- Xem danh sách và chi tiết khóa học, tìm kiếm theo danh mục/cấp độ
- Xem thông tin giảng viên và hồ sơ công khai
- Đăng ký, đăng nhập tài khoản

### Học viên

- Quản lý hồ sơ cá nhân (avatar, bio, headline, social links)
- Duyệt, tìm kiếm, đăng ký khóa học (miễn phí/trả phí/audit)
- Giỏ hàng và thanh toán mô phỏng
- Xem chương học, bài giảng, tài liệu và video
- Đánh dấu bài học hoàn thành, theo dõi tiến độ %
- Làm bài kiểm tra trắc nghiệm, xem điểm
- Nộp bài tập, xem điểm số và phản hồi
- Đánh giá khóa học (rating 1-5 + bình luận)
- Nhận chứng chỉ sau khi hoàn thành khóa học trả phí
- Xem lịch sử đăng ký, thanh toán và chứng chỉ
- Nhắn tin trực tiếp hoặc theo nhóm
- **AI Assistant:** tải tài liệu PDF/TXT/DOCX/PPTX, hỏi đáp, tóm tắt, tạo flashcard

### Giảng viên

- Tạo và quản lý khóa học (thông tin, thumbnail, giá, danh mục)
- Tạo chương học (section) và bài học (lesson) với video, tài liệu
- Tạo quiz, câu hỏi trắc nghiệm và đáp án
- Tạo và quản lý bài tập (assignment)
- Xem bài nộp, chấm điểm và phản hồi
- Quản lý danh sách học viên trong khóa học
- Xóa học viên khỏi khóa học
- Theo dõi tiến độ và hoạt động học tập
- Xem thống kê tổng quan, theo khóa học, chuỗi thời gian, mức độ tương tác
- Trao đổi qua hệ thống nhắn tin
- **AI Assistant:** tài liệu giảng dạy, hỗ trợ soạn bài

### Quản trị viên

- Quản lý tài khoản, vai trò và quyền truy cập qua Django Admin
- Quản lý toàn bộ dữ liệu hệ thống

## Công nghệ

### Backend

| Công nghệ | Phiên bản |
| --------- | --------: |
| Python | 3.10+ |
| Django | 5.2.7 |
| Django REST Framework | 3.16.1 |
| Simple JWT | 5.5.1 |
| MySQL | 8+ khuyến nghị |
| mysqlclient | 2.2.7 |
| django-cors-headers | 4.9.0 |
| python-dotenv | 1.2.2 |
| ChromaDB | 0.5+ |
| Ollama (Python client) | 0.3+ |
| pypdf | 4.0+ |
| python-docx | 1.1+ |
| python-pptx | 1.0+ |

### Frontend

| Công nghệ | Phiên bản |
| --------- | --------: |
| React | 18.2.0 |
| React Router DOM | 6.20.0 |
| Axios | 1.6.2 |
| Vite | 5.0.8 |
| Tailwind CSS | 3.4.0 |
| Recharts | 3.5.1 |

### AI Models (Ollama)

| Model | Vai trò |
| ----- | ------- |
| **bge-m3** | Embedding model — vector hóa tài liệu và câu hỏi |
| **qwen2.5:3b** | LLM — sinh câu trả lời dựa trên ngữ cảnh |

## Kiến trúc

```text
React Client
    │ HTTP/JSON + Bearer JWT
    ▼
Django REST Framework
    │ Django ORM
    ├── MySQL
    │   ├── users, courses, sections, lessons
    │   ├── enrollments, lesson_progresses
    │   ├── certificates, cart_items, payments
    │   ├── quizzes, questions, choices, attempts, answers
    │   ├── assignments, submissions
    │   ├── course_reviews
    │   ├── conversations, messages
    │   ├── rag_documents, rag_chunks
    │   └── rag_conversations, rag_messages
    │
    ├── Media Storage
    │   └── rag/documents/{user_id}/...
    │
    ├── ChromaDB Persistent
    │   └── embedding + metadata + chunk text
    │
    └── Ollama
        ├── bge-m3       → tạo embedding
        └── qwen2.5:3b   → sinh câu trả lời
```

## Cấu trúc dự án

```text
LMS_DJANGO/
├── lms_api/
│   ├── lms_backend/       # Cấu hình Django (settings, urls, wsgi)
│   ├── users/             # Người dùng, xác thực và hồ sơ
│   ├── courses/           # Khóa học, chương, bài học
│   ├── enrollments/       # Ghi danh, tiến độ, giỏ hàng, thanh toán, chứng chỉ
│   ├── assessments/       # Quiz, câu hỏi, bài tập, bài nộp
│   ├── reviews/           # Đánh giá khóa học
│   ├── analytics/         # Thống kê giảng viên
│   ├── chat/              # Nhắn tin (hội thoại, tin nhắn)
│   ├── rag/               # AI Assistant (RAG với ChromaDB + Ollama)
│   ├── common/            # Thành phần dùng chung (permissions)
│   ├── cert/              # Chứng chỉ CA cho database
│   ├── chroma_db/         # Vector store persistent (ChromaDB)
│   ├── media/             # Tệp tải lên (gồm rag/documents/)
│   ├── .env.example
│   └── manage.py
├── lms_frontend/
│   ├── src/
│   │   ├── api/           # Axios client + ragApi
│   │   ├── components/    # UI components (navbar, rag/, chat/, ...)
│   │   ├── config/        # Cấu hình danh mục khóa học
│   │   ├── context/       # AuthContext, ThemeContext
│   │   ├── pages/         # Pages (AIAssistant, ChatPage, ...)
│   │   └── routes/        # AppRouter
│   └── package.json
├── requirements.txt
├── README.md
├── RAG.md                 # Tài liệu chi tiết module AI Assistant
└── Description.md         # SRS — Đặc tả yêu cầu phần mềm
```

## Các model chính

```text
User
├── Course → Section → Lesson
├── Enrollment → LessonProgress → Certificate
├── Quiz → Question → Choice → StudentQuizAttempt
├── Assignment → Submission
├── CartItem
├── Payment
├── CourseReview
├── Conversation → Message
└── RagDocument → RagChunk → RagConversation → RagMessage
```

## Bắt đầu

### Yêu cầu

- Git
- Python 3.10+
- Node.js 18+
- npm
- MySQL Server 8+
- Ollama (cho AI Assistant) — tải tại [ollama.ai](https://ollama.ai)

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

# RAG / AI Assistant
RAG_CHROMA_PATH=./chroma_db
RAG_COLLECTION_NAME=lms_user_documents
RAG_OLLAMA_BASE_URL=http://127.0.0.1:11434
RAG_LLM_MODEL=qwen2.5:3b
RAG_EMBED_MODEL=bge-m3
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

### 7. Cài đặt AI Assistant (tùy chọn)

Cài Ollama và tải model:

```bash
ollama pull bge-m3
ollama pull qwen2.5:3b
```

Kiểm tra Ollama sẵn sàng:

```bash
ollama serve     # Nếu chưa chạy nền
python manage.py rag_health
```

Xem tài liệu chi tiết tại [`RAG.md`](RAG.md).

## Xác thực

Các API được bảo vệ sử dụng JWT:

```http
Authorization: Bearer <access_token>
```

- Access token: 1 giờ
- Refresh token: 7 ngày

## API chính

### Backend (REST API)

| Nhóm | Prefix/Endpoint |
| ---- | --------------- |
| Authentication | `/api/auth/` |
| Users | `/api/users/` |
| Courses | `/api/courses/` |
| Teacher courses | `/api/teacher/courses/` |
| Enrollments | `/api/enrollments/` |
| Cart | `/api/enrollments/cart/` |
| Certificates | `/api/enrollments/me/certificates/` |
| Quizzes | `/api/quizzes/` |
| Assignments | `/api/assignments/` |
| Reviews | `/api/courses/{course_id}/reviews/` |
| Analytics | `/api/teacher/analytics/` |
| Chat | `/api/chat/` |
| **AI Assistant (RAG)** | `/api/rag/` |

### Chat

| Method | Endpoint | Mô tả |
| ------ | -------- | ----- |
| `GET/POST` | `/api/chat/conversations/` | Danh sách / Tạo hội thoại |
| `GET/PUT/DELETE` | `/api/chat/conversations/{id}/` | Chi tiết hội thoại |
| `GET/POST` | `/api/chat/conversations/{id}/messages/` | Danh sách / Gửi tin nhắn |
| `GET` | `/api/chat/unread-count/` | Số hội thoại chưa đọc |

### AI Assistant (RAG)

| Method | Endpoint | Mô tả |
| ------ | -------- | ----- |
| `GET` | `/api/rag/health/` | Kiểm tra Ollama + ChromaDB |
| `GET/POST` | `/api/rag/documents/` | Danh sách / Upload tài liệu |
| `GET/DELETE` | `/api/rag/documents/{id}/` | Chi tiết / Xóa tài liệu |
| `POST` | `/api/rag/documents/{id}/reindex/` | Re-index tài liệu |
| `GET/POST` | `/api/rag/conversations/` | Danh sách / Tạo hội thoại |
| `GET/PUT/DELETE` | `/api/rag/conversations/{id}/` | Chi tiết hội thoại |
| `POST` | `/api/rag/conversations/{id}/messages/` | Gửi câu hỏi đến AI |

## Frontend Routes

| Route | Mô tả | Quyền |
| ----- | ----- | ----- |
| `/` | Trang chủ | Public |
| `/browse` | Duyệt khóa học | Public |
| `/login`, `/register` | Đăng nhập, đăng ký | Public |
| `/courses/:id` | Chi tiết khóa học | Public |
| `/courses/:id/learn` | Học khóa học | Authenticated |
| `/courses/:id/learn/lessons/:id` | Xem bài học | Authenticated |
| `/dashboard` | Dashboard học viên | Authenticated |
| `/my-learning` | Khóa học của tôi | Student |
| `/cart`, `/cart/checkout` | Giỏ hàng & thanh toán | Authenticated |
| `/teacher/dashboard` | Dashboard giảng viên | Teacher |
| `/teacher/analytics` | Thống kê | Teacher |
| `/teacher/courses/:id/edit` | Chỉnh sửa khóa học | Teacher |
| `/teacher/courses/:id/quizzes` | Quản lý quiz | Teacher |
| `/teacher/courses/:id/students` | Quản lý học viên | Teacher |
| `/chat` | Nhắn tin | Authenticated |
| `/ai-assistant` | AI Assistant (RAG) | Authenticated |

## Kiểm thử

Backend:

```bash
cd lms_api
python manage.py check
python manage.py test
python manage.py makemigrations --check
```

RAG health check:

```bash
python manage.py rag_health
python manage.py reindex_rag
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
- AI Assistant yêu cầu Ollama chạy nền với model `bge-m3` và `qwen2.5:3b`.
- ChromaDB lưu vector tại `lms_api/chroma_db/` — không commit thư mục này lên Git.
- Chi tiết module RAG xem tại [`RAG.md`](RAG.md).
- Chi tiết đặc tả yêu cầu phần mềm xem tại [`Description.md`](Description.md).

For issues and questions, please open an issue on GitHub.
