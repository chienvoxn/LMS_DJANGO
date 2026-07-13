<div align="center">

# LMS_DJANGO

**Nền tảng Learning Management System full-stack với Django REST Framework, React và trợ lý AI RAG chạy cục bộ**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2.7-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.16.1-A30000?logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.0.8-646CFF?logo=vite&logoColor=white)](https://vite.dev/)
[![MySQL](https://img.shields.io/badge/MySQL-8%2B-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_AI-000000?logo=ollama&logoColor=white)](https://ollama.com/)

</div>

---

## Mục lục

- [LMS\_DJANGO](#lms_django)
  - [Mục lục](#mục-lục)
  - [Giới thiệu](#giới-thiệu)
  - [Điểm nổi bật](#điểm-nổi-bật)
  - [Vai trò người dùng](#vai-trò-người-dùng)
  - [Tính năng chính](#tính-năng-chính)
    - [Khách](#khách)
    - [Học viên](#học-viên)
    - [Giảng viên](#giảng-viên)
    - [Quản trị viên](#quản-trị-viên)
  - [Trợ lý AI RAG](#trợ-lý-ai-rag)
    - [Luồng xử lý](#luồng-xử-lý)
    - [Khả năng](#khả-năng)
    - [Cấu hình mặc định](#cấu-hình-mặc-định)
  - [Công nghệ sử dụng](#công-nghệ-sử-dụng)
    - [Backend cốt lõi](#backend-cốt-lõi)
    - [Frontend](#frontend)
    - [AI và xử lý tài liệu](#ai-và-xử-lý-tài-liệu)
  - [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
  - [Cấu trúc dự án](#cấu-trúc-dự-án)
  - [Mô hình dữ liệu](#mô-hình-dữ-liệu)
    - [LMS](#lms)
    - [RAG](#rag)
  - [Hướng dẫn cài đặt](#hướng-dẫn-cài-đặt)
    - [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
    - [1. Clone repository](#1-clone-repository)
    - [2. Tạo môi trường ảo ở thư mục gốc](#2-tạo-môi-trường-ảo-ở-thư-mục-gốc)
    - [3. Cài dependency cho RAG](#3-cài-dependency-cho-rag)
    - [4. Tạo MySQL database](#4-tạo-mysql-database)
    - [5. Tạo file môi trường](#5-tạo-file-môi-trường)
    - [6. Cấu hình RAG tùy chọn](#6-cấu-hình-rag-tùy-chọn)
    - [7. Kiểm tra MySQL SSL](#7-kiểm-tra-mysql-ssl)
    - [8. Chạy migration](#8-chạy-migration)
    - [9. Cài frontend](#9-cài-frontend)
  - [Khởi chạy dự án](#khởi-chạy-dự-án)
    - [1. Chạy Ollama](#1-chạy-ollama)
    - [2. Chạy backend](#2-chạy-backend)
    - [3. Chạy frontend](#3-chạy-frontend)
    - [Địa chỉ mặc định](#địa-chỉ-mặc-định)
    - [Chạy nhanh trên Windows](#chạy-nhanh-trên-windows)
  - [Xác thực JWT](#xác-thực-jwt)
  - [API chính](#api-chính)
    - [Tổng quan](#tổng-quan)
    - [Authentication](#authentication)
    - [RAG](#rag-1)
  - [Kiểm thử và quản trị RAG](#kiểm-thử-và-quản-trị-rag)
    - [Backend](#backend)
    - [Frontend](#frontend-1)
    - [Kiểm tra RAG](#kiểm-tra-rag)
  - [Các lưu ý hiện tại](#các-lưu-ý-hiện-tại)
  - [Bảo mật và triển khai](#bảo-mật-và-triển-khai)
  - [Tài liệu liên quan](#tài-liệu-liên-quan)

---

## Giới thiệu

**LMS_DJANGO** là một nền tảng quản lý học tập trực tuyến được phát triển theo mô hình của các hệ thống như **Coursera** và **Udemy**.

Hệ thống hỗ trợ quy trình học tập trực tuyến từ đầu đến cuối:

- Tìm kiếm và xem thông tin khóa học.
- Quản lý giỏ hàng và thanh toán mô phỏng.
- Đăng ký và tham gia khóa học.
- Xem video, tài liệu và nội dung bài học.
- Theo dõi tiến độ học tập.
- Làm quiz và nộp bài tập.
- Chấm điểm và phản hồi bài nộp.
- Đánh giá khóa học.
- Cấp chứng chỉ hoàn thành.
- Nhắn tin trực tiếp hoặc theo nhóm.
- Hỏi đáp với tài liệu cá nhân thông qua trợ lý AI RAG.

Dự án sử dụng kiến trúc tách biệt:

- **Backend:** Django REST Framework.
- **Frontend:** React, Vite và Tailwind CSS.
- **Database chính:** MySQL.
- **Vector database:** ChromaDB.
- **Local AI runtime:** Ollama.
- **Authentication:** JSON Web Token.
- **API architecture:** RESTful API.

> Dự án được xây dựng chủ yếu cho mục đích học tập, nghiên cứu và thực hành phát triển một nền tảng giáo dục trực tuyến full-stack có tích hợp AI.

---

## Điểm nổi bật

| Thành phần                     | Mô tả                                                                             |
| ------------------------------ | --------------------------------------------------------------------------------- |
| **LMS đầy đủ**                 | Quản lý khóa học, chương, bài học, quiz, bài tập, tiến độ, đánh giá và chứng chỉ. |
| **Phân quyền theo vai trò**    | Giao diện và API riêng cho khách, học viên, giảng viên và quản trị viên.          |
| **JWT Authentication**         | Access token, refresh token và tự động làm mới token ở frontend.                  |
| **Teacher Analytics**          | Thống kê tổng quan, khóa học, mức độ tương tác và dữ liệu theo thời gian.         |
| **Chat**                       | Hỗ trợ hội thoại trực tiếp và hội thoại nhóm.                                     |
| **AI Assistant**               | Tải tài liệu, lập chỉ mục, hỏi đáp theo ngữ cảnh và trả về nguồn trích dẫn.       |
| **Local-first AI**             | Mô hình ngôn ngữ và embedding chạy qua Ollama trên máy cục bộ.                    |
| **Frontend/Backend tách biệt** | React giao tiếp với Django REST Framework qua HTTP/JSON.                          |

---

## Vai trò người dùng

| Vai trò           | Khả năng chính                                                                                 |
| ----------------- | ---------------------------------------------------------------------------------------------- |
| **Khách**         | Xem trang chủ, tìm kiếm khóa học, xem chi tiết khóa học và hồ sơ công khai.                    |
| **Học viên**      | Mua hoặc đăng ký khóa học, học bài, làm quiz, nộp bài tập, theo dõi tiến độ và nhận chứng chỉ. |
| **Giảng viên**    | Xây dựng khóa học, quản lý nội dung, bài đánh giá, học viên và thống kê.                       |
| **Quản trị viên** | Quản lý dữ liệu và tài khoản thông qua Django Admin.                                           |

---

## Tính năng chính

### Khách

- Xem danh sách và chi tiết khóa học đã xuất bản.
- Tìm kiếm và lọc khóa học.
- Xem danh mục khóa học.
- Xem danh sách giảng viên nổi bật.
- Xem hồ sơ công khai của giảng viên và học viên.
- Đăng ký tài khoản.
- Đăng nhập vào hệ thống.

### Học viên

- Quản lý hồ sơ cá nhân, ảnh đại diện, tiểu sử và liên kết mạng xã hội.
- Duyệt, tìm kiếm và xem đánh giá khóa học.
- Thêm hoặc xóa khóa học khỏi giỏ hàng.
- Thanh toán từng khóa học hoặc thanh toán nhiều khóa học trong giỏ hàng.
- Đăng ký và tham gia khóa học.
- Xem chương học, bài giảng, video, nội dung và tài liệu đính kèm.
- Đánh dấu hoàn thành bài học.
- Theo dõi phần trăm tiến độ khóa học.
- Làm quiz và xem kết quả.
- Nộp bài tập bằng nội dung hoặc liên kết.
- Xem điểm và phản hồi từ giảng viên.
- Viết, cập nhật hoặc xóa đánh giá khóa học.
- Nhận và xem chứng chỉ hoàn thành.
- Xem lịch sử thanh toán.
- Nhắn tin trực tiếp hoặc theo nhóm.
- Sử dụng AI Assistant với tài liệu cá nhân.

### Giảng viên

- Tạo, chỉnh sửa, xuất bản và xóa khóa học.
- Quản lý tiêu đề, mô tả, ảnh đại diện, cấp độ, danh mục và giá khóa học.
- Tạo và sắp xếp chương học.
- Tạo bài học chứa video, tài liệu và nội dung.
- Tạo quiz.
- Tạo câu hỏi dạng:
  - Một lựa chọn.
  - Nhiều lựa chọn.
  - Văn bản.
- Tạo và quản lý đáp án.
- Tạo và chỉnh sửa bài tập.
- Xem danh sách bài nộp.
- Chấm điểm và gửi phản hồi.
- Xem và quản lý danh sách học viên của khóa học.
- Xóa học viên khỏi khóa học khi cần.
- Theo dõi thống kê khóa học và mức độ tương tác.
- Nhắn tin với học viên.
- Sử dụng AI Assistant với tài liệu cá nhân.

### Quản trị viên

- Đăng nhập vào Django Admin.
- Quản lý người dùng và vai trò.
- Quản lý các model đã đăng ký trong hệ thống.
- Theo dõi và chỉnh sửa dữ liệu ở cấp quản trị.

> Repository hiện chưa có dashboard quản trị riêng trên React. Các tác vụ quản trị hệ thống được thực hiện chủ yếu qua Django Admin.

---

## Trợ lý AI RAG

Module `rag` cung cấp tính năng hỏi đáp dựa trên tài liệu do từng người dùng tải lên.

### Luồng xử lý

```text
Người dùng tải tài liệu
        │
        ▼
Lưu file trong media/
        │
        ▼
Trích xuất nội dung
        │
        ▼
Chia văn bản thành các chunk
        │
        ▼
Tạo embedding bằng bge-m3
        │
        ▼
Lưu vector vào ChromaDB
        │
        ▼
Truy xuất các đoạn liên quan
        │
        ▼
Sinh câu trả lời bằng qwen2.5:3b
        │
        ▼
Trả về câu trả lời và nguồn trích dẫn
```

### Khả năng

- Tải lên tài liệu cá nhân.
- Hỗ trợ các định dạng:
  - PDF.
  - TXT.
  - DOCX.
  - PPTX.
- Theo dõi trạng thái xử lý:
  - `pending`.
  - `processing`.
  - `ready`.
  - `failed`.
- Tạo nhiều cuộc hội thoại.
- Chọn tài liệu dùng làm ngữ cảnh cho từng cuộc hội thoại.
- Lưu lịch sử tin nhắn.
- Trả về citation theo trang hoặc section khi có dữ liệu.
- Xóa, cập nhật hoặc lập chỉ mục lại tài liệu.
- Kiểm tra trạng thái Ollama, model và vector store.
- Cô lập dữ liệu RAG theo từng người dùng.

### Cấu hình mặc định

| Thành phần             | Giá trị mặc định         |
| ---------------------- | ------------------------ |
| LLM model              | `qwen2.5:3b`             |
| Embedding model        | `bge-m3`                 |
| Ollama URL             | `http://127.0.0.1:11434` |
| Chroma collection      | `lms_user_documents`     |
| Chunk size             | `1000`                   |
| Chunk overlap          | `180`                    |
| Top K                  | `6`                      |
| Maximum file size      | `30 MB`                  |
| Các định dạng cho phép | `pdf, txt, docx, pptx`   |

> Tính năng hiện không thực hiện OCR. PDF chỉ chứa ảnh hoặc tài liệu scan có thể không trích xuất được nội dung.

---

## Công nghệ sử dụng

### Backend cốt lõi

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
| PyJWT                 |         2.13.0 |

### Frontend

| Công nghệ        | Phiên bản |
| ---------------- | --------: |
| React            |    18.2.0 |
| React Router DOM |    6.20.0 |
| Axios            |     1.6.2 |
| Vite             |     5.0.8 |
| Tailwind CSS     |     3.4.0 |
| Recharts         |     3.5.1 |

### AI và xử lý tài liệu

| Công nghệ    | Vai trò                            |
| ------------ | ---------------------------------- |
| Ollama       | Chạy LLM và embedding model cục bộ |
| `qwen2.5:3b` | Sinh câu trả lời                   |
| `bge-m3`     | Tạo vector embedding               |
| ChromaDB     | Lưu trữ và tìm kiếm vector         |
| pypdf        | Đọc PDF                            |
| python-docx  | Đọc DOCX                           |
| python-pptx  | Đọc PPTX                           |

---

## Kiến trúc hệ thống

```text
┌─────────────────────────────────────┐
│ React + Vite + Tailwind CSS         │
│ http://localhost:5173               │
└──────────────────┬──────────────────┘
                   │ HTTP/JSON
                   │ Bearer JWT
                   ▼
┌─────────────────────────────────────┐
│ Django REST Framework               │
│ http://localhost:8000/api           │
├────────────────┬────────────────────┤
│ Django ORM     │ Media storage      │
│                │                    │
▼                ▼                    ▼
MySQL        lms_api/media/      RAG services
                                   │
                     ┌─────────────┴─────────────┐
                     ▼                           ▼
              Ollama models                 ChromaDB
           qwen2.5:3b + bge-m3        lms_api/chroma_db/
```

---

## Cấu trúc dự án

```text
LMS_DJANGO/
├── lms_api/
│   ├── lms_backend/       # Settings, URL và cấu hình Django
│   ├── users/             # User model, xác thực và hồ sơ
│   ├── courses/           # Khóa học, chương và bài học
│   ├── enrollments/       # Đăng ký, tiến độ, giỏ hàng và thanh toán
│   ├── assessments/       # Quiz, câu hỏi, bài tập và bài nộp
│   ├── reviews/           # Đánh giá khóa học
│   ├── analytics/         # Thống kê dành cho giảng viên
│   ├── chat/              # Hội thoại và tin nhắn
│   ├── rag/               # Document RAG, conversation và AI assistant
│   ├── common/            # Permission và thành phần dùng chung
│   ├── cert/              # Chứng chỉ CA cho kết nối MySQL
│   ├── chroma_db/         # Dữ liệu vector ChromaDB
│   ├── media/             # File do người dùng tải lên
│   └── manage.py
│
├── lms_frontend/
│   ├── src/
│   │   ├── api/           # Axios client và RAG API
│   │   ├── components/    # Component dùng chung
│   │   │   ├── chat/
│   │   │   ├── curriculum/
│   │   │   ├── lesson/
│   │   │   ├── profile/
│   │   │   ├── quiz/
│   │   │   └── rag/
│   │   ├── config/
│   │   ├── context/
│   │   ├── pages/         # Trang học viên, giảng viên, chat và AI
│   │   └── routes/        # Public và protected routes
│   └── package.json
│
├── requirements.txt       # Dependency backend cốt lõi
├── RAG.md                 # Tài liệu chi tiết về RAG
├── CHAT.md                # Tài liệu module chat
├── init_project.bat       # Cài dependency trên Windows
├── run_project.bat        # Khởi chạy backend và frontend trên Windows
└── README.md
```

---

## Mô hình dữ liệu

### LMS

```text
User
├── Course
│   └── Section
│       └── Lesson
├── Enrollment
│   ├── LessonProgress
│   └── Certificate
├── Quiz
│   ├── Question
│   │   └── Choice
│   └── StudentQuizAttempt
│       └── StudentAnswer
├── Assignment
│   └── Submission
├── CartItem
├── Payment
├── CourseReview
└── Conversation
    ├── ConversationParticipant
    └── Message
```

### RAG

```text
User
├── RagDocument
│   └── RagChunk
└── RagConversation
    └── RagMessage
```

---

## Hướng dẫn cài đặt

### Yêu cầu hệ thống

Cần cài đặt:

- Git.
- Python 3.10 trở lên.
- Node.js 18 trở lên.
- npm.
- MySQL Server 8 trở lên.
- Ollama nếu sử dụng AI Assistant.

### 1. Clone repository

```bash
git clone https://github.com/chienvoxn/LMS_DJANGO.git
cd LMS_DJANGO
```

### 2. Tạo môi trường ảo ở thư mục gốc

Các file `init_project.bat` và `run_project.bat` trong repository sử dụng thư mục `venv/` ở **thư mục gốc**, vì vậy nên tạo môi trường ảo tại đây.

```bash
python -m venv venv
```

Kích hoạt trên Windows:

```powershell
venv\Scripts\activate
```

Kích hoạt trên Linux hoặc macOS:

```bash
source venv/bin/activate
```

Cài backend dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Cài dependency cho RAG

Các thư viện RAG hiện chưa nằm trong `requirements.txt` chính. Cài bổ sung nếu sử dụng AI Assistant:

```bash
pip install "pypdf>=4.0" "chromadb>=0.5" "ollama>=0.3" "python-docx>=1.1" "python-pptx>=1.0"
```

Nếu không sử dụng AI Assistant, có thể bỏ qua bước cài Ollama và các dependency RAG.

### 4. Tạo MySQL database

Đăng nhập MySQL và chạy:

```sql
CREATE DATABASE lms_backend
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
```

### 5. Tạo file môi trường

Backend đọc biến môi trường từ:

```text
lms_api/.env.local
```

Repository hiện không có file `.env.example`, vì vậy hãy tạo thủ công file `lms_api/.env.local` với nội dung:

```dotenv
SECRET_KEY=replace_with_a_secure_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=lms_backend
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Tạo Django secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Sao chép giá trị được tạo và gán vào `SECRET_KEY`.

### 6. Cấu hình RAG tùy chọn

Có thể thêm các biến sau vào `lms_api/.env.local`:

```dotenv
RAG_CHROMA_PATH=chroma_db
RAG_COLLECTION_NAME=lms_user_documents

RAG_OLLAMA_BASE_URL=http://127.0.0.1:11434
RAG_LLM_MODEL=qwen2.5:3b
RAG_EMBED_MODEL=bge-m3

RAG_CHUNK_SIZE=1000
RAG_CHUNK_OVERLAP=180
RAG_TOP_K=6
RAG_MAX_DISTANCE=0.82
RAG_MAX_FILE_SIZE_MB=30
RAG_OLLAMA_TIMEOUT=180
```

Các biến này đều có giá trị mặc định trong `settings.py`, nên chỉ cần khai báo khi muốn thay đổi cấu hình. Danh sách định dạng `pdf`, `txt`, `docx` và `pptx` hiện được khai báo trực tiếp bằng `RAG_ALLOWED_EXTENSIONS` trong `settings.py`, không đọc từ biến môi trường.

### 7. Kiểm tra MySQL SSL

Cấu hình database hiện truyền chứng chỉ CA tại:

```text
lms_api/cert/ca.pem
```

Nếu sử dụng MySQL từ xa yêu cầu SSL, cần bảo đảm chứng chỉ hợp lệ.

Nếu sử dụng MySQL local không hỗ trợ hoặc không yêu cầu SSL, hãy điều chỉnh phần sau trong `lms_api/lms_backend/settings.py`:

```python
"OPTIONS": {
    "ssl": {
        "ca": str(BASE_DIR / "cert" / "ca.pem"),
    }
}
```

Chỉ nên bỏ cấu hình SSL trong môi trường local. Production nên sử dụng kết nối database được mã hóa.

### 8. Chạy migration

```bash
cd lms_api
python manage.py check
python manage.py migrate
python manage.py createsuperuser
```

### 9. Cài frontend

Từ thư mục gốc:

```bash
cd lms_frontend
npm install
```

---

## Khởi chạy dự án

### 1. Chạy Ollama

Cài và tải các model:

```bash
ollama pull bge-m3
ollama pull qwen2.5:3b
```

Khởi chạy Ollama nếu ứng dụng chưa tự chạy dưới dạng service:

```bash
ollama serve
```

> Ollama được cài riêng trên hệ điều hành, không được cài vào Python virtual environment.

### 2. Chạy backend

Từ thư mục gốc:

```bash
venv\Scripts\activate
cd lms_api
python manage.py runserver
```

Linux hoặc macOS:

```bash
source venv/bin/activate
cd lms_api
python manage.py runserver
```

### 3. Chạy frontend

Mở terminal khác:

```bash
cd lms_frontend
npm run dev
```

### Địa chỉ mặc định

| Dịch vụ      | URL                                  |
| ------------ | ------------------------------------ |
| Frontend     | `http://localhost:5173/`             |
| Backend API  | `http://127.0.0.1:8000/api/`         |
| Django Admin | `http://127.0.0.1:8000/admin/`       |
| AI Assistant | `http://localhost:5173/ai-assistant` |
| Ollama       | `http://127.0.0.1:11434/`            |

### Chạy nhanh trên Windows

Repository có hai script hỗ trợ:

```powershell
init_project.bat
run_project.bat
```

- `init_project.bat`: kích hoạt `venv`, cài Python dependencies và chạy `npm install`.
- `run_project.bat`: gọi script khởi tạo, sau đó mở backend và frontend trong hai cửa sổ terminal.

Các script này yêu cầu `venv/` nằm ở thư mục gốc repository.

---

## Xác thực JWT

Các API được bảo vệ nhận access token trong header:

```http
Authorization: Bearer <access_token>
```

Thời hạn mặc định:

| Token         | Thời hạn |
| ------------- | -------: |
| Access token  |    1 giờ |
| Refresh token |   7 ngày |

Frontend lưu token trong `localStorage`. Axios interceptor tự:

1. Gắn access token vào request.
2. Gọi `/api/auth/refresh/` khi server trả về `401`.
3. Lưu access token mới.
4. Chuyển người dùng về `/login` nếu refresh token không còn hợp lệ.

---

## API chính

### Tổng quan

| Nhóm                    | Endpoint chính                                   |
| ----------------------- | ------------------------------------------------ |
| Authentication          | `/api/auth/`                                     |
| Users và profile        | `/api/users/`                                    |
| Public courses          | `/api/courses/`                                  |
| Teacher courses         | `/api/teacher/courses/`                          |
| Teacher sections        | `/api/teacher/sections/`                         |
| Teacher lessons         | `/api/teacher/lessons/`                          |
| Enrollments và progress | `/api/enrollments/`, `/api/student/my-courses/`  |
| Cart và checkout        | `/api/enrollments/cart/`                         |
| Quiz                    | `/api/quizzes/`, `/api/teacher/quizzes/`         |
| Assignments             | `/api/assignments/`, `/api/teacher/assignments/` |
| Reviews                 | `/api/courses/{course_id}/reviews/`              |
| Certificates            | `/api/enrollments/me/certificates/`              |
| Teacher analytics       | `/api/teacher/analytics/`                        |
| Chat                    | `/api/chat/`                                     |
| RAG                     | `/api/rag/`                                      |

### Authentication

| Method | Endpoint                     | Chức năng               |
| ------ | ---------------------------- | ----------------------- |
| `POST` | `/api/auth/register/`        | Đăng ký tài khoản       |
| `POST` | `/api/auth/login/`           | Đăng nhập               |
| `POST` | `/api/auth/refresh/`         | Làm mới access token    |
| `GET`  | `/api/auth/me/`              | Lấy người dùng hiện tại |
| `POST` | `/api/auth/change-password/` | Đổi mật khẩu            |

### RAG

| Method             | Endpoint                                | Chức năng                       |
| ------------------ | --------------------------------------- | ------------------------------- |
| `GET`              | `/api/rag/health/`                      | Kiểm tra trạng thái RAG         |
| `GET`              | `/api/rag/documents/`                   | Lấy danh sách tài liệu          |
| `POST`             | `/api/rag/documents/`                   | Tải lên và lập chỉ mục tài liệu |
| `GET/PATCH/DELETE` | `/api/rag/documents/{id}/`              | Xem, cập nhật hoặc xóa tài liệu |
| `POST`             | `/api/rag/documents/{id}/reindex/`      | Lập chỉ mục lại tài liệu        |
| `GET/POST`         | `/api/rag/conversations/`               | Lấy hoặc tạo cuộc hội thoại     |
| `GET/PATCH/DELETE` | `/api/rag/conversations/{id}/`          | Quản lý cuộc hội thoại          |
| `GET/POST`         | `/api/rag/conversations/{id}/messages/` | Lấy lịch sử hoặc gửi câu hỏi    |

> Các endpoint có thể yêu cầu đăng nhập, đúng vai trò hoặc quyền sở hữu tài nguyên.

---

## Kiểm thử và quản trị RAG

### Backend

```bash
cd lms_api

python manage.py check
python manage.py test
python manage.py makemigrations --check
```

### Frontend

```bash
cd lms_frontend

npm run lint
npm run build
```

### Kiểm tra RAG

```bash
cd lms_api
python manage.py rag_health
```

Lập chỉ mục lại tài liệu RAG:

```bash
python manage.py reindex_rag
```

---

## Các lưu ý hiện tại

- `requirements.txt` chỉ chứa dependency backend cốt lõi, chưa chứa các package RAG.
- Repository không có `.env.example`; cần tự tạo `lms_api/.env.local`.
- Frontend hiện đặt cứng API base URL là `http://localhost:8000/api/` trong `lms_frontend/src/api/client.js`.
- Refresh endpoint cũng đang dùng URL `http://localhost:8000/api/auth/refresh/`.
- `CORS_ALLOW_ALL_ORIGINS=True` đang được bật trực tiếp trong Django settings.
- Payment là luồng thanh toán mô phỏng, không phải tích hợp cổng thanh toán thực.
- Media được lưu cục bộ trong `lms_api/media/`.
- Vector database được lưu cục bộ trong `lms_api/chroma_db/`.
- MySQL SSL CA đang được cấu hình trực tiếp trong `settings.py`.
- RAG không hỗ trợ OCR cho tài liệu scan.
- Frontend chưa có trang quản trị dành riêng cho admin.

---

## Bảo mật và triển khai

Trước khi triển khai production:

- Đặt `DEBUG=False`.
- Cấu hình chính xác `ALLOWED_HOSTS`.
- Thay `CORS_ALLOW_ALL_ORIGINS=True` bằng danh sách origin được phép.
- Không hard-code backend URL trong frontend; nên dùng biến môi trường Vite.
- Sử dụng secret key mạnh.
- Không commit `.env.local`, password, API key hoặc token.
- Sử dụng HTTPS.
- Bảo vệ thư mục media.
- Sử dụng object storage nếu cần lưu nhiều file.
- Dùng database account có quyền hạn tối thiểu cần thiết.
- Sao lưu MySQL và ChromaDB.
- Không dùng `python manage.py runserver` cho production.
- Dùng Gunicorn, Uvicorn hoặc server triển khai phù hợp.
- Cấu hình web server để phục vụ static và media files.
- Đánh giá tài nguyên phần cứng trước khi chạy local LLM cho nhiều người dùng.

Các mục quan trọng đã được `.gitignore` bỏ qua gồm:

```gitignore
venv/
.venv/
env/

.env
.env.local
.env.prod
.env.*.local

lms_api/media/
*.sqlite3
database.sql
```

---

## Tài liệu liên quan

- [RAG.md](./RAG.md): kiến trúc, cấu hình và cách vận hành AI Assistant.
- [CHAT.md](./CHAT.md): mô tả module hội thoại và tin nhắn.
- [Description.md](./Description.md): tài liệu mô tả dự án.
- [OPENCODE.md](./OPENCODE.md): ghi chú và hướng dẫn phát triển liên quan.

---

</div>
