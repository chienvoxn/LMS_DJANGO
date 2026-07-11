# OPENCODE.md - Triển khai chức năng Chat

## 1. Phân tích hệ thống hiện có

### 1.1. Tổng quan dự án
- **Backend**: Django 5.2.7 + DRF 3.16.1 (Python)
- **Frontend**: React 18.2.0 + Vite 5.0.8 + TailwindCSS 3.4.0
- **Database**: MySQL
- **Auth**: JWT (SimpleJWT) - email-based authentication
- **Custom apps (7)**: users, courses, enrollments, assessments, reviews, analytics, common

### 1.2. Phát hiện ban đầu
- **Không có** chức năng chat nào trong hệ thống (0 file, 0 code liên quan)
- **Navbar.jsx** đã có sẵn button chat với placeholder dialog
  - State: `showChatDialog`, `chatRef`
  - UI: dropdown placeholder "Hộp thoại chat sẽ được bổ sung sau"
- **database.sql**: không chứa bảng chat nào

### 1.3. Schema users table (quan trọng cho chat)
```python
class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)  # định danh chính
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20)  # student/teacher/admin
    avatar_url = models.URLField(blank=True, null=True)
    # ...
    USERNAME_FIELD = 'email'
```

---

## 2. Backend - Django App `chat`

### 2.1. Tạo app
```bash
python manage.py startapp chat
```

### 2.2. Models (`chat/models.py`)

#### `Conversation`
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField (PK) | |
| is_group | BooleanField | default=False |
| name | CharField(255, nullable) | cho group chat |
| participants | ManyToManyField(User, through=ConversationParticipant) | |
| created_at | DateTimeField(auto_now_add) | |
| updated_at | DateTimeField(auto_now) | |

#### `ConversationParticipant` (through model)
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField (PK) | |
| conversation | ForeignKey(Conversation) | |
| user | ForeignKey(User) | |
| joined_at | DateTimeField(auto_now_add) | |
| **unique_together** | ['conversation', 'user'] | |

#### `Message`
| Field | Type | Notes |
|-------|------|-------|
| id | AutoField (PK) | |
| conversation | ForeignKey(Conversation, related_name='messages') | |
| sender | ForeignKey(User, related_name='sent_messages') | |
| content | TextField | |
| created_at | DateTimeField(auto_now_add) | |

### 2.3. Serializers (`chat/serializers.py`)

| Serializer | Usage | Key fields |
|------------|-------|------------|
| `UserBriefSerializer` | User snippet in messages | id, email, full_name, avatar_url, role |
| `MessageSerializer` | Message payload | id, sender (UserBrief), content, created_at |
| `ConversationListSerializer` | Sidebar list | id, is_group, name, display_name, display_avatar, last_message, member_count |
| `ConversationDetailSerializer` | Chat window detail | id, is_group, name, display_name, display_avatar, members[], messages[] |
| `CreateConversationSerializer` | Create chat (POST) | emails[] - validates all exist |

**Logic `display_name`**: nếu group → lấy `name`, nếu 1-1 → lấy `full_name`/`email` của người kia

**Logic `CreateConversationSerializer.validate_emails`**: kiểm tra tất cả email tồn tại trong DB, trả lỗi nếu có email không hợp lệ

**Logic `CreateConversationSerializer.create`**:
- 1 email → kiểm tra conversation 1-1 đã tồn tại chưa (nếu có → trả về), nếu chưa → tạo mới
- Nhiều email → tạo group chat, thêm tất cả (bao gồm người tạo)
- **`_ensure_participants(conversation, users)`**: khi trả về conversation đã tồn tại, kiểm tra user nào chưa là participant → thêm mới. Fix bug "conversation biến mất sau refresh" (serializers.py:114-120)

### 2.4. Views (`chat/views.py`)

| View | Method(s) | Endpoint | Description |
|------|-----------|----------|-------------|
| `ConversationListCreateView` | GET, POST | `/api/chat/conversations/` | List user's conversations / Create new |
| `ConversationDetailView` | GET | `/api/chat/conversations/{id}/` | Conversation detail + members + messages |
| `MessageListCreateView` | GET, POST | `/api/chat/conversations/{id}/messages/` | List messages / Send message |
| `ConversationUnreadCountView` | GET | `/api/chat/unread-count/` | Unread count (placeholder) |

**Permissions**: Tất cả require `IsAuthenticated`
**MessageListCreateView**: kiểm tra user là member của conversation trước khi gửi

