# Đặc tả Yêu cầu Phần mềm (SRS) — Hệ thống Quản lý Học tập LMS_DJANGO

> **Phiên bản:** 2.0  
> **Ngày:** 13/07/2026  
> **Tác giả:** @chienvoxn, @Dathless  
> **Tuân chuẩn:** IEEE 29148-2018, IEEE 830-1998

---

## Lịch sử tài liệu (Document History)

| Phiên bản | Ngày       | Tác giả           | Mô tả thay đổi                                        |
| --------- | ---------- | ----------------- | ----------------------------------------------------- |
| 1.0       | 12/07/2026 | @chienvoxn        | Tạo lần đầu                                           |
| 2.0       | 13/07/2026 | @chienvoxn        | Bổ sung module RAG, cập nhật kiến trúc, API đầy đủ    |

---

## Mục lục (Table of Contents)

1. [Giới thiệu (Introduction)](#phần-i--giới-thiệu-introduction)
2. [Mô tả tổng quan (Overall Description)](#phần-ii--mô-tả-tổng-quan-overall-description)
3. [Yêu cầu chức năng (Functional Requirements)](#phần-iii--yêu-cầu-chức-năng-functional-requirements)
4. [Yêu cầu phi chức năng (Non-Functional Requirements)](#phần-iv--yêu-cầu-phi-chức-năng-non-functional-requirements)
5. [Thiết kế hệ thống & Kiến trúc kỹ thuật](#phần-v--thiết-kế-hệ-thống--kiến-trúc-kỹ-thuật)
6. [Sơ đồ UML](#phần-vi--sơ-đồ-uml)
7. [Ma trận truy vết yêu cầu](#phần-vii--ma-trận-truy-vết-yêu-cầu-requirements-traceability-matrix)
8. [Kế hoạch kiểm thử](#phần-viii--kế-hoạch-kiểm-thử-tóm-tắt)
9. [Phụ lục](#phần-ix--phụ-lục)

---

## Phần I — Giới thiệu (Introduction)

### 1. Mục đích tài liệu (Purpose)

Tài liệu này đặc tả chi tiết yêu cầu chức năng và phi chức năng cho hệ thống **LMS_DJANGO — Learning Management System**. Đây là tài liệu tham chiếu duy nhất cho đội ngũ phát triển, kiểm thử và các bên liên quan trong suốt vòng đời dự án.

### 2. Phạm vi sản phẩm (Scope)

**LMS_DJANGO** là nền tảng học trực tuyến toàn diện với 4 nhóm người dùng:

- **Khách (Guest):** Xem danh sách/chi tiết khóa học, tìm kiếm, xem hồ sơ công khai giảng viên/học viên.
- **Học viên (Student):** Đăng ký, tìm kiếm khóa học, ghi danh (miễn phí/trả phí/audit), theo dõi tiến độ, làm bài kiểm tra/bài tập, nhận chứng chỉ, đánh giá khóa học, nhắn tin với giảng viên, sử dụng trợ lý AI (RAG) trên tài liệu cá nhân.
- **Giảng viên (Teacher):** Tạo và quản lý khóa học (bài giảng, chương mục), tạo bài kiểm tra/bài tập, chấm điểm, quản lý học viên, xem thống kê phân tích, sử dụng trợ lý AI (RAG).
- **Quản trị viên (Admin):** Quản lý tài khoản, vai trò và quyền truy cập qua Django Admin.

**Nằm trong phạm vi:**
- Quản lý xác thực & phân quyền (JWT, role-based)
- Quản lý khóa học, chương (section), bài học (lesson)
- Ghi danh & theo dõi tiến độ học tập
- Bài kiểm tra trắc nghiệm (quiz) & bài tập tự luận (assignment)
- Đánh giá/xếp hạng khóa học
- Giỏ hàng & thanh toán mô phỏng
- Chứng chỉ hoàn thành khóa học
- Nhắn tin (1-1 và nhóm)
- Phân tích thống kê cho giảng viên
- Hồ sơ công khai cho học viên & giảng viên
- **Trợ lý AI (RAG):** Tải tài liệu PDF/TXT/DOCX/PPTX, hỏi đáp, tóm tắt, tạo flashcard dựa trên nội dung tài liệu cá nhân

**Ngoài phạm vi:**
- Tích hợp cổng thanh toán thật (Stripe/PayPal...)
- Hỗ trợ đa ngôn ngữ giao diện (frontend i18n)
- Phát trực tiếp (livestream)
- Hệ thống thông báo push/email
- Thi hỗ trợ giám thị (proctoring)
- WebSocket real-time chat (hiện dùng polling)
- OCR cho PDF scan

### 3. Định nghĩa, từ viết tắt, thuật ngữ (Definitions, Acronyms)

| Thuật ngữ              | Giải thích                                                          |
| ---------------------- | ------------------------------------------------------------------- |
| **SRS**                | Software Requirements Specification                                 |
| **JWT**                | JSON Web Token — xác thực người dùng                                |
| **DRF**                | Django REST Framework                                               |
| **CRUD**               | Create, Read, Update, Delete                                        |
| **Role**               | Vai trò người dùng: student / teacher / admin                       |
| **Enrollment**         | Ghi danh (bản ghi học viên tham gia khóa học)                       |
| **Section**            | Chương trong khóa học                                               |
| **Lesson**             | Bài học trong chương                                                |
| **Quiz**               | Bài kiểm tra trắc nghiệm                                            |
| **Assignment**         | Bài tập tự luận/nộp file                                            |
| **Submission**         | Bài nộp của học viên cho Assignment                                 |
| **Certificate**        | Chứng chỉ hoàn thành khóa học                                       |
| **CartItem**           | Mục trong giỏ hàng                                                  |
| **Payment**            | Giao dịch thanh toán                                                |
| **RAG**                | Retrieval-Augmented Generation — kỹ thuật truy xuất và sinh văn bản |
| **ChromaDB**           | Vector database lưu embedding                                       |
| **Ollama**             | Local AI inference server                                           |
| **Embedding**          | Vector biểu diễn ngữ nghĩa của văn bản                              |
| **LLM**                | Large Language Model                                                |
| **Chunk**              | Đoạn văn bản nhỏ được cắt từ tài liệu gốc                          |
| **Citation**           | Trích dẫn nguồn tài liệu trong câu trả lời AI                      |
| **IDOR**               | Insecure Direct Object Reference — lỗ hổng bảo mật                  |

### 4. Tài liệu tham khảo (References)

1. IEEE 29148-2018 — Systems and software engineering — Life cycle processes
2. IEEE 830-1998 — Recommended Practice for Software Requirements Specifications
3. [Django REST Framework Documentation](https://www.django-rest-framework.org/)
4. [React Documentation](https://react.dev/)
5. [SimpleJWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)
6. [ChromaDB Documentation](https://docs.trychroma.com/)
7. [Ollama Documentation](https://ollama.ai/)
8. Mã nguồn dự án: [github.com/chienvoxn/LMS_DJANGO](https://github.com/chienvoxn/LMS_DJANGO)

### 5. Tổng quan tài liệu (Document Overview)

Tài liệu gồm 9 phần: Giới thiệu → Mô tả tổng quan → Yêu cầu chức năng → Yêu cầu phi chức năng → Thiết kế hệ thống & Kiến trúc → Sơ đồ UML → Ma trận truy vết → Kế hoạch kiểm thử → Phụ lục.

---

## Phần II — Mô tả tổng quan (Overall Description)

### 1. Bối cảnh sản phẩm (Product Perspective)

LMS_DJANGO là hệ thống mới phát triển từ đầu, kiến trúc **client-server** tách biệt hoàn toàn frontend và backend:

- **Backend API:** Django 5.2.7 + Django REST Framework 3.16.1 — cung cấp RESTful API
- **Frontend SPA:** React 18.2 + Vite 5.0 + Tailwind CSS 3.4 — giao diện người dùng
- **Cơ sở dữ liệu:** MySQL 8.0+
- **Xác thực:** JWT (SimpleJWT 5.5.1) — access token 1 giờ, refresh token 7 ngày
- **AI:** Ollama (bge-m3 embedding + qwen2.5:3b LLM) + ChromaDB vector store

Người dùng truy cập qua trình duyệt web. Frontend gọi API backend qua HTTP, backend trả JSON.

### 2. Chức năng chính của sản phẩm (Product Functions)

1. **Xác thực & quản lý người dùng** — đăng ký, đăng nhập, đổi mật khẩu, hồ sơ cá nhân, hồ sơ công khai
2. **Quản lý khóa học** — xem danh sách, chi tiết, tìm kiếm, lọc theo danh mục/cấp độ
3. **Quản lý chương/bài học** — CRUD chương (section), bài học (lesson) cho giảng viên
4. **Ghi danh & theo dõi tiến độ** — ghi danh miễn phí/trả phí/audit, đánh dấu bài học đã hoàn thành, tính % tiến độ
5. **Giỏ hàng & thanh toán** — thêm/xóa khóa học, checkout mô phỏng
6. **Bài kiểm tra (Quiz)** — tạo câu hỏi trắc nghiệm (single/multiple choice), làm bài, chấm điểm tự động
7. **Bài tập (Assignment)** — tạo bài tập, nộp bài kèm file, chấm điểm và phản hồi từ giảng viên
8. **Chứng chỉ** — cấp chứng chỉ khi hoàn thành khóa học trả phí với mã code unique
9. **Đánh giá khóa học** — xếp hạng 1-5 sao, bình luận
10. **Nhắn tin** — tạo hội thoại 1-1/nhóm, gửi/nhận tin nhắn, polling 5 giây
11. **Phân tích giảng viên** — thống kê tổng quan, theo khóa học, chuỗi thời gian, mức độ tương tác
12. **Hồ sơ công khai** — hồ sơ học viên & giảng viên (xem được mà không cần đăng nhập)
13. **Trợ lý AI (RAG)** — tải tài liệu cá nhân, hỏi đáp dựa trên nội dung tài liệu, tóm tắt, tạo flashcard, citation kèm nguồn

### 3. Đối tượng người dùng và đặc điểm (User Classes and Characteristics)

| Lớp người dùng      | Mô tả                     | Đặc điểm                                                                                  |
| ------------------- | ------------------------- | ----------------------------------------------------------------------------------------- |
| **Guest**           | Khách                     | Xem danh sách/chi tiết khóa học, hồ sơ công khai, không cần đăng nhập                     |
| **Student**         | Học viên                  | Đăng ký tài khoản, ghi danh khóa học, làm bài kiểm tra, nộp bài tập, nhận chứng chỉ, dùng AI Assistant |
| **Teacher**         | Giảng viên                | Tạo/quản lý khóa học, bài kiểm tra, bài tập, chấm điểm, xem thống kê, dùng AI Assistant   |
| **Admin**           | Quản trị viên             | Quản lý tài khoản, vai trò và toàn bộ dữ liệu qua Django Admin                            |

### 4. Môi trường vận hành (Operating Environment)

| Thành phần   | Công nghệ                                           |
| ------------ | --------------------------------------------------- |
| **Backend**  | Python 3.10+, Django 5.2.7, Gunicorn/uWSGI + Nginx |
| **Frontend** | React 18.2, Chrome/Firefox/Edge/Safari (bản mới nhất) |
| **Database** | MySQL 8.0+ với SSL connection                        |
| **AI**       | Ollama server (bge-m3 + qwen2.5:3b), ChromaDB persistent |
| **Dev**      | Django runserver (port 8000) + Vite dev server (port 3000) |
| **Storage**  | Local media storage (production: S3/CDN)             |

### 5. Ràng buộc thiết kế/triển khai (Design and Implementation Constraints)

- **Backend framework:** Django REST Framework (bắt buộc)
- **Frontend framework:** React 18 + Vite (bắt buộc)
- **Xác thực:** JWT qua SimpleJWT, email-based authentication
- **Cơ sở dữ liệu:** MySQL (bắt buộc SSL)
- **AI:** Ollama local server (bge-m3 + qwen2.5:3b), ChromaDB
- **Mã nguồn:** Tuân thủ PEP 8 (Python)
- **CORS:** Mở toàn bộ origin ở development
- **Pagination:** PageNumberPagination, 10 items/trang (mặc định)

### 6. Giả định và phụ thuộc (Assumptions and Dependencies)

- **Giả định:** Người dùng có kết nối internet ổn định
- **Giả định:** Thanh toán được mô phỏng (không tích hợp cổng thanh toán thật)
- **Giả định:** MySQL đã được cài đặt và cấu hình SSL
- **Giả định:** Ollama được cài đặt và chạy nền với 2 model
- **Phụ thuộc Backend:** `django`, `djangorestframework`, `djangorestframework-simplejwt`, `mysqlclient`, `django-cors-headers`, `python-dotenv`, `chromadb`, `ollama`, `pypdf`, `python-docx`, `python-pptx`
- **Phụ thuộc Frontend:** `react`, `react-router-dom`, `axios`, `recharts`, `tailwindcss`

---

## Phần III — Yêu cầu chức năng (Functional Requirements)

### Module 1: Xác thực & Quản lý Người dùng

#### FR-01: Đăng ký tài khoản

| Mục                      | Mô tả                                                                                                                                                                                                                                                      |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu**           | FR-01                                                                                                                                                                                                                                                      |
| **Mô tả**                | Người dùng mới đăng ký tài khoản với email, mật khẩu, họ tên, vai trò                                                                                                                                                                                      |
| **Actor**                | Guest                                                                                                                                                                                                                                                      |
| **Điều kiện tiên quyết** | Email chưa tồn tại trong hệ thống                                                                                                                                                                                                                          |
| **Luồng chính**          | 1. Người dùng nhập email, password, password_confirm, full_name, role. 2. Hệ thống kiểm tra email unique. 3. Hệ thống kiểm tra password khớp. 4. Hệ thống tạo User mới với password đã hash. 5. Hệ thống sinh JWT tokens (access + refresh). 6. Trả về user info + tokens. |
| **Luồng thay thế**       | Email đã tồn tại → 400 "A user with this email already exists". Password không khớp → 400 "Passwords do not match".                                                                                                                                        |
| **Điều kiện sau**        | Tài khoản được tạo, người dùng tự động đăng nhập                                                                                                                                                                                                           |
| **Business rules**       | Password tối thiểu 8 ký tự. Endpoint: `POST /api/auth/register/`. Role mặc định: `student`.                                                                                                                                                                |

#### FR-02: Đăng nhập

| Mục                      | Mô tả                                                                                           |
| ------------------------ | ----------------------------------------------------------------------------------------------- |
| **Mã yêu cầu**           | FR-02                                                                                           |
| **Mô tả**                | Người dùng đăng nhập bằng email và password, nhận JWT tokens                                    |
| **Actor**                | Student, Teacher                                                                                |
| **Điều kiện tiên quyết** | Tài khoản đã tồn tại                                                                            |
| **Luồng chính**          | 1. Người dùng gửi email + password. 2. Hệ thống xác thực. 3. Trả về access_token + refresh_token. |
| **Luồng thay thế**       | Sai email/password → 401 Unauthorized                                                           |
| **Điều kiện sau**        | Access token có hiệu lực 1 giờ, refresh token 7 ngày                                            |
| **Business rules**       | Endpoint: `POST /api/auth/login/`. Sử dụng email mapping cho SimpleJWT username field.          |

#### FR-03: Xem thông tin người dùng hiện tại

| Mục                | Mô tả                                                     |
| ------------------ | --------------------------------------------------------- |
| **Mã yêu cầu**     | FR-03                                                     |
| **Mô tả**          | Xem thông tin người dùng đang đăng nhập                   |
| **Actor**          | Student, Teacher                                          |
| **Endpoint**       | `GET /api/auth/me/`                                       |
| **Response**       | id, email, full_name, role, avatar_url, bio, headline, ... |

#### FR-04: Xem/Cập nhật hồ sơ cá nhân

| Mục                | Mô tả                                                                                                          |
| ------------------ | -------------------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu**     | FR-04                                                                                                          |
| **Mô tả**          | Người dùng xem và cập nhật thông tin hồ sơ của mình (avatar, bio, headline, country, social_links)             |
| **Actor**          | Student, Teacher                                                                                               |
| **Endpoint**       | `GET/PUT/PATCH /api/users/me/profile/`                                                                         |
| **Luồng chính**    | 1. GET lấy thông tin hồ sơ. 2. PUT/PATCH cập nhật một hoặc nhiều trường.                                      |
| **Điều kiện sau**  | Hồ sơ được cập nhật                                                                                            |
| **Business rules** | Chỉ chủ sở hữu mới được cập nhật. Social_links phải là dict với các key: facebook, linkedin, github, website. |

#### FR-05: Xem hồ sơ công khai

| Mục                | Mô tả                                                                                                                                                                                            |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Mã yêu cầu**     | FR-05                                                                                                                                                                                            |
| **Mô tả**          | Xem hồ sơ công khai của học viên hoặc giảng viên mà không cần đăng nhập                                                                                                                          |
| **Actor**          | Guest, Student, Teacher                                                                                                                                                                          |
| **Endpoint**       | `GET /api/students/{id}/profile/`, `GET /api/instructors/{id}/profile/`                                                                                                                          |
| **Luồng chính**    | 1. Người dùng gửi yêu cầu. 2. Hệ thống trả về thông tin + thống kê.                                                                                                                             |
| **Business rules** | Instructor profile: thống kê khóa học, rating, số học viên. Student profile: danh sách khóa học đã ghi danh kèm tiến độ.                                                                         |

#### FR-06: Đổi mật khẩu

| Mục                | Mô tả                                                                                                    |
| ------------------ | -------------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu**     | FR-06                                                                                                    |
| **Mô tả**          | Người dùng đã xác thực đổi mật khẩu                                                                      |
| **Actor**          | Student, Teacher                                                                                         |
| **Endpoint**       | `POST /api/auth/change-password/`                                                                        |
| **Business rules** | Yêu cầu old_password + new_password. Mật khẩu mới phải khác mật khẩu cũ. Django password validators.     |

#### FR-07: Top giảng viên

| Mục            | Mô tả                                                  |
| -------------- | ------------------------------------------------------ |
| **Mã yêu cầu** | FR-07                                                  |
| **Mô tả**      | Xem top 10 giảng viên xếp theo số học viên hoặc rating |
| **Actor**      | Guest                                                  |
| **Endpoint**   | `GET /api/instructors/top/?sort=students\|rating`      |

---

### Module 2: Quản lý Khóa học

#### FR-08: Xem danh sách khóa học (công khai)

| Mục                | Mô tả                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------- |
| **Mã yêu cầu**     | FR-08                                                                                 |
| **Mô tả**          | Xem danh sách khóa học đã xuất bản, hỗ trợ tìm kiếm, lọc theo category/level, sắp xếp |
| **Actor**          | Guest, Student, Teacher                                                               |
| **Endpoint**       | `GET /api/courses/`                                                                   |
| **Query params**   | `search`, `category`, `level`, `ordering`, `page`                                     |
| **Business rules** | Chỉ hiện khóa học có `is_published=True`. Phân trang 10 khóa học/trang. Search trên title, subtitle, description. |

#### FR-09: Xem chi tiết khóa học

| Mục            | Mô tả                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu** | FR-09                                                                                             |
| **Mô tả**      | Xem chi tiết khóa học gồm rating trung bình, số review, thông tin giảng viên, trạng thái ghi danh |
| **Actor**      | Guest, Student, Teacher                                                                           |
| **Endpoint**   | `GET /api/courses/{id}/`                                                                          |

#### FR-10: Xem chương trình học (curriculum)

| Mục            | Mô tả                                                                                                                |
| -------------- | -------------------------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu** | FR-10                                                                                                                |
| **Mô tả**      | Xem cấu trúc khóa học: danh sách section và lesson kèm trạng thái hoàn thành nếu đã ghi danh                         |
| **Actor**      | Guest (xem cấu trúc), Student (xem trạng thái hoàn thành)                                                            |
| **Endpoint**   | `GET /api/courses/{id}/curriculum/`                                                                                  |

#### FR-11: Xem danh mục khóa học

| Mục            | Mô tả                                                           |
| -------------- | --------------------------------------------------------------- |
| **Mã yêu cầu** | FR-11                                                           |
| **Mô tả**      | Lấy danh sách các category duy nhất từ các khóa học đã xuất bản |
| **Actor**      | Guest, Student, Teacher                                         |
| **Endpoint**   | `GET /api/courses/categories/`                                  |

#### FR-12: Xem chi tiết bài học (yêu cầu ghi danh)

| Mục                | Mô tả                                                        |
| ------------------ | ------------------------------------------------------------ |
| **Mã yêu cầu**     | FR-12                                                        |
| **Mô tả**          | Xem nội dung bài học (video, tài liệu, content)              |
| **Actor**          | Student                                                      |
| **Endpoint**       | `GET /api/lessons/{id}/`                                     |
| **Business rules** | Yêu cầu học viên đã ghi danh khóa học. 403 nếu chưa ghi danh.|

#### FR-13: Quản lý khóa học (Giảng viên)

| Mục                | Mô tả                                                                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu**     | FR-13                                                                                                                                       |
| **Mô tả**          | Giảng viên tạo, xem, sửa, xóa khóa học, section, lesson                                                                                    |
| **Actor**          | Teacher                                                                                                                                     |
| **Endpoints**      | `GET/POST /api/teacher/courses/`, `GET/PUT/PATCH/DELETE /api/teacher/courses/{id}/` (kèm sections, lessons)                                 |
| **Business rules** | Chỉ giảng viên mới có quyền. Chỉ sửa/xóa khóa học của chính mình (`IsOwnerOrReadOnly`). Section và lesson được quản lý qua nested routes. |

---

### Module 3: Ghi danh & Tiến độ

#### FR-14: Ghi danh khóa học miễn phí

| Mục                      | Mô tả                                                          |
| ------------------------ | -------------------------------------------------------------- |
| **Mã yêu cầu**           | FR-14                                                          |
| **Mô tả**                | Học viên ghi danh vào khóa học miễn phí (price = 0)           |
| **Actor**                | Student                                                        |
| **Endpoint**             | `POST /api/courses/{course_id}/enroll/`                        |
| **Điều kiện tiên quyết** | Khóa học tồn tại và đã xuất bản. Người dùng có role 'student'. |
| **Luồng thay thế**       | Đã ghi danh → 400 "You are already enrolled"                   |
| **Điều kiện sau**        | Enrollment created, progress_percent = 0                       |

#### FR-15: Ghi danh khóa học trả phí / Audit

| Mục                | Mô tả                                                                                            |
| ------------------ | ------------------------------------------------------------------------------------------------ |
| **Mã yêu cầu**     | FR-15                                                                                            |
| **Mô tả**          | Học viên mua khóa học (paid) hoặc ghi danh kiểu audit (miễn phí, không chứng chỉ)               |
| **Actor**          | Student                                                                                          |
| **Endpoint**       | `POST /api/courses/{course_id}/purchase/`                                                        |
| **Body**           | `{"mode": "audit" \| "paid"}`                                                                    |
| **Business rules** | Có thể nâng cấp từ audit lên paid. Không thể mua khóa học của chính mình.                        |

#### FR-16: Đánh dấu bài học hoàn thành

| Mục               | Mô tả                                                                                    |
| ----------------- | ---------------------------------------------------------------------------------------- |
| **Mã yêu cầu**    | FR-16                                                                                    |
| **Mô tả**         | Học viên đánh dấu bài học đã hoàn thành. Hệ thống tự động tính % tiến độ khóa học.       |
| **Actor**         | Student                                                                                  |
| **Endpoint**      | `POST /api/lessons/{lesson_id}/complete/`                                                |
| **Điều kiện sau** | `progress_percent` = (completed_lessons / total_lessons) * 100. Không thể > 100.         |

#### FR-17: Xem khóa học của tôi

| Mục            | Mô tả                                                                         |
| -------------- | ----------------------------------------------------------------------------- |
| **Mã yêu cầu** | FR-17                                                                         |
| **Mô tả**      | Xem danh sách khóa học đã ghi danh kèm tiến độ, bài học cuối cùng đã truy cập |
| **Actor**      | Student                                                                       |
| **Endpoint**   | `GET /api/student/my-courses/`                                                |

#### FR-18: Xem danh sách học viên (Giảng viên)

| Mục              | Mô tả                                                                                                             |
| ---------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu**   | FR-18                                                                                                             |
| **Mô tả**        | Giảng viên xem danh sách học viên trong khóa học kèm tiến độ, số quiz đã làm, số assignment đã nộp               |
| **Actor**        | Teacher                                                                                                           |
| **Endpoint**     | `GET /api/teacher/courses/{course_id}/students/`                                                                  |
| **Query params** | `q` (tìm kiếm theo tên/email), `status` (completed/in_progress)                                                   |

#### FR-19: Xóa học viên khỏi khóa học

| Mục            | Mô tả                                                                                                   |
| -------------- | ------------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu** | FR-19                                                                                                   |
| **Mô tả**      | Giảng viên xóa học viên khỏi khóa học (xóa toàn bộ dữ liệu liên quan: progress, quiz attempts, submissions) |
| **Actor**      | Teacher                                                                                                 |
| **Endpoint**   | `DELETE /api/teacher/courses/{course_id}/students/{student_id}/`                                        |

---

### Module 4: Giỏ hàng & Thanh toán

#### FR-20: Quản lý giỏ hàng

| Mục                | Mô tả                                                                                              |
| ------------------ | -------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu**     | FR-20                                                                                              |
| **Mô tả**          | Học viên xem giỏ hàng, thêm khóa học, xóa khóa học khỏi giỏ                                       |
| **Actor**          | Student                                                                                            |
| **Endpoints**      | `GET /api/enrollments/cart/`, `POST /api/enrollments/cart/add/`, `DELETE /api/enrollments/cart/items/{id}/` |
| **Business rules** | Không thể thêm khóa học của chính mình. Không thể thêm khóa học đã sở hữu. Tự động lấy giá hiện tại. |

#### FR-21: Thanh toán giỏ hàng

| Mục                | Mô tả                                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu**     | FR-21                                                                                             |
| **Mô tả**          | Học viên thanh toán toàn bộ hoặc một số mục trong giỏ hàng (mô phỏng)                             |
| **Actor**          | Student                                                                                           |
| **Endpoint**       | `POST /api/enrollments/cart/checkout/`                                                            |
| **Body**           | `{"item_ids": [1, 2]}` (optional, mặc định thanh toán tất cả)                                     |
| **Business rules** | Thanh toán luôn thành công. Tạo Payment record với status="succeeded". Tạo Enrollment với enrollment_type="paid". |

#### FR-22: Xem lịch sử thanh toán

| Mục            | Mô tả                                 |
| -------------- | ------------------------------------- |
| **Mã yêu cầu** | FR-22                                 |
| **Mô tả**      | Xem lịch sử thanh toán của người dùng |
| **Actor**      | Student                               |
| **Endpoint**   | `GET /api/enrollments/me/payments/`   |

---

### Module 5: Bài kiểm tra (Quiz)

#### FR-23: Quản lý Quiz (Giảng viên)

| Mục                | Mô tả                                                                                                                                 |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu**     | FR-23                                                                                                                                 |
| **Mô tả**          | Giảng viên CRUD quiz, thêm/sửa/xóa câu hỏi và lựa chọn                                                                               |
| **Actor**          | Teacher                                                                                                                               |
| **Endpoints**      | `POST/GET /api/teacher/quizzes/`, `GET/PUT/PATCH/DELETE /api/teacher/quizzes/{id}/`, kèm questions, choices endpoints                 |
| **Business rules** | Quiz gắn với một khóa học. 2 quiz types: Foundations Quiz và Applied Skills Quiz. Hỗ trợ single_choice, multiple_choice question types. |

#### FR-24: Làm bài kiểm tra (Học viên)

| Mục                | Mô tả                                                                                                                                                                  |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu**     | FR-24                                                                                                                                                                  |
| **Mô tả**          | Học viên xem danh sách quiz, bắt đầu làm quiz, nộp bài và nhận điểm tự động                                                                                            |
| **Actor**          | Student                                                                                                                                                                |
| **Flow**           | 1. `GET /api/courses/{id}/quizzes/` → 2. `GET /api/quizzes/{id}/` (ẩn đáp án) → 3. `POST /api/quizzes/{id}/start/` → 4. `POST /api/quizzes/{id}/submit/`              |
| **Business rules** | StudentAnswer không hiện `is_correct` khi làm bài. Quiz được chấm dựa trên tổng điểm các câu đúng. Hỗ trợ auto-save quiz progress vào localStorage.                    |

#### FR-25: Xem lịch sử làm quiz

| Mục            | Mô tả                                     |
| -------------- | ----------------------------------------- |
| **Mã yêu cầu** | FR-25                                     |
| **Mô tả**      | Xem các lần làm bài kiểm tra của bản thân |
| **Actor**      | Student                                   |
| **Endpoint**   | `GET /api/quizzes/{id}/attempts/me/`      |

---

### Module 6: Bài tập (Assignment)

#### FR-26: Quản lý Assignment (Giảng viên)

| Mục                | Mô tả                                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| **Mã yêu cầu**     | FR-26                                                                                                                    |
| **Mô tả**          | Giảng viên CRUD assignment, xem bài nộp của học viên, chấm điểm                                                          |
| **Actor**          | Teacher                                                                                                                  |
| **Endpoints**      | Teacher CRUD: `POST/GET /api/teacher/assignments/`, `GET /api/teacher/assignments/{id}/submissions/`, `PATCH /api/teacher/submissions/{id}/grade/` |
| **Business rules** | Assignment có due_date, max_points, attachment_url. Grading gồm grade + feedback.                                        |

#### FR-27: Nộp bài tập (Học viên)

| Mục                | Mô tả                                                                          |
| ------------------ | ------------------------------------------------------------------------------ |
| **Mã yêu cầu**     | FR-27                                                                          |
| **Mô tả**          | Học viên nộp bài tập (text/file), xem lại bài nộp và điểm                      |
| **Actor**          | Student                                                                        |
| **Endpoints**      | `POST /api/assignments/{id}/submit/`, `GET /api/assignments/{id}/my-submission/` |
| **Business rules** | Mỗi học viên chỉ nộp một lần. Nếu đã chấm điểm (graded) thì không thể sửa.     |

#### FR-28: Upload file

| Mục            | Mô tả                                                                                        |
| -------------- | -------------------------------------------------------------------------------------------- |
| **Mã yêu cầu** | FR-28                                                                                        |
| **Mô tả**      | Upload file lên server, trả về URL (dùng cho assignment submission, lesson document, avatar) |
| **Actor**      | Student, Teacher                                                                             |
| **Endpoint**   | `POST /api/upload/`                                                                          |
| **Business rules** | File được lưu với tên UUID. Trả về URL của file đã upload.                               |

---

### Module 7: Chứng chỉ

#### FR-29: Cấp chứng chỉ

| Mục                      | Mô tả                                                                        |
| ------------------------ | ---------------------------------------------------------------------------- |
| **Mã yêu cầu**           | FR-29                                                                        |
| **Mô tả**                | Học viên yêu cầu cấp chứng chỉ sau khi hoàn thành khóa học trả phí           |
| **Actor**                | Student                                                                      |
| **Endpoint**             | `POST /api/courses/{course_id}/certificate/issue/`                           |
| **Điều kiện tiên quyết** | Enrollment type = 'paid', progress_percent = 100%                            |
| **Điều kiện sau**        | Certificate được tạo với mã code UUID hex[:32]. enrollment.granted_certificate = True |

#### FR-30: Xem chứng chỉ

| Mục            | Mô tả                                                                                   |
| -------------- | --------------------------------------------------------------------------------------- |
| **Mã yêu cầu** | FR-30                                                                                   |
| **Mô tả**      | Xem chứng chỉ của một khóa học hoặc danh sách chứng chỉ                                 |
| **Actor**      | Student                                                                                 |
| **Endpoints**  | `GET /api/courses/{course_id}/certificate/me/`, `GET /api/enrollments/me/certificates/` |

---

### Module 8: Đánh giá khóa học

#### FR-31: Đánh giá khóa học

| Mục                | Mô tả                                                                                         |
| ------------------ | --------------------------------------------------------------------------------------------- |
| **Mã yêu cầu**     | FR-31                                                                                         |
| **Mô tả**          | Học viên tạo/cập nhật/xóa đánh giá (rating 1-5 + bình luận) cho khóa học đã ghi danh          |
| **Actor**          | Student                                                                                       |
| **Endpoints**      | `GET/POST /api/courses/{course_id}/reviews/`, `GET/PUT/PATCH/DELETE /api/reviews/{id}/`       |
| **Business rules** | Mỗi học viên chỉ một review mỗi khóa học. Yêu cầu đã ghi danh.                               |

#### FR-32: Xem rating tổng quan

| Mục            | Mô tả                                                |
| -------------- | ---------------------------------------------------- |
| **Mã yêu cầu** | FR-32                                                |
| **Mô tả**      | Xem rating trung bình và tổng số review của khóa học |
| **Actor**      | Guest, Student, Teacher                              |
| **Endpoint**   | `GET /api/courses/{course_id}/rating-summary/`       |

---

### Module 9: Nhắn tin

#### FR-33: Quản lý hội thoại

| Mục                | Mô tả                                                                              |
| ------------------ | ---------------------------------------------------------------------------------- |
| **Mã yêu cầu**     | FR-33                                                                              |
| **Mô tả**          | Xem danh sách hội thoại, tạo hội thoại mới (1-1 hoặc nhóm)                         |
| **Actor**          | Student, Teacher                                                                   |
| **Endpoints**      | `GET/POST /api/chat/conversations/`, `GET /api/chat/conversations/{id}/`           |
| **Business rules** | Hội thoại 1-1 tự động tái sử dụng nếu đã tồn tại. Hội thoại nhóm khi có > 2 người. |

#### FR-34: Gửi & nhận tin nhắn

| Mục                | Mô tả                                                          |
| ------------------ | -------------------------------------------------------------- |
| **Mã yêu cầu**     | FR-34                                                          |
| **Mô tả**          | Gửi tin nhắn trong hội thoại, xem danh sách tin nhắn           |
| **Actor**          | Student, Teacher                                               |
| **Endpoints**      | `GET/POST /api/chat/conversations/{id}/messages/`              |
| **Business rules** | Chỉ thành viên hội thoại mới xem/gửi tin nhắn. Polling 5 giây. |

#### FR-35: Đếm hội thoại chưa đọc

| Mục            | Mô tả                                  |
| -------------- | -------------------------------------- |
| **Mã yêu cầu** | FR-35                                  |
| **Mô tả**      | Đếm số hội thoại chưa đọc của người dùng |
| **Actor**      | Student, Teacher                       |
| **Endpoint**   | `GET /api/chat/unread-count/`          |

---

### Module 10: Phân tích Giảng viên

#### FR-36: Thống kê tổng quan

| Mục            | Mô tả                                                                                                           |
| -------------- | --------------------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu** | FR-36                                                                                                           |
| **Mô tả**      | Xem thống kê tổng quan: tổng khóa học, tổng ghi danh, tổng học viên, rating trung bình, doanh thu, số chứng chỉ |
| **Actor**      | Teacher                                                                                                         |
| **Endpoint**   | `GET /api/teacher/analytics/summary/`                                                                           |

#### FR-37: Thống kê theo khóa học

| Mục            | Mô tả                                                                      |
| -------------- | -------------------------------------------------------------------------- |
| **Mã yêu cầu** | FR-37                                                                      |
| **Mô tả**      | Thống kê chi tiết từng khóa học: số ghi danh, rating, doanh thu, chứng chỉ |
| **Actor**      | Teacher                                                                    |
| **Endpoint**   | `GET /api/teacher/analytics/courses/`                                      |

#### FR-38: Dữ liệu chuỗi thời gian & Tương tác

| Mục            | Mô tả                                                                                                      |
| -------------- | ---------------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu** | FR-38                                                                                                      |
| **Mô tả**      | Xem biểu đồ ghi danh theo thời gian và các chỉ số tương tác (quiz, assignment, bài học đã hoàn thành)       |
| **Actor**      | Teacher                                                                                                    |
| **Endpoints**  | `GET /api/teacher/analytics/timeseries/`, `GET /api/teacher/analytics/engagement/`                         |
| **Query params** | `months` (mặc định 6)                                                                                   |

---

### Module 11: Trợ lý AI (RAG)

#### FR-39: Kiểm tra sức khỏe hệ thống RAG

| Mục                | Mô tả                                                    |
| ------------------ | -------------------------------------------------------- |
| **Mã yêu cầu**     | FR-39                                                    |
| **Mô tả**          | Kiểm tra kết nối Ollama và ChromaDB                      |
| **Actor**          | Student, Teacher                                         |
| **Endpoint**       | `GET /api/rag/health/`                                   |
| **Response**       | `{"status": "ok", "ollama": true, "chroma": true}`       |
| **HTTP Status**    | 200 nếu ok, 503 nếu degraded                             |

#### FR-40: Quản lý tài liệu RAG

| Mục                | Mô tả                                                                                                |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu**     | FR-40                                                                                                |
| **Mô tả**          | Upload, xem danh sách, xem chi tiết, xóa, re-index tài liệu cá nhân                                  |
| **Actor**          | Student, Teacher                                                                                     |
| **Endpoints**      | `GET/POST /api/rag/documents/`, `GET/DELETE /api/rag/documents/{id}/`, `POST /api/rag/documents/{id}/reindex/` |
| **Định dạng hỗ trợ** | PDF, TXT, DOCX, PPTX                                                                               |
| **Giới hạn**       | 30 MB/file                                                                                           |
| **Business rules** | Chỉ chủ sở hữu mới xem/xóa tài liệu. Tài liệu được index đồng bộ (parse → chunk → embedding → ChromaDB). |

**Luồng upload và index:**
1. Validate file (extension, size, empty)
2. Lưu file vào `media/rag/documents/{owner_id}/{uuid}.{ext}`
3. Tính SHA-256 checksum
4. Parse nội dung (pypdf/python-docx/python-pptx)
5. Chunk nội dung (size=1000, overlap=180)
6. Embedding theo batch (16 chunks/batch) qua Ollama bge-m3
7. Upsert vector vào ChromaDB
8. Lưu RagChunk records vào MySQL
9. Cập nhật status = "ready" (hoặc "failed" nếu lỗi)

#### FR-41: Quản lý hội thoại RAG

| Mục                | Mô tả                                                                         |
| ------------------ | ----------------------------------------------------------------------------- |
| **Mã yêu cầu**     | FR-41                                                                         |
| **Mô tả**          | Tạo, xem, cập nhật, xóa hội thoại AI (giống giao diện ChatGPT)               |
| **Actor**          | Student, Teacher                                                              |
| **Endpoints**      | `GET/POST /api/rag/conversations/`, `GET/PUT/PATCH/DELETE /api/rag/conversations/{id}/` |
| **Business rules** | Mỗi hội thoại gắn với một hoặc nhiều tài liệu. Chỉ chủ sở hữu mới truy cập.  |

#### FR-42: Hỏi đáp RAG

| Mục                | Mô tả                                                                                                                                                      |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Mã yêu cầu**     | FR-42                                                                                                                                                      |
| **Mô tả**          | Gửi câu hỏi đến AI, nhận câu trả lời dựa trên tài liệu đã chọn, kèm citation                                                                               |
| **Actor**          | Student, Teacher                                                                                                                                           |
| **Endpoint**       | `POST /api/rag/conversations/{id}/messages/`                                                                                                               |
| **Luồng chính**    | 1. Embedding câu hỏi (bge-m3) → 2. Query ChromaDB (top_k=6, max_distance=0.82) → 3. Lấy lịch sử 8 tin nhắn → 4. Build prompt → 5. Gọi LLM (qwen2.5:3b, temperature=0) → 6. Tạo citation → 7. Lưu user + assistant message |
| **Response**       | `{conversation_id, answer, citations: [{source_number, document_id, document_name, page_number, chunk_index, distance}], user_message, assistant_message}`  |

#### FR-43: Re-index tài liệu RAG

| Mục                | Mô tả                                                              |
| ------------------ | ------------------------------------------------------------------ |
| **Mã yêu cầu**     | FR-43                                                              |
| **Mô tả**          | Re-index một tài liệu (xóa vector cũ, tạo lại từ đầu)              |
| **Actor**          | Student, Teacher                                                   |
| **Endpoint**       | `POST /api/rag/documents/{id}/reindex/`                            |
| **Kết quả**        | 200 nếu thành công (status=ready), 422 nếu thất bại (status=failed) |

---

## Phần IV — Yêu cầu phi chức năng (Non-Functional Requirements)

### NFR-01: Hiệu năng (Performance)

| Yêu cầu | Mô tả |
| ------- | ----- |
| NFR-01.1 | Thời gian phản hồi API trung bình < 500ms (với 100 request đồng thời) |
| NFR-01.2 | Phân trang mặc định 10 bản ghi/trang |
| NFR-01.3 | Sử dụng `select_related`, `prefetch_related` để tối ưu truy vấn database |
| NFR-01.4 | Frontend SPA giảm tải server rendering |
| NFR-01.5 | Chat polling interval 5 giây (tối ưu cho scaling) |
| NFR-01.6 | RAG indexing đồng bộ (cần nâng cấp lên background task cho production) |

### NFR-02: Bảo mật (Security)

| Yêu cầu | Mô tả |
| ------- | ----- |
| NFR-02.1 | **Xác thực:** JWT (SimpleJWT) — access token 1 giờ, refresh token 7 ngày |
| NFR-02.2 | **Phân quyền:** Role-based (student/teacher/admin) qua custom permissions `IsTeacher`, `IsOwnerOrReadOnly` |
| NFR-02.3 | **Mật khẩu:** Hash bằng Django PBKDF2; validation (min length, không trùng với email) |
| NFR-02.4 | **CORS:** Cấu hình linh hoạt (AllowAll ở dev, whitelist ở production) |
| NFR-02.5 | **File upload:** Lưu trữ trên server, tên file unique (UUID) |
| NFR-02.6 | **RAG security:** Mọi queryset lọc theo `owner=request.user`. ChromaDB lọc theo `owner_id`. Chống IDOR. |
| NFR-02.7 | **Prompt injection:** System prompt yêu cầu coi nội dung tài liệu là dữ liệu, không phải chỉ dẫn hệ thống. |

### NFR-03: Khả năng mở rộng (Scalability)

| Yêu cầu | Mô tả |
| ------- | ----- |
| NFR-03.1 | Kiến trúc RESTful stateless — dễ dàng scale ngang backend |
| NFR-03.2 | Database indexing trên các field thường xuyên truy vấn (email, course_id, user_id, owner_id+status, conversation+created_at) |
| NFR-03.3 | Frontend SPA tĩnh có thể deploy qua CDN |
| NFR-03.4 | ChromaDB PersistentClient phù hợp single-process; production cần nâng cấp lên ChromaDB server |

### NFR-04: Độ tin cậy & Sẵn sàng (Reliability/Availability)

| Yêu cầu | Mô tả |
| ------- | ----- |
| NFR-04.1 | MySQL với SSL connection |
| NFR-04.2 | Logging cấu hình sẵn (console, level INFO) |
| NFR-04.3 | Xử lý lỗi đồng nhất: trả về JSON với success/error/details |
| NFR-04.4 | RAG health check endpoint kiểm tra Ollama + ChromaDB trước khi xử lý |

### NFR-05: Khả năng bảo trì (Maintainability)

| Yêu cầu | Mô tả |
| ------- | ----- |
| NFR-05.1 | Kiến trúc Django app (module hóa): users, courses, enrollments, assessments, reviews, analytics, chat, rag |
| NFR-05.2 | PEP 8 coding style (Python) |
| NFR-05.3 | DRF ViewSets cho CRUD chuẩn hóa |
| NFR-05.4 | Environment variables qua `.env.local` / `.env.prod` (python-dotenv) |
| NFR-05.5 | Tách biệt business logic vào services layer (analytics/services.py, rag/services/) |

### NFR-06: Khả năng tương thích (Compatibility)

| Yêu cầu | Mô tả |
| ------- | ----- |
| NFR-06.1 | Backend: Python 3.10+, Django 5.2+ |
| NFR-06.2 | Frontend: React 18+, Chrome/Firefox/Edge/Safari (2 phiên bản gần nhất) |
| NFR-06.3 | Database: MySQL 8.0+ |
| NFR-06.4 | API trả về JSON, RESTful |
| NFR-06.5 | RAG: Ollama server Windows/Linux, ChromaDB persistent |

### NFR-07: Usability/UX

| Yêu cầu | Mô tả |
| ------- | ----- |
| NFR-07.1 | Giao diện responsive (mobile/tablet/desktop) nhờ TailwindCSS |
| NFR-07.2 | Hỗ trợ dark mode (ThemeContext + Tailwind class strategy) |
| NFR-07.3 | Loading skeleton, error state, empty state cho mọi trang |
| NFR-07.4 | Phân trang, tìm kiếm, lọc dễ dàng |
| NFR-07.5 | Thông báo lỗi rõ ràng bằng tiếng Anh (API response) |
| NFR-07.6 | RAG giao diện tiếng Việt với 3-panel layout |
| NFR-07.7 | Quick actions cho RAG (tóm tắt, giải thích, tạo flashcard, tạo câu hỏi) |

### NFR-08: Tuân thủ pháp lý (Legal)

| Yêu cầu | Mô tả |
| ------- | ----- |
| NFR-08.1 | Mật khẩu được lưu trữ hash (PBKDF2), không plaintext |
| NFR-08.2 | API yêu cầu xác thực cho dữ liệu nhạy cảm |
| NFR-08.3 | RAG: tài liệu riêng tư theo user, không chia sẻ giữa các tài khoản |

---

## Phần V — Thiết kế hệ thống & Kiến trúc kỹ thuật

### 1. Kiến trúc tổng thể (Architecture Overview)

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              Client (Browser)                                        │
│  ┌──────────────────────────────────────────────────────────────────────────────┐   │
│  │                    React SPA (Vite + TailwindCSS)                             │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │   │
│  │  │ Auth     │ │ Courses  │ │ Quiz     │ │ Chat     │ │ AI Assistant     │   │   │
│  │  │ Pages    │ │ Pages    │ │ Pages    │ │ Pages    │ │ (RAG) Pages      │   │   │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────────┬─────────┘   │   │
│  │       └──────┬─────┴────────────┴────────────┴────────────────┘             │   │
│  │              │ Axios HTTP Client (JWT Interceptor, Auto Refresh)             │   │
│  └──────────────┼───────────────────────────────────────────────────────────────┘   │
└─────────────────┼───────────────────────────────────────────────────────────────────┘
                  │ HTTP/REST JSON
                  │ Authorization: Bearer <JWT>
┌─────────────────┼───────────────────────────────────────────────────────────────────┐
│  ┌──────────────┴────────────────────────────────────────────────────────────────┐  │
│  │                         Django REST Framework (port 8000)                      │  │
│  │  ┌──────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐ ┌──────────────┐   │  │
│  │  │ users/   │ │ courses/   │ │ assessments│ │ chat/    │ │ rag/         │   │  │
│  │  │ auth     │ │ sections   │ │ quizzes    │ │ convs    │ │ documents    │   │  │
│  │  │ profile  │ │ lessons    │ │ questions  │ │ msgs     │ │ conversations│   │  │
│  │  ├──────────┤ │            │ │ choices    │ │          │ │ messages     │   │  │
│  │  │ enroll-  │ │ reviews/   │ │ attempts   │ │          │ │ services/    │   │  │
│  │  │ ments/   │ │ course_rev │ │ submissions│ │          │ │  indexing    │   │  │
│  │  │ progress │ │            │ │            │ │          │ │  retrieval   │   │  │
│  │  │ cart     │ │ analytics/ │ │ common/    │ │          │ │  rag_service │   │  │
│  │  │ payments │ │ stats      │ │ permissions│ │          │ │              │   │  │
│  │  │ certs    │ │            │ │            │ │          │ │              │   │  │
│  │  └──────────┘ └────────────┘ └────────────┘ └──────────┘ └──────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────────────┘  │
│                           │                                                         │
│                    ┌──────┴──────────────────────────────────┐                      │
│                    │              MySQL Database              │                      │
│                    │  users, courses, sections, lessons,       │                      │
│                    │  enrollments, lesson_progresses,          │                      │
│                    │  certificates, cart_items, payments,      │                      │
│                    │  quizzes, questions, choices, attempts,   │                      │
│                    │  assignments, submissions, reviews,       │                      │
│                    │  conversations, messages,                 │                      │
│                    │  rag_documents, rag_chunks,               │                      │
│                    │  rag_conversations, rag_messages          │                      │
│                    └───────────────────────────────────────────┘                      │
│                                                                                       │
│                    ┌───────────────────────────────────────────┐                      │
│                    │         AI Layer (RAG)                     │                      │
│                    │  ┌────────────────┐ ┌──────────────────┐  │                      │
│                    │  │   ChromaDB     │ │     Ollama        │  │                      │
│                    │  │  Persistent    │ │  ┌─────────────┐ │  │                      │
│                    │  │  Client        │ │  │  bge-m3     │ │  │                      │
│                    │  │  (Vector DB)   │ │  │  (embedding) │ │  │                      │
│                    │  │                │ │  ├─────────────┤ │  │                      │
│                    │  │  collection:   │ │  │ qwen2.5:3b  │ │  │                      │
│                    │  │  lms_user_     │ │  │ (LLM)       │ │  │                      │
│                    │  │  documents     │ │  └─────────────┘ │  │                      │
│                    │  └────────────────┘ └──────────────────┘  │                      │
│                    └───────────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### 2. Lựa chọn công nghệ (Tech Stack)

| Layer                     | Công nghệ                    | Lý do chọn                                                                 |
| ------------------------- | ---------------------------- | -------------------------------------------------------------------------- |
| **Backend Framework**     | Django 5.2.7                 | ORM mạnh, bảo mật tích hợp, admin built-in, cộng đồng lớn                  |
| **REST API**              | DRF 3.16.1                   | Serializers, ViewSets, authentication classes, pagination, filtering       |
| **Authentication**        | SimpleJWT 5.5.1              | JWT tích hợp DRF, access/refresh token, dễ cấu hình                        |
| **Database**              | MySQL 8.0+                   | Ổn định, transaction, phổ biến, UTF8MB4 support                           |
| **Frontend**              | React 18.2                   | Component-based, ecosystem lớn, performance cao                            |
| **Routing**               | React Router DOM 6.20        | SPA routing, nested routes, guards (ProtectedRoute, TeacherRoute, StudentRoute) |
| **HTTP Client**           | Axios 1.6                    | Interceptors, token refresh tự động, FormData support                      |
| **CSS**                   | Tailwind CSS 3.4             | Utility-first, responsive, dark mode, custom design system                 |
| **Build**                 | Vite 5.0                     | Fast HMR, optimized build, zero-config                                     |
| **Charts**                | Recharts 3.5                 | React-native charting, dễ dùng, hỗ trợ area/line/bar charts               |
| **Vector Store**          | ChromaDB 0.5+                | Persistent local vector DB, cosine distance, metadata filtering           |
| **AI Embedding**          | Ollama (bge-m3)              | Local embedding, không cần API key, batch processing                       |
| **AI LLM**                | Ollama (qwen2.5:3b)          | Local LLM, 3B parameters, phù hợp hardware tầm trung                       |

### 3. Thiết kế cơ sở dữ liệu (Database Design)

#### 3.1. ER Diagram (Entity-Relationship)

```mermaid
erDiagram
    users ||--o{ courses : "teacher → course"
    users ||--o{ enrollments : "student → enrollment"
    users ||--o{ certificates : "user → certificate"
    users ||--o{ cart_items : "user → cart"
    users ||--o{ payments : "user → payment"
    users ||--o{ course_reviews : "user → review"
    users ||--o{ conversation_participants : "user → participant"
    users ||--o{ messages : "sender → message"
    users ||--o{ student_quiz_attempts : "student → attempt"
    users ||--o{ submissions : "student → submission"
    users ||--o{ rag_documents : "owner → document"
    users ||--o{ rag_conversations : "owner → conversation"

    courses ||--o{ sections : "course → section"
    courses ||--o{ enrollments : "course → enrollment"
    courses ||--o{ certificates : "course → certificate"
    courses ||--o{ quizzes : "course → quiz"
    courses ||--o{ assignments : "course → assignment"
    courses ||--o{ course_reviews : "course → review"
    courses ||--o{ cart_items : "course → cart_item"
    courses ||--o{ payments : "course → payment"

    sections ||--o{ lessons : "section → lesson"
    enrollments ||--o{ lesson_progresses : "enrollment → progress"

    quizzes ||--o{ questions : "quiz → question"
    questions ||--o{ choices : "question → choice"
    student_quiz_attempts ||--o{ student_answers : "attempt → answer"
    quizzes ||--o{ student_quiz_attempts : "quiz → attempt"

    assignments ||--o{ submissions : "assignment → submission"

    conversations ||--o{ conversation_participants : "conversation → participant"
    conversations ||--o{ messages : "conversation → message"

    rag_documents ||--o{ rag_chunks : "document → chunk"
    rag_conversations ||--o{ rag_messages : "conversation → message"
    rag_conversations }--o{ rag_documents : "M2M documents"
```

#### 3.2. Mô tả chi tiết các bảng

##### `users`

| Trường       | Kiểu         | Ràng buộc               | Mô tả                                   |
| ------------ | ------------ | ----------------------- | --------------------------------------- |
| id           | BigAuto      | PK                      |                                         |
| email        | EmailField   | Unique, Index, NOT NULL | Đăng nhập chính (USERNAME_FIELD)        |
| password     | VARCHAR(128) | NOT NULL                | Hashed password (PBKDF2)                |
| full_name    | VARCHAR(255) | Blank=True              | Họ tên đầy đủ                           |
| role         | VARCHAR(20)  | Default='student'       | student, teacher, admin                 |
| avatar_url   | URLField     | Nullable                | URL ảnh đại diện                        |
| bio          | Text         | Blank=True              | Tiểu sử                                 |
| headline     | VARCHAR(255) | Blank=True              | Chức danh (giảng viên)                  |
| country      | VARCHAR(100) | Blank=True              | Quốc gia                                |
| language     | VARCHAR(50)  | Default='en'            | Ngôn ngữ                                |
| social_links | JSON         | Default=dict            | Links: facebook, linkedin, github, website |
| is_staff     | Boolean      | Default=False           | Django admin access                     |
| is_superuser | Boolean      | Default=False           | Django superuser                        |
| date_joined  | DateTime     | Auto                    |                                         |

##### `courses`

| Trường        | Kiểu          | Ràng buộc               | Mô tả                            |
| ------------- | ------------- | ----------------------- | -------------------------------- |
| id            | BigAuto       | PK                      |                                  |
| teacher       | FK→users.id   | CASCADE                 | Giảng viên tạo khóa học          |
| title         | VARCHAR(255)  | NOT NULL                | Tiêu đề                          |
| subtitle      | VARCHAR(255)  | Blank=True              | Phụ đề                           |
| description   | Text          | NOT NULL                | Mô tả chi tiết                   |
| thumbnail_url | URLField      | Nullable                | Ảnh thumbnail                    |
| price         | Decimal(10,2) | Default=0.00            | Giá (0 = miễn phí)               |
| level         | VARCHAR(20)   | Default='beginner'      | beginner, intermediate, advanced |
| category      | VARCHAR(100)  | Blank=True              | Danh mục                         |
| is_published  | Boolean       | Default=False           | Đã xuất bản?                     |
| created_at    | DateTime      | Auto                    |                                  |
| updated_at    | DateTime      | Auto                    |                                  |

##### `sections`

| Trường     | Kiểu            | Ràng buộc                | Mô tả          |
| ---------- | --------------- | ------------------------ | -------------- |
| id         | BigAuto         | PK                       |                |
| course     | FK→courses.id   | CASCADE                  | Khóa học cha   |
| title      | VARCHAR(255)    | NOT NULL                 | Tên chương     |
| sort_order | PositiveInteger | Default=0, unique(course)| Thứ tự sắp xếp |

##### `lessons`

| Trường        | Kiểu            | Ràng buộc                  | Mô tả             |
| ------------- | --------------- | -------------------------- | ----------------- |
| id            | BigAuto         | PK                         |                   |
| section       | FK→sections.id  | CASCADE                    | Chương cha        |
| title         | VARCHAR(255)    | NOT NULL                   | Tiêu đề bài học   |
| video_url     | URLField        | Nullable                   | Link video (YouTube) |
| document_file | FileField       | Nullable                   | File tài liệu     |
| content       | Text            | Blank=True                 | Nội dung bài học  |
| duration      | PositiveInteger | Default=0                  | Thời lượng (giây) |
| sort_order    | PositiveInteger | Default=0, unique(section) | Thứ tự            |

##### `enrollments`

| Trường              | Kiểu            | Ràng buộc               | Mô tả                         |
| ------------------- | --------------- | ----------------------- | ----------------------------- |
| id                  | BigAuto         | PK                      |                               |
| student             | FK→users.id     | CASCADE                 | Học viên                      |
| course              | FK→courses.id   | CASCADE                 | Khóa học                      |
| progress_percent    | PositiveInteger | Default=0, 0-100        | % tiến độ                     |
| enrollment_type     | VARCHAR(10)     | Default='audit'         | audit, paid                   |
| price_paid          | Decimal(10,2)   | Default=0.00            | Số tiền đã trả                |
| granted_certificate | Boolean         | Default=False           | Đã cấp chứng chỉ?             |
| created_at          | DateTime        | Auto                    |                               |
| _Unique_            |                 | (student, course)       | Mỗi học viên một lần ghi danh |

##### `lesson_progresses`

| Trường        | Kiểu              | Ràng buộc                | Mô tả          |
| ------------- | ----------------- | ------------------------ | -------------- |
| id            | BigAuto           | PK                       |                |
| enrollment    | FK→enrollments.id | CASCADE                  |                |
| lesson        | FK→lessons.id     | CASCADE                  |                |
| is_completed  | Boolean           | Default=False            |                |
| completed_at  | DateTime          | Nullable                 |                |
| _Unique_      |                   | (enrollment, lesson)     |                |

##### `certificates`

| Trường           | Kiểu              | Ràng buộc            | Mô tả                     |
| ---------------- | ----------------- | -------------------- | ------------------------- |
| id               | BigAuto           | PK                   |                           |
| user             | FK→users.id       | CASCADE              |                           |
| course           | FK→courses.id     | CASCADE              |                           |
| enrollment       | FK→enrollments.id | CASCADE              |                           |
| issued_at        | DateTime          | Auto                 |                           |
| certificate_code | VARCHAR(32)       | Unique, NOT NULL     | UUID hex[:32]             |
| _Unique_         |                   | (user, course)       | Một chứng chỉ/user/course |

##### `cart_items`

| Trường       | Kiểu          | Ràng buộc      | Mô tả                  |
| ------------ | ------------- | -------------- | ---------------------- |
| id           | BigAuto       | PK             |                        |
| user         | FK→users.id   | CASCADE        |                        |
| course       | FK→courses.id | CASCADE        |                        |
| price_at_add | Decimal(10,2) | Default=0.00   | Giá tại thời điểm thêm |
| created_at   | DateTime      | Auto           |                        |
| _Unique_     |               | (user, course) |                        |

##### `payments`

| Trường         | Kiểu              | Ràng buộc           | Mô tả                       |
| -------------- | ----------------- | ------------------- | --------------------------- |
| id             | BigAuto           | PK                  |                             |
| user           | FK→users.id       | CASCADE             |                             |
| course         | FK→courses.id     | SET NULL            |                             |
| enrollment     | FK→enrollments.id | SET NULL            |                             |
| amount         | Decimal(10,2)     | NOT NULL            |                             |
| currency       | VARCHAR(10)       | Default='USD'       |                             |
| status         | VARCHAR(20)       | Default='succeeded' | succeeded, failed, refunded |
| source         | VARCHAR(20)       | Default='single'    | single, cart, upgrade       |
| reference_code | VARCHAR(64)       | Unique              | PAY-{UUID}                  |
| created_at     | DateTime          | Auto                |                             |

##### `quizzes`

| Trường       | Kiểu            | Ràng buộc     | Mô tả |
| ------------ | --------------- | ------------- | ----- |
| id           | BigAuto         | PK            |       |
| course       | FK→courses.id   | CASCADE       |       |
| title        | VARCHAR(255)    | NOT NULL      |       |
| description  | Text            | Blank=True    |       |
| is_published | Boolean         | Default=False |       |
| time_limit   | PositiveInteger | Nullable      | Phút  |
| created_at   | DateTime        | Auto          |       |
| updated_at   | DateTime        | Auto          |       |

##### `questions`

| Trường        | Kiểu            | Ràng buộc               | Mô tả                                |
| ------------- | --------------- | ----------------------- | ------------------------------------ |
| id            | BigAuto         | PK                      |                                      |
| quiz          | FK→quizzes.id   | CASCADE                 |                                      |
| text          | Text            | NOT NULL                | Nội dung câu hỏi                     |
| question_type | VARCHAR(32)     | Default='single_choice' | single_choice, multiple_choice, text |
| points        | PositiveInteger | Default=1, min=1        |                                      |
| order         | PositiveInteger | Default=0               |                                      |

##### `choices`

| Trường      | Kiểu            | Ràng buộc     | Mô tả             |
| ----------- | --------------- | ------------- | ----------------- |
| id          | BigAuto         | PK            |                   |
| question    | FK→questions.id | CASCADE       |                   |
| text        | VARCHAR(255)    | NOT NULL      | Nội dung lựa chọn |
| is_correct  | Boolean         | Default=False | Đáp án đúng?      |

##### `student_quiz_attempts`

| Trường       | Kiểu          | Ràng buộc             | Mô tả                  |
| ------------ | ------------- | --------------------- | ---------------------- |
| id           | BigAuto       | PK                    |                        |
| student      | FK→users.id   | CASCADE               |                        |
| quiz         | FK→quizzes.id | CASCADE               |                        |
| started_at   | DateTime      | Auto                  |                        |
| completed_at | DateTime      | Nullable              |                        |
| score        | Float         | Default=0.0           |                        |
| status       | VARCHAR(20)   | Default='in_progress' | in_progress, completed |

##### `assignments`

| Trường         | Kiểu            | Ràng buộc     | Mô tả |
| -------------- | --------------- | ------------- | ----- |
| id             | BigAuto         | PK            |       |
| course         | FK→courses.id   | CASCADE       |       |
| title          | VARCHAR(255)    | NOT NULL      |       |
| description    | Text            | Blank=True    |       |
| due_date       | DateTime        | Nullable      |       |
| max_points     | PositiveInteger | Default=10    |       |
| attachment_url | VARCHAR(500)    | Blank=True    |       |
| is_published   | Boolean         | Default=False |       |
| created_at     | DateTime        | Auto          |       |

##### `submissions`

| Trường        | Kiểu              | Ràng buộc             | Mô tả             |
| ------------- | ----------------- | --------------------- | ----------------- |
| id            | BigAuto           | PK                    |                   |
| assignment    | FK→assignments.id | CASCADE               |                   |
| student       | FK→users.id       | CASCADE               |                   |
| content       | Text              | Blank=True            | Nội dung/file URL |
| submitted_at  | DateTime          | Auto                  |                   |
| graded_at     | DateTime          | Nullable              |                   |
| grade         | Float             | Nullable              |                   |
| feedback      | Text              | Blank=True            |                   |
| status        | VARCHAR(20)       | Default='submitted'   | submitted, graded |
| _Unique_      |                   | (assignment, student) |                   |

##### `course_reviews`

| Trường     | Kiểu                 | Ràng buộc      | Mô tả |
| ---------- | -------------------- | -------------- | ----- |
| id         | BigAuto              | PK             |       |
| course     | FK→courses.id        | CASCADE        |       |
| user       | FK→users.id          | CASCADE        |       |
| rating     | PositiveSmallInteger | Validated 1-5 |       |
| comment    | Text                 | Blank=True     |       |
| created_at | DateTime             | Auto           |       |
| updated_at | DateTime             | Auto           |       |
| _Unique_   |                      | (course, user) |       |

##### `conversations`

| Trường     | Kiểu             | Ràng buộc     | Mô tả |
| ---------- | ---------------- | ------------- | ----- |
| id         | BigAuto          | PK            |       |
| is_group   | Boolean          | Default=False |       |
| name       | VARCHAR(255)     | Nullable      |       |
| created_at | DateTime         | Auto          |       |
| updated_at | DateTime         | Auto          |       |

##### `messages`

| Trường          | Kiểu                | Ràng buộc | Mô tả |
| --------------- | ------------------- | --------- | ----- |
| id              | BigAuto             | PK        |       |
| conversation    | FK→conversations.id | CASCADE   |       |
| sender          | FK→users.id         | CASCADE   |       |
| content         | Text                | NOT NULL  |       |
| created_at      | DateTime            | Auto      |       |

##### `rag_documents`

| Trường        | Kiểu                | Ràng buộc               | Mô tả                      |
| ------------- | ------------------- | ----------------------- | -------------------------- |
| id            | BigAuto             | PK                      |                            |
| owner         | FK→users.id         | CASCADE                 | Chủ sở hữu                 |
| name          | VARCHAR(255)        | NOT NULL                | Tên hiển thị               |
| original_name | VARCHAR(255)        | NOT NULL                | Tên file gốc               |
| file          | FileField           | NOT NULL                | File path                  |
| file_type     | VARCHAR(20)         | NOT NULL                | pdf, txt, docx, pptx       |
| mime_type     | VARCHAR(120)        | Blank=True              | MIME type                  |
| size_bytes    | PositiveBigInteger  | Default=0               | Kích thước file            |
| checksum      | VARCHAR(64)         | Blank=True, db_index    | SHA-256                    |
| status        | VARCHAR(20)         | Default='pending'       | pending, processing, ready, failed |
| chunk_count   | PositiveInteger     | Default=0               | Số chunk                   |
| error_message | Text                | Blank=True              | Lỗi khi index              |
| processed_at  | DateTime            | Nullable                | Thời điểm xử lý xong       |
| created_at    | DateTime            | Auto                    |                            |
| updated_at    | DateTime            | Auto                    |                            |

##### `rag_chunks`

| Trường       | Kiểu                | Ràng buộc                | Mô tả                      |
| ------------ | ------------------- | ------------------------ | -------------------------- |
| id           | BigAuto             | PK                       |                            |
| document     | FK→rag_documents.id | CASCADE                  | Tài liệu cha               |
| vector_id    | VARCHAR(100)        | Unique                   | `doc-{id}-chunk-{index}`   |
| chunk_index  | PositiveInteger     | unique(document, index)  | Thứ tự chunk               |
| content      | Text                | NOT NULL                 | Nội dung chunk             |
| page_number  | PositiveInteger     | Nullable                 | Trang/slide                |
| section_title| VARCHAR(255)        | Blank=True               | Tiêu đề phần               |
| metadata     | JSON                | Default=dict             | Owner_id, document_name... |
| created_at   | DateTime            | Auto                     |                            |

##### `rag_conversations`

| Trường     | Kiểu                | Ràng buộc               | Mô tả                  |
| ---------- | ------------------- | ----------------------- | ---------------------- |
| id         | BigAuto             | PK                      |                        |
| owner      | FK→users.id         | CASCADE                 | Chủ hội thoại          |
| title      | VARCHAR(255)        | Default='New chat'      | Tiêu đề                |
| documents  | M2M→rag_documents   |                         | Tài liệu được chọn     |
| created_at | DateTime            | Auto                    |                        |
| updated_at | DateTime            | Auto                    |                        |

##### `rag_messages`

| Trường           | Kiểu                  | Ràng buộc                | Mô tả                  |
| ---------------- | --------------------- | ------------------------ | ---------------------- |
| id               | BigAuto               | PK                       |                        |
| conversation     | FK→rag_conversations  | CASCADE                  |                        |
| role             | VARCHAR(20)           | NOT NULL                 | user, assistant        |
| content          | Text                  | NOT NULL                 | Nội dung               |
| citations        | JSON                  | Default=list             | Danh sách nguồn        |
| model_name       | VARCHAR(100)          | Blank=True               | qwen2.5:3b             |
| response_time_ms | PositiveInteger       | Default=0                | Thời gian phản hồi     |
| created_at       | DateTime              | Auto                     |                        |

### 4. Thiết kế API

#### 4.1. Định dạng request/response

**Success Response:**
```json
{
  "success": true,
  "data": { ... }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message",
  "details": { ... }
}
```

**Paginated Response:**
```json
{
  "count": 100,
  "next": "http://api.example.com/courses/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

#### 4.2. Danh sách API Endpoint đầy đủ

##### Authentication (`/api/auth/`)

| Method | Endpoint              | Mô tả            | Permission  |
| ------ | --------------------- | ---------------- | ----------- |
| POST   | `/api/auth/register/` | Đăng ký          | AllowAny    |
| POST   | `/api/auth/login/`    | Đăng nhập        | AllowAny    |
| POST   | `/api/auth/refresh/`  | Refresh token    | AllowAny    |
| GET    | `/api/auth/me/`       | Thông tin user   | IsAuthenticated |
| POST   | `/api/auth/change-password/` | Đổi mật khẩu | IsAuthenticated |

##### Users (`/api/users/`)

| Method | Endpoint                              | Mô tả                | Permission      |
| ------ | ------------------------------------- | -------------------- | --------------- |
| GET/POST | `/api/users/`                       | Danh sách/Tạo user  | Varies          |
| GET/PUT/PATCH/DELETE | `/api/users/{id}/`          | Chi tiết user       | Varies          |
| GET    | `/api/users/me/profile/`              | Hồ sơ của tôi       | IsAuthenticated |
| PUT/PATCH | `/api/users/me/profile/`          | Cập nhật hồ sơ      | IsOwner         |
| GET    | `/api/users/{id}/profile/`             | Hồ sơ công khai     | AllowAny        |
| GET    | `/api/instructors/top/`               | Top giảng viên      | AllowAny        |
| GET    | `/api/instructors/{id}/profile/`       | Hồ sơ giảng viên   | AllowAny        |

##### Courses (`/api/courses/`, `/api/teacher/courses/`)

| Method | Endpoint                              | Mô tả                     | Permission      |
| ------ | ------------------------------------- | ------------------------- | --------------- |
| GET    | `/api/courses/`                       | Danh sách khóa học        | AllowAny        |
| GET    | `/api/courses/{id}/`                  | Chi tiết khóa học         | AllowAny        |
| GET    | `/api/courses/categories/`            | Danh mục khóa học         | AllowAny        |
| GET    | `/api/courses/{id}/curriculum/`       | Chương trình học          | AllowAny        |
| GET/POST | `/api/teacher/courses/`            | CRUD khóa học (GV)        | IsTeacher       |
| GET/PUT/PATCH/DELETE | `/api/teacher/courses/{id}/` | CRUD khóa học (GV)       | IsTeacher+Owner |
| GET/POST | `/api/teacher/sections/`           | CRUD section              | IsTeacher       |
| GET/PUT/PATCH/DELETE | `/api/teacher/sections/{id}/` | CRUD section              | IsTeacher+Owner |
| GET/POST | `/api/teacher/lessons/`           | CRUD lesson               | IsTeacher       |
| GET/PUT/PATCH/DELETE | `/api/teacher/lessons/{id}/` | CRUD lesson               | IsTeacher+Owner |

##### Enrollments (`/api/enrollments/`, `/api/courses/`)

| Method | Endpoint                              | Mô tả                     | Permission      |
| ------ | ------------------------------------- | ------------------------- | --------------- |
| POST   | `/api/courses/{id}/enroll/`           | Ghi danh miễn phí         | IsAuthenticated |
| POST   | `/api/courses/{id}/purchase/`         | Mua/audit khóa học        | IsAuthenticated |
| POST   | `/api/lessons/{id}/complete/`         | Hoàn thành bài học        | IsAuthenticated |
| GET    | `/api/student/my-courses/`            | Khóa học của tôi          | IsAuthenticated |
| GET    | `/api/enrollments/me/`                | Ghi danh của tôi          | IsAuthenticated |
| GET    | `/api/enrollments/me/certificates/`   | Chứng chỉ của tôi         | IsAuthenticated |
| GET    | `/api/enrollments/me/payments/`       | Lịch sử thanh toán        | IsAuthenticated |
| GET/POST | `/api/enrollments/cart/`           | Giỏ hàng                  | IsAuthenticated |
| POST   | `/api/enrollments/cart/add/`          | Thêm vào giỏ              | IsAuthenticated |
| DELETE | `/api/enrollments/cart/items/{id}/`   | Xóa khỏi giỏ              | IsAuthenticated |
| POST   | `/api/enrollments/cart/checkout/`     | Thanh toán                | IsAuthenticated |
| POST   | `/api/courses/{id}/certificate/issue/` | Cấp chứng chỉ           | IsAuthenticated |
| GET    | `/api/courses/{id}/certificate/me/`   | Xem chứng chỉ khóa học    | IsAuthenticated |
| GET    | `/api/teacher/courses/{id}/students/` | DS học viên (GV)          | IsTeacher       |
| DELETE | `/api/teacher/courses/{id}/students/{sid}/` | Xóa học viên       | IsTeacher       |

##### Assessments (`/api/teacher/quizzes/`, `/api/teacher/assignments/`)

| Method | Endpoint                              | Mô tả                     | Permission      |
| ------ | ------------------------------------- | ------------------------- | --------------- |
| GET/POST | `/api/teacher/quizzes/`            | CRUD quiz (GV)            | IsTeacher       |
| GET/PUT/PATCH/DELETE | `/api/teacher/quizzes/{id}/` | CRUD quiz (GV)            | IsTeacher+Owner |
| POST   | `/api/teacher/quizzes/{id}/questions/` | Thêm câu hỏi          | IsTeacher       |
| GET/PUT/PATCH/DELETE | `/api/teacher/questions/{id}/` | CRUD câu hỏi        | IsTeacher       |
| POST   | `/api/teacher/questions/{id}/choices/` | Thêm lựa chọn          | IsTeacher       |
| GET/PUT/PATCH/DELETE | `/api/teacher/choices/{id}/` | CRUD lựa chọn          | IsTeacher       |
| GET/POST | `/api/teacher/assignments/`      | CRUD assignment (GV)      | IsTeacher       |
| GET/PUT/PATCH/DELETE | `/api/teacher/assignments/{id}/` | CRUD assignment     | IsTeacher+Owner |
| GET    | `/api/teacher/assignments/{id}/submissions/` | DS bài nộp     | IsTeacher       |
| PATCH  | `/api/teacher/submissions/{id}/grade/` | Chấm điểm            | IsTeacher       |

##### Assessments (Student)

| Method | Endpoint                              | Mô tả                     | Permission      |
| ------ | ------------------------------------- | ------------------------- | --------------- |
| GET    | `/api/courses/{id}/quizzes/`          | DS quiz khóa học          | IsAuthenticated |
| GET    | `/api/quizzes/{id}/`                  | Chi tiết quiz             | IsAuthenticated |
| POST   | `/api/quizzes/{id}/start/`            | Bắt đầu làm quiz          | IsAuthenticated |
| POST   | `/api/quizzes/{id}/submit/`           | Nộp bài                   | IsAuthenticated |
| GET    | `/api/quizzes/{id}/attempts/me/`      | Lịch sử làm quiz          | IsAuthenticated |
| GET    | `/api/courses/{id}/assignments/`      | DS assignment khóa học    | IsAuthenticated |
| GET    | `/api/assignments/{id}/`              | Chi tiết assignment       | IsAuthenticated |
| POST   | `/api/assignments/{id}/submit/`       | Nộp bài tập               | IsAuthenticated |
| GET    | `/api/assignments/{id}/my-submission/`| Bài nộp của tôi           | IsAuthenticated |
| POST   | `/api/upload/`                        | Upload file               | IsAuthenticated |

##### Reviews (`/api/courses/{id}/reviews/`)

| Method | Endpoint                              | Mô tả                     | Permission      |
| ------ | ------------------------------------- | ------------------------- | --------------- |
| GET/POST | `/api/courses/{id}/reviews/`      | DS/Tạo review             | GET: AllowAny, POST: IsAuthenticated |
| GET    | `/api/courses/{id}/rating-summary/`   | Rating tổng quan          | AllowAny        |
| GET    | `/api/courses/{id}/my-review/`        | Review của tôi            | IsAuthenticated |
| GET/PUT/PATCH/DELETE | `/api/reviews/{id}/`    | Chi tiết review           | IsAuthenticated+Owner |

##### Analytics (`/api/teacher/analytics/`)

| Method | Endpoint                              | Mô tả                     | Permission      |
| ------ | ------------------------------------- | ------------------------- | --------------- |
| GET    | `/api/teacher/analytics/summary/`     | Thống kê tổng quan        | IsTeacher       |
| GET    | `/api/teacher/analytics/courses/`     | Thống kê theo khóa học    | IsTeacher       |
| GET    | `/api/teacher/analytics/timeseries/`  | Dữ liệu chuỗi thời gian   | IsTeacher       |
| GET    | `/api/teacher/analytics/engagement/`  | Mức độ tương tác          | IsTeacher       |

##### Chat (`/api/chat/`)

| Method | Endpoint                              | Mô tả                     | Permission      |
| ------ | ------------------------------------- | ------------------------- | --------------- |
| GET/POST | `/api/chat/conversations/`        | DS/Tạo hội thoại          | IsAuthenticated |
| GET    | `/api/chat/conversations/{id}/`       | Chi tiết hội thoại        | IsAuthenticated |
| GET/POST | `/api/chat/conversations/{id}/messages/` | DS/Gửi tin nhắn      | IsAuthenticated |
| GET    | `/api/chat/unread-count/`             | Đếm chưa đọc              | IsAuthenticated |

##### RAG `/api/rag/`)

| Method | Endpoint                              | Mô tả                     | Permission      |
| ------ | ------------------------------------- | ------------------------- | --------------- |
| GET    | `/api/rag/health/`                    | Kiểm tra sức khỏe         | IsAuthenticated |
| GET/POST | `/api/rag/documents/`              | DS/Upload tài liệu        | IsAuthenticated |
| GET/DELETE | `/api/rag/documents/{id}/`       | Chi tiết/Xóa tài liệu    | IsAuthenticated+Owner |
| POST   | `/api/rag/documents/{id}/reindex/`    | Re-index tài liệu         | IsAuthenticated+Owner |
| GET/POST | `/api/rag/conversations/`         | DS/Tạo hội thoại          | IsAuthenticated |
| GET/PUT/PATCH/DELETE | `/api/rag/conversations/{id}/` | CRUD hội thoại           | IsAuthenticated+Owner |
| POST   | `/api/rag/conversations/{id}/messages/` | Gửi câu hỏi            | IsAuthenticated+Owner |

#### 4.3. Mã lỗi HTTP

| Mã  | Ý nghĩa               | Ngữ cảnh                          |
| --- | --------------------- | --------------------------------- |
| 200 | OK                    | Thành công                        |
| 201 | Created               | Tạo mới thành công                |
| 204 | No Content            | Xóa thành công                    |
| 400 | Bad Request           | Dữ liệu đầu vào không hợp lệ      |
| 401 | Unauthorized          | Token không hợp lệ/hết hạn        |
| 403 | Forbidden             | Không có quyền truy cập           |
| 404 | Not Found             | Resource không tồn tại            |
| 422 | Unprocessable Entity  | Dữ liệu không thể xử lý (RAG reindex failed) |
| 500 | Internal Server Error | Lỗi server                        |
| 503 | Service Unavailable   | RAG degraded (Ollama/ChromaDB down) |

---

## Phần VI — Sơ đồ UML

### 1. Use Case Diagram

```mermaid
graph TD
    subgraph "Hệ thống LMS_DJANGO"
        UC1(Đăng ký/Đăng nhập)
        UC2(Xem danh sách khóa học)
        UC3(Xem chi tiết khóa học)
        UC4(Ghi danh khóa học)
        UC5(Mua khóa học)
        UC6(Quản lý giỏ hàng)
        UC7(Đánh dấu bài học hoàn thành)
        UC8(Làm bài kiểm tra)
        UC9(Nộp bài tập)
        UC10(Xem chứng chỉ)
        UC11(Đánh giá khóa học)
        UC12(Nhắn tin)
        UC13(Tạo/Quản lý khóa học)
        UC14(Tạo Quiz & Assignment)
        UC15(Chấm điểm bài tập)
        UC16(Xem thống kê)
        UC17(Quản lý học viên)
        UC18(Cấp chứng chỉ)
        UC19(Xem hồ sơ công khai)
        UC20(Upload tài liệu AI)
        UC21(Hỏi đáp với AI Assistant)

        Actor_Student --- UC1 & UC2 & UC3 & UC4 & UC5 & UC6 & UC7 & UC8 & UC9 & UC10 & UC11 & UC12 & UC19 & UC20 & UC21
        Actor_Teacher --- UC1 & UC2 & UC3 & UC12 & UC13 & UC14 & UC15 & UC16 & UC17 & UC18 & UC19 & UC20 & UC21
        Actor_Guest --- UC2 & UC3 & UC19
    end
```

### 2. Class Diagram

```mermaid
classDiagram
    class User {
        +int id
        +string email
        +string password
        +string full_name
        +string role
        +string avatar_url
        +string bio
        +string headline
        +string country
        +string language
        +dict social_links
    }

    class Course {
        +int id
        +string title
        +string subtitle
        +text description
        +string thumbnail_url
        +decimal price
        +string level
        +string category
        +bool is_published
        +datetime created_at
        +datetime updated_at
    }

    class Section {
        +int id
        +string title
        +int sort_order
    }

    class Lesson {
        +int id
        +string title
        +string video_url
        +string document_file
        +text content
        +int duration
        +int sort_order
    }

    class Enrollment {
        +int id
        +string enrollment_type
        +int progress_percent
        +decimal price_paid
        +bool granted_certificate
    }

    class LessonProgress {
        +bool is_completed
        +datetime completed_at
    }

    class Certificate {
        +int id
        +string certificate_code
        +datetime issued_at
    }

    class CartItem {
        +int id
        +decimal price_at_add
    }

    class Payment {
        +int id
        +decimal amount
        +string currency
        +string status
        +string source
        +string reference_code
    }

    class Quiz {
        +int id
        +string title
        +text description
        +bool is_published
        +int time_limit
    }

    class Question {
        +int id
        +text text
        +string question_type
        +int points
        +int order
    }

    class Choice {
        +int id
        +string text
        +bool is_correct
    }

    class StudentQuizAttempt {
        +int id
        +float score
        +string status
    }

    class StudentAnswer {
        +int id
    }

    class Assignment {
        +int id
        +string title
        +text description
        +datetime due_date
        +int max_points
        +bool is_published
    }

    class Submission {
        +int id
        +text content
        +float grade
        +text feedback
        +string status
    }

    class CourseReview {
        +int id
        +int rating
        +text comment
    }

    class Conversation {
        +int id
        +bool is_group
        +string name
    }

    class Message {
        +int id
        +text content
    }

    class RagDocument {
        +int id
        +string name
        +string original_name
        +string file_type
        +int size_bytes
        +string checksum
        +string status
        +int chunk_count
    }

    class RagChunk {
        +int id
        +string vector_id
        +int chunk_index
        +text content
        +int page_number
    }

    class RagConversation {
        +int id
        +string title
    }

    class RagMessage {
        +int id
        +string role
        +text content
        +list citations
        +int response_time_ms
    }

    User "1" --> "*" Course : teaches
    User "1" --> "*" Enrollment : enrolls
    User "1" --> "*" Certificate : owns
    User "1" --> "*" CartItem : has
    User "1" --> "*" Payment : makes
    User "1" --> "*" CourseReview : writes
    User "1" --> "*" StudentQuizAttempt : takes
    User "1" --> "*" Submission : submits
    User "1" --> "*" Message : sends
    User "1" --> "*" RagDocument : owns
    User "1" --> "*" RagConversation : owns

    Course "1" --> "*" Section : contains
    Section "1" --> "*" Lesson : contains
    Course "1" --> "*" Enrollment : has
    Course "1" --> "*" Certificate : issues
    Course "1" --> "*" Quiz : assesses
    Course "1" --> "*" Assignment : assigns
    Course "1" --> "*" CourseReview : reviewed_by
    Course "1" --> "*" CartItem : added_to_cart
    Course "1" --> "*" Payment : paid_for

    Enrollment "1" --> "*" LessonProgress : tracks
    Quiz "1" --> "*" Question : contains
    Question "1" --> "*" Choice : has
    StudentQuizAttempt "1" --> "*" StudentAnswer : contains
    Quiz "1" --> "*" StudentQuizAttempt : attempted_by

    Assignment "1" --> "*" Submission : receives

    Conversation "1" --> "*" Message : contains

    RagDocument "1" --> "*" RagChunk : chunks
    RagConversation "1" --> "*" RagMessage : messages
    RagConversation "*" --> "*" RagDocument : references
```

### 3. Sequence Diagram — Luồng RAG (AI Assistant)

```mermaid
sequenceDiagram
    participant User as Người dùng
    participant Frontend as React SPA
    participant API as Django REST API
    participant MySQL
    participant ChromaDB as ChromaDB Vector Store
    participant Ollama

    Note over User,Ollama: Upload & Index tài liệu
    User->>Frontend: Upload file PDF
    Frontend->>API: POST /api/rag/documents/ (FormData)
    API->>MySQL: INSERT RagDocument (status=pending)
    API->>API: Parse file (pypdf/python-docx/python-pptx)
    API->>API: Chunk nội dung (size=1000, overlap=180)
    API->>Ollama: Embedding batch (bge-m3)
    Ollama-->>API: Vector embeddings
    API->>ChromaDB: Upsert vectors + metadata
    API->>MySQL: INSERT RagChunks, UPDATE status=ready
    API-->>Frontend: 201 Created, {status: "ready"}
    Frontend-->>User: Tài liệu sẵn sàng

    Note over User,Ollama: Hỏi đáp
    User->>Frontend: Chọn tài liệu + gửi câu hỏi
    Frontend->>API: POST /api/rag/conversations/{id}/messages/
    API->>MySQL: Lưu user message
    API->>Ollama: Embedding câu hỏi (bge-m3)
    Ollama-->>API: Query embedding
    API->>ChromaDB: Query top_k=6, max_distance=0.82
    ChromaDB-->>API: Retreived chunks + scores
    API->>API: Build prompt (system + history + context)
    API->>Ollama: Chat completion (qwen2.5:3b, temp=0)
    Ollama-->>API: Câu trả lời
    API->>MySQL: Lưu assistant message + citations
    API-->>Frontend: {answer, citations, user_message, assistant_message}
    Frontend-->>User: Hiển thị câu trả lời + citation cards
```

### 4. Activity Diagram — Quy trình học viên hoàn thành khóa học

```mermaid
flowchart TD
    A([Bắt đầu]) --> B{Tìm khóa học?}
    B -->|Tìm kiếm| C[Xem danh sách khóa học]
    B -->|Duyệt| D[Xem danh mục]
    C --> E[Chọn khóa học]
    D --> E
    E --> F[Xem chi tiết khóa học]
    F --> G{Khóa học miễn phí?}
    G -->|Có| H[Ghi danh miễn phí]
    G -->|Không| I{Đã có trong giỏ?}
    I -->|Chưa| J[Thêm vào giỏ hàng]
    J --> K[Thanh toán]
    K --> L[Ghi danh trả phí]
    I -->|Rồi| K
    H --> M[Vào học]
    L --> M
    M --> N[Học bài học]
    N --> O[Đánh dấu hoàn thành]
    O --> P{Còn bài học?}
    P -->|Có| N
    P -->|Không| Q{Từng trả phí?}
    Q -->|Có| R[Yêu cầu chứng chỉ]
    R --> S[Nhận chứng chỉ]
    Q -->|Không| T([Kết thúc])
    S --> T
```

### 5. State Diagrams

#### 5.1. Enrollment State

```mermaid
stateDiagram-v2
    [*] --> Enrolled : Ghi danh
    Enrolled --> InProgress : Học bài 1
    InProgress --> Completed : Hoàn thành 100%
    Completed --> Certified : Cấp chứng chỉ
    Certified --> [*]

    state InProgress {
        [*] --> Watching : Xem bài học
        Watching --> Done : Đánh dấu hoàn thành
        Done --> Watching : Bài học tiếp theo
    }
```

#### 5.2. Submission State

```mermaid
stateDiagram-v2
    [*] --> Draft : Assignment chưa publish
    Draft --> Published : Giảng viên publish
    Published --> Submitted : Học viên nộp bài
    Submitted --> Graded : Giảng viên chấm điểm
    Graded --> [*]
```

#### 5.3. RAG Document State

```mermaid
stateDiagram-v2
    [*] --> Pending : Upload thành công
    Pending --> Processing : Bắt đầu index
    Processing --> Ready : Index thành công
    Processing --> Failed : Lỗi (Ollama/parse)
    Ready --> Processing : Re-index
    Failed --> Processing : Re-index
    Ready --> [*] : Xóa tài liệu
```

---

## Phần VII — Ma trận truy vết yêu cầu (Requirements Traceability Matrix)

| Mã yêu cầu | Tên chức năng                      | Module        | Use Case | Backend View                            | Frontend Component         | Ưu tiên |
| ---------- | ---------------------------------- | ------------- | -------- | --------------------------------------- | -------------------------- | ------- |
| FR-01      | Đăng ký                            | Auth          | UC1      | auth_views.py:RegisterView              | Register.jsx               | High    |
| FR-02      | Đăng nhập                          | Auth          | UC1      | auth_views.py:CustomTokenObtainPairView | Login.jsx                  | High    |
| FR-03      | Thông tin user hiện tại            | Auth          | UC1      | auth_views.py:MeAPIView                 | Navbar.jsx                 | High    |
| FR-04      | Hồ sơ cá nhân                      | Users         | UC1      | viewsets.py:UserViewSet                 | EditProfile.jsx            | Medium  |
| FR-05      | Hồ sơ công khai                    | Users         | UC19     | auth_views.py:PublicProfileAPIView      | PublicProfile.jsx          | Low     |
| FR-06      | Đổi mật khẩu                       | Auth          | UC1      | auth_views.py:ChangePasswordAPIView     | ChangePassword.jsx         | Medium  |
| FR-07      | Top giảng viên                     | Users         | UC19     | auth_views.py:TopInstructorsAPIView     | Home.jsx, InstructorCard.jsx | Low   |
| FR-08      | Danh sách khóa học                 | Courses       | UC2      | courses/views.py:CourseViewSet          | BrowseCourses.jsx          | High    |
| FR-09      | Chi tiết khóa học                  | Courses       | UC3      | courses/views.py:CourseViewSet.retrieve | CourseLandingPage.jsx      | High    |
| FR-10      | Chương trình học                   | Courses       | UC3      | courses/views.py:CourseCurriculumAPIView| CourseLandingPage.jsx      | High    |
| FR-11      | Danh mục khóa học                  | Courses       | UC2      | courses/views.py:CourseCategoriesListAPIView | BrowseCourses.jsx     | Low     |
| FR-12      | Xem bài học                        | Courses       | UC3      | courses/views.py:LessonDetailAPIView    | CourseLearning.jsx         | High    |
| FR-13      | Quản lý khóa học (GV)              | Courses       | UC13     | courses/teacher_views.py               | CourseEditor.jsx           | High    |
| FR-14      | Ghi danh miễn phí                  | Enrollments   | UC4      | enrollments/views.py:EnrollCourseAPIView| CourseLandingPage.jsx      | High    |
| FR-15      | Ghi danh trả phí/audit             | Enrollments   | UC5      | enrollments/views.py:PurchaseCourseAPIView | CourseLandingPage.jsx  | High    |
| FR-16      | Hoàn thành bài học                 | Enrollments   | UC7      | enrollments/views.py:CompleteLessonAPIView | CourseLearning.jsx     | High    |
| FR-17      | Khóa học của tôi                   | Enrollments   | UC4      | enrollments/views.py:StudentMyCoursesAPIView | MyLearning.jsx       | High    |
| FR-18      | DS học viên (GV)                   | Enrollments   | UC17     | enrollments/views.py:TeacherCourseStudentsView | TeacherStudents.jsx | Medium  |
| FR-19      | Xóa học viên (GV)                  | Enrollments   | UC17     | enrollments/views.py:RemoveStudentFromCourseView | TeacherStudents.jsx | Low     |
| FR-20      | Quản lý giỏ hàng                   | Enrollments   | UC6      | enrollments/cart_views.py              | CartPage.jsx               | Medium  |
| FR-21      | Thanh toán giỏ hàng                | Enrollments   | UC5      | enrollments/cart_views.py:CartCheckoutAPIView | CartCheckoutPage.jsx  | Medium  |
| FR-22      | Lịch sử thanh toán                 | Enrollments   | UC5      | enrollments/views.py:PaymentHistoryListAPIView | StudentPaymentHistory.jsx | Low |
| FR-23      | Quản lý quiz (GV)                  | Assessments   | UC14     | assessments/views.py:TeacherQuizViewSet | QuizEditor.jsx, TeacherCourseQuizzes.jsx | High |
| FR-24      | Làm quiz (HV)                      | Assessments   | UC8      | assessments/views.py:QuizStartAPIView, QuizSubmitAPIView | StudentQuizPlayer.jsx | High |
| FR-25      | Lịch sử làm quiz                   | Assessments   | UC8      | assessments/views.py:QuizAttemptsMeAPIView | QuizHistory.jsx        | Low     |
| FR-26      | Quản lý assignment (GV)            | Assessments   | UC14     | assessments/views.py:TeacherAssignmentViewSet | TeacherAssignmentEditor.jsx | High |
| FR-27      | Nộp bài tập (HV)                   | Assessments   | UC9      | assessments/views.py:AssignmentSubmitAPIView | StudentAssignmentDetail.jsx | Medium |
| FR-28      | Upload file                        | Assessments   | UC9      | assessments/views.py:upload_file_view  | (Axios upload)             | Medium  |
| FR-29      | Cấp chứng chỉ                      | Enrollments   | UC18     | enrollments/views.py:IssueCertificateAPIView | CertificateView.jsx    | Medium  |
| FR-30      | Xem chứng chỉ                      | Enrollments   | UC10     | enrollments/views.py:MyCertificateAPIView | CertificateView.jsx    | Medium  |
| FR-31      | Đánh giá khóa học                  | Reviews       | UC11     | reviews/views.py:CourseReviewListCreateAPIView | CourseReviewForm.jsx  | Medium  |
| FR-32      | Rating tổng quan                   | Reviews       | UC11     | reviews/views.py:CourseRatingSummaryAPIView | CourseLandingPage.jsx  | Low     |
| FR-33      | Quản lý hội thoại                  | Chat          | UC12     | chat/views.py:ConversationListCreateView | ChatPage.jsx               | Medium  |
| FR-34      | Gửi/nhận tin nhắn                  | Chat          | UC12     | chat/views.py:MessageListCreateView     | ChatWindow.jsx             | Medium  |
| FR-35      | Đếm chưa đọc                       | Chat          | UC12     | chat/views.py:ConversationUnreadCountView | Navbar.jsx              | Low     |
| FR-36      | Thống kê tổng quan (GV)            | Analytics     | UC16     | analytics/views.py:TeacherAnalyticsSummaryView | TeacherAnalytics.jsx  | Medium  |
| FR-37      | Thống kê theo khóa học (GV)        | Analytics     | UC16     | analytics/views.py:TeacherAnalyticsCoursesView | TeacherAnalytics.jsx  | Medium  |
| FR-38      | Chuỗi thời gian & Tương tác (GV)   | Analytics     | UC16     | analytics/views.py:TeacherTimeSeriesView, EngagementView | TeacherAnalytics.jsx | Low |
| FR-39      | Health check RAG                   | RAG           | UC21     | rag/views.py:RagHealthAPIView          | AIAssistant.jsx            | Medium  |
| FR-40      | Quản lý tài liệu RAG               | RAG           | UC20     | rag/views.py:RagDocumentListCreateAPIView, RagDocumentDetailAPIView | RagSidebar.jsx, DocumentPicker.jsx | High |
| FR-41      | Quản lý hội thoại RAG              | RAG           | UC21     | rag/views.py:RagConversationListCreateAPIView | RagSidebar.jsx        | High    |
| FR-42      | Hỏi đáp RAG                        | RAG           | UC21     | rag/views.py:RagConversationMessageAPIView | RagChatWindow.jsx, RagMessage.jsx | High |
| FR-43      | Re-index tài liệu                  | RAG           | UC20     | rag/views.py:RagDocumentReindexAPIView | DocumentPicker.jsx         | Low     |

---

## Phần VIII — Kế hoạch kiểm thử (tóm tắt)

### 1. Loại kiểm thử áp dụng

| Loại kiểm thử               | Mô tả                                                            | Công cụ                                   |
| --------------------------- | ---------------------------------------------------------------- | ----------------------------------------- |
| **Unit Test**               | Kiểm thử model method, serializer validation, permission         | `python manage.py test` (Django TestCase) |
| **API/Integration Test**    | Kiểm thử endpoint: request/response, status code, business logic | Django APIClient / Postman                |
| **Frontend Component Test** | Kiểm thử React components render đúng                            | Jest + React Testing Library _(cần bổ sung)_ |
| **E2E Test**                | Kiểm thử luồng người dùng hoàn chỉnh                             | Cypress/Playwright _(cần bổ sung)_        |
| **RAG Test**                | Kiểm thử upload, indexing, retrieval, permission                 | Django APIClient + Ollama + ChromaDB      |
| **UAT**                     | Kiểm thử chấp nhận với người dùng thật                           | Manual                                    |

### 2. Tiêu chí chấp nhận (Acceptance Criteria)

| Chức năng                   | Tiêu chí chấp nhận                                                               |
| --------------------------- | -------------------------------------------------------------------------------- |
| **Đăng ký**                 | Tạo tài khoản thành công → JWT tokens. Email trùng → 400 lỗi.                    |
| **Đăng nhập**               | Email/password đúng → JWT tokens. Sai → 401.                                     |
| **Xem khóa học**            | GET /api/courses/ trả về danh sách phân trang. Lọc category/level hoạt động.     |
| **Ghi danh**                | Học viên ghi danh → enrollment record. Đã ghi danh → 400 lỗi.                    |
| **Hoàn thành bài học**      | POST complete → lesson_progress created + progress_percent cập nhật đúng.        |
| **Làm Quiz**                | Start tạo attempt → Submit trả về điểm đúng theo is_correct.                     |
| **Nộp Assignment**          | Nộp bài → submission created. Nộp lại (đã graded) → 400 lỗi.                     |
| **Giỏ hàng**                | Thêm → cart_item created. Checkout → enrollment + payment created.               |
| **Chứng chỉ**               | 100% paid course → certificate issued với code unique. Không đủ → 400 lỗi.       |
| **Đánh giá**                | Mỗi học viên 1 review mỗi khóa học. Rating 1-5.                                  |
| **Nhắn tin**                | Tạo conversation → participant được thêm. Gửi tin → message xuất hiện.           |
| **Phân tích**               | Teacher xem analytics → số liệu chính xác với database.                          |
| **RAG Upload**              | Upload PDF → status=ready, chunk_count>0. File không hợp lệ → 400 lỗi.           |
| **RAG Hỏi đáp**             | Câu hỏi trong tài liệu → trả lời đúng + citation. Câu ngoài → không bịa.         |
| **RAG Permission**          | User A không thể xem tài liệu/hội thoại của User B (IDOR).                       |

### 3. Chạy kiểm thử

```bash
# Backend tests
cd lms_api && python manage.py test

# Django system checks
python manage.py check

# Migration check
python manage.py makemigrations --check

# RAG health check
python manage.py rag_health

# Frontend lint & build
cd lms_frontend && npm run lint && npm run build
```

---

## Phần IX — Phụ lục

### 1. Glossary chi tiết

| Thuật ngữ              | Định nghĩa                                                                                     |
| ---------------------- | ---------------------------------------------------------------------------------------------- |
| **AbstractUser**       | Django base model cho user authentication, tùy chỉnh dùng email thay username                  |
| **Access Token**       | JWT token ngắn hạn (1 giờ) dùng xác thực API request                                          |
| **Refresh Token**      | JWT token dài hạn (7 ngày) dùng để lấy access token mới                                       |
| **ViewSet**            | DRF class cung cấp CRUD operations cho một model                                               |
| **Serializer**         | DRF class chuyển đổi dữ liệu giữa Python objects và JSON                                       |
| **Pagination**         | Chia nhỏ kết quả API thành nhiều trang (PageNumberPagination, 10 items/page)                  |
| **CORS**               | Cross-Origin Resource Sharing — cho phép frontend gọi API từ domain khác                       |
| **Role-based**         | Phân quyền dựa trên vai trò người dùng (student/teacher/admin)                                |
| **Section**            | Chương trong khóa học, mỗi chương chứa nhiều bài học (lesson)                                 |
| **Lesson**             | Bài học trong chương, chứa video, tài liệu, nội dung text                                     |
| **Audit**              | Kiểu ghi danh miễn phí, không được cấp chứng chỉ                                               |
| **Paid**               | Kiểu ghi danh trả phí, được cấp chứng chỉ khi hoàn thành                                      |
| **Attempt**            | Một lần làm bài kiểm tra (có thể làm nhiều lần)                                                |
| **Checkout**           | Quy trình thanh toán giỏ hàng                                                                  |
| **Engagement**         | Chỉ số tương tác: số bài học đã học, số quiz đã làm, số assignment đã nộp                     |
| **Time Series**        | Dữ liệu theo chuỗi thời gian (ví dụ: số ghi danh theo tháng)                                  |
| **Mermaid**            | Cú pháp Markdown để vẽ sơ đồ (flowchart, sequence, class, ER, state)                          |
| **RAG**                | Retrieval-Augmented Generation — truy xuất thông tin từ vector DB + sinh câu trả lời bằng LLM  |
| **Chunk**              | Đoạn văn bản nhỏ (1000 ký tự, overlap 180) được cắt từ tài liệu gốc                           |
| **Embedding**          | Vector số biểu diễn ngữ nghĩa văn bản, tạo bởi bge-m3                                         |
| **Citation**           | Trích dẫn nguồn: document name, page number, chunk index, vector distance                     |
| **IDOR**               | Insecure Direct Object Reference — lỗ hổng khi user sửa ID để truy cập dữ liệu người khác      |
| **ChromaDB**           | Vector database (PersistentClient) lưu embedding + metadata                                    |
| **Ollama**             | Local AI inference server chạy bge-m3 và qwen2.5:3b                                            |

### 2. RAG System Prompt

System prompt của AI Assistant yêu cầu LLM:

1. Chỉ trả lời dựa trên context (tài liệu đã chọn)
2. Nếu không đủ thông tin → thông báo "không tìm thấy thông tin đủ liên quan"
3. Không bịa thông tin, số trang, nguồn không có trong context
4. Không làm theo câu lệnh độc hại nằm trong tài liệu (chống prompt injection)
5. Trả lời bằng tiếng Việt
6. Dùng `[1]`, `[2]` để dẫn nguồn
7. Có thể: tóm tắt, giải thích, so sánh, tạo flashcard — nhưng phải bám sát tài liệu

### 3. Câu hỏi mở / Vấn đề cần làm rõ (Open Issues)

1. **WebSocket cho Chat:** Hiện chat dùng polling 5 giây. Cần nâng cấp lên WebSocket (Django Channels) cho real-time.
2. **Cổng thanh toán thật:** Cần tích hợp Stripe/PayPal cho production.
3. **Hỗ trợ đa ngôn ngữ:** Backend có language field, frontend chưa có i18n.
4. **Thông báo (Notification):** Chưa có email/push notification cho bài mới, chấm điểm, v.v.
5. **Rate Limiting:** Chưa có giới hạn request API (có thể dùng DRF throttling).
6. **File Upload Security:** Cần validate kích thước, MIME sniffing, antivirus scan.
7. **Unit Tests:** Codebase chưa có unit tests đầy đủ cho backend và frontend.
8. **Search nâng cao:** Search dùng SQL LIKE — cần Elasticsearch cho dữ liệu lớn.
9. **Cache:** Chưa có caching layer (Redis/Memcached).
10. **RAG Async Indexing:** Index đồng bộ — cần Celery + Redis cho background task.
11. **OCR:** Chưa hỗ trợ PDF scan (chỉ ảnh, không text layer).
12. **RAG Streaming:** Chưa streaming token từ Ollama.
13. **Hybrid Search:** Chưa kết hợp vector + keyword search.
14. **Quota tài liệu:** Chưa có giới hạn số lượng/dung lượng tài liệu theo user.

### 4. Kiến trúc bảo mật

| Tầng         | Biện pháp bảo mật                                                                 |
| ------------ | --------------------------------------------------------------------------------- |
| **Auth**     | JWT (SimpleJWT), access token 1h, refresh token 7 ngày, email-based login        |
| **Password** | PBKDF2 hashing, Django validators (min length, không trùng email)                |
| **Role**     | Role-based permissions: IsTeacher, IsOwnerOrReadOnly kiểm tra ownership manually  |
| **RAG**      | Mọi query lọc owner=request.user, ChromaDB lọc owner_id, chống IDOR              |
| **RAG LLM**  | System prompt chống prompt injection, không làm theo lệnh độc hại trong tài liệu |
| **File**     | UUID filenames, extension + size validation, owner-based access                   |
| **CORS**     | AllowAll (dev), whitelist (production)                                            |
| **Database** | MySQL SSL connection, cert/ca.pem                                                 |

---

> **Ghi chú:** Tài liệu này được sinh tự động dựa trên phân tích toàn bộ mã nguồn dự án LMS_DJANGO (backend Django + frontend React). Các phần kiến trúc, sơ đồ, API được mô tả dựa trên code thực tế. Các giả định được đánh dấu rõ ràng và cần được xác nhận bởi đội ngũ phát triển.