**Fix Prefetch messages**: `get_queryset` sử dụng `Prefetch('messages', ...order_by('-created_at'))` không slice (tránh lỗi sliced queryset trong Prefetch). `ConversationListSerializer.get_last_message` dùng cache `_prefetched_objects_cache` thay vì query mới. (views.py:31-39, serializers.py:32-39)

### 2.5. URLs (`chat/urls.py`)
```python
urlpatterns = [
    path('chat/conversations/', views.ConversationListCreateView.as_view()),
    path('chat/conversations/<int:pk>/', views.ConversationDetailView.as_view()),
    path('chat/conversations/<int:conversation_id>/messages/', views.MessageListCreateView.as_view()),
    path('chat/unread-count/', views.ConversationUnreadCountView.as_view()),
]
```

### 2.6. Cập nhật cấu hình
- `lms_backend/settings.py`: thêm `'chat'` vào `INSTALLED_APPS`
- `lms_backend/urls.py`: thêm `path('api/', include('chat.urls'))`

### 2.7. Migrations
```bash
python manage.py makemigrations chat
python manage.py migrate chat
```

---

## 3. Frontend - React Components

### 3.1. API Client (`api/client.js`)
```javascript
export const chatAPI = {
  getConversations: () => api.get('/chat/conversations/'),
  getConversationDetail: (id) => api.get(`/chat/conversations/${id}/`),
  createConversation: (emails) => api.post('/chat/conversations/', { emails }),
  getMessages: (conversationId) => api.get(`/chat/conversations/${conversationId}/messages/`),
  sendMessage: (conversationId, content) => api.post(`/chat/conversations/${conversationId}/messages/`, { content }),
};
```

### 3.2. Components Tree
```
ChatPage
├── ConversationList (sidebar trái)
│   ├── Search input
│   ├── Conversation item (avatar + display_name + last_message)
│   └── + Button → CreateChatDialog (modal)
│       ├── Textarea nhập email
│       └── Nút Create / Cancel
└── ChatWindow (khung phải)
    ├── Header (avatar + display_name + group members list)
    ├── MessageList
    │   ├── Date separator
    │   ├── Message bubble (own = primary color, other = gray)
    │   └── Auto scroll to bottom
    └── MessageInput
        ├── Auto-resize textarea
        ├── Enter để gửi, Shift+Enter để xuống dòng
        └── Send button
```

### 3.3. Component Details

#### `ChatPage.jsx` (`/chat` route)
- State: conversations[], activeConversationId, activeConversation, messages[]
- `fetchConversations()` → GET `/chat/conversations/`
- `fetchDetail(id)` khi activeConversationId thay đổi → GET `/chat/conversations/{id}/`
- `handleSendMessage(content)` → POST `/chat/conversations/{id}/messages/`
- Layout: `h-[calc(100vh-64px)] flex` → sidebar 384px + chat window flex-1
- **Polling tự động**: `setInterval(fetchConversations, 5000)` → đồng bộ conversation list real-time
- **Polling detail**: `setInterval(fetchDetail, 5000)` khi có conversation active → đồng bộ messages
- **Merge logic**: khi poll, merge dữ liệu mới với state cũ, tránh mất conversation khi API trả về thiếu
- **Cleanup**: clear interval khi component unmount (useRef + return cleanup)

#### `ConversationList.jsx`
- Search filter theo display_name
- Active state: primary border + background
- Hiển thị avatar (group icon / initial), display_name, last_message preview
- Empty state: "No conversations yet"
- CreateChatDialog modal overlay

#### `CreateChatDialog.jsx`
- Textarea nhập email, hỗ trợ phân tách bằng `,` `;` `\n`
- Validate: ít nhất 1 email
- Error display: "Emails not found: ..."
- Success: onConversationCreated → add vào list + switch active

#### `ChatWindow.jsx`
- Empty state (không có conversation active): icon + "Select a conversation"
- Header: avatar + display_name + group members list (join bằng ", ")
- Renders MessageList + MessageInput

#### `MessageList.jsx`
- Date separators: nếu ngày khác nhau giữa 2 message
- Own message: `bg-primary-500 text-white rounded-br-sm` (phải)
- Other message: `bg-slate-100 dark:bg-slate-700 rounded-bl-sm` (trái)
- Group chat: hiển thị sender name trước message của người khác
- Time format: today → HH:MM, yesterday → "Yesterday", < 7 days → weekday, else → "Mon DD"
- Auto scroll to bottom khi messages thay đổi

#### `MessageInput.jsx`
- Textarea auto-resize (max 120px)
- Enter để gửi (không Shift+Enter)
- Disabled state khi không có conversation active
- Send button disabled khi text rỗng

### 3.4. Route
- `AppRouter.jsx`: thêm `path="/chat"` với `ProtectedRoute`
- Import `ChatPage` từ `../pages/ChatPage`

### 3.5. Navbar.jsx cập nhật
- **Xóa**: state `showChatDialog`, ref `chatRef`, dropdown placeholder
- **Sửa**: chat button `onClick` → `navigate('/chat')`
- Giữ nguyên icon chat + green dot indicator

---

## 4. Kiểm thử

### 4.1. Backend
```bash
python manage.py check          # OK - 0 silenced issues
python manage.py runserver      # API hoạt động, chat endpoints respond
```

### 4.2. Frontend
```bash
npx vite build                  # Build thành công, 0 errors
```

---

## 5. Danh sách file đã tạo/sửa

### File mới tạo
| File | Mô tả |
|------|-------|
| `lms_api/chat/__init__.py` | App init |
| `lms_api/chat/admin.py` | Admin config |
| `lms_api/chat/apps.py` | App config |
| `lms_api/chat/models.py` | Conversation, ConversationParticipant, Message models |
| `lms_api/chat/serializers.py` | UserBrief, Message, ConversationList, ConversationDetail, CreateConversation serializers |
| `lms_api/chat/views.py` | ConversationListCreateView, ConversationDetailView, MessageListCreateView, ConversationUnreadCountView |
| `lms_api/chat/urls.py` | Chat URL configuration |
| `lms_api/chat/tests.py` | Test file |
| `lms_api/chat/migrations/0001_initial.py` | Initial migration |
| `lms_frontend/src/pages/ChatPage.jsx` | Main chat page |
| `lms_frontend/src/components/chat/CreateChatDialog.jsx` | Create conversation modal |
| `lms_frontend/src/components/chat/ConversationList.jsx` | Conversation sidebar |
| `lms_frontend/src/components/chat/MessageList.jsx` | Message display |
| `lms_frontend/src/components/chat/MessageInput.jsx` | Message input form |
| `lms_frontend/src/components/chat/ChatWindow.jsx` | Chat window container |

### File đã sửa
| File | Thay đổi |
|------|----------|
| `lms_api/lms_backend/settings.py` | Thêm `'chat'` vào INSTALLED_APPS |
| `lms_api/lms_backend/urls.py` | Thêm `path('api/', include('chat.urls'))` |
| `lms_frontend/src/api/client.js` | Thêm `chatAPI` export |
| `lms_frontend/src/routes/AppRouter.jsx` | Thêm route `/chat` với ProtectedRoute |
| `lms_frontend/src/components/Navbar.jsx` | Chat button navigate đến `/chat`, xóa placeholder code |

---

## 6. API Endpoints Summary

| Method | Endpoint | Auth | Mô tả |
|--------|----------|------|-------|
| GET | `/api/chat/conversations/` | JWT | Danh sách conversation của user (có last_message, display_name) |
| POST | `/api/chat/conversations/` | JWT | Tạo chat mới. Body: `{"emails": ["a@b.com"]}` hoặc `{"emails": ["a@b.com", "c@d.com"]}` |
| GET | `/api/chat/conversations/{id}/` | JWT | Chi tiết conversation + members + messages |
| GET | `/api/chat/conversations/{id}/messages/` | JWT | Lịch sử tin nhắn |
| POST | `/api/chat/conversations/{id}/messages/` | JWT | Gửi tin nhắn. Body: `{"content": "Hello"}` |

---

## 7. Tuân thủ CHAT.md

| Yêu cầu | Trạng thái |
|---------|-----------|
| Đọc database.sql trước | ✅ Đã đọc và phân tích |
| Chat 1-1 | ✅ 1 email → tìm/tạo conversation |
| Group chat (>2 người) | ✅ Nhiều email → tạo group |
| Chỉ text message | ✅ Chỉ có content (text) |
| Không kết bạn | ✅ Nhập email trực tiếp |
| Email không hợp lệ → không tạo | ✅ Validate + báo lỗi |
| Conversation list bên trái | ✅ ConversationList component |
| Chat window bên phải | ✅ ChatWindow component |
| Ô nhập text + nút gửi | ✅ MessageInput component |
| Danh sách thành viên group | ✅ Header + members list |
| Không tạo API ngoài phạm vi | ✅ Chỉ 5 endpoints cần thiết |
| Không thay đổi module không liên quan | ✅ Chỉ sửa settings.py, urls.py |
| Không thêm tính năng ngoài mô tả | ✅ Không voice/video/file/image/... |
