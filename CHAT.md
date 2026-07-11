# CHAT.md

## Mục tiêu

Triển khai chức năng chat cho hệ thống LMS.

**Tech stack** - Backend: Django - Database: MySQL - Frontend: ReactJS +
Vite

## Yêu cầu bắt buộc

Trước khi thực hiện bất kỳ công việc nào, **AI PHẢI đọc file
`database.sql`** để hiểu chính xác cấu trúc CSDL hiện có.

Không được: - tự suy luận schema - tự tạo bảng nếu chưa kiểm tra
`database.sql` - tự đổi tên bảng/cột - tự thêm quan hệ không tồn tại -
tự mở rộng yêu cầu

Mọi thao tác phải dựa trên cấu trúc trong `database.sql`.

## Phạm vi

Chỉ triển khai chức năng chat cơ bản giống Messenger.

Bao gồm: - Chat 1-1 - Group chat (\>2 người) - Chỉ hỗ trợ tin nhắn text.

Không triển khai: - voice - video - file - image - sticker - emoji
reaction - nickname - theme - poll - pin - reply - forward - message
recall - typing indicator - read receipt - online status - call - bất kỳ
chức năng nào không được mô tả.

## Quy tắc tạo cuộc trò chuyện

Không tồn tại khái niệm kết bạn.

Người dùng nhập email.

### Trường hợp 1

Nhập đúng 1 email.

Nếu email tồn tại: - tạo cuộc chat 1-1 giữa hai tài khoản nếu chưa có. -
nếu đã có thì mở lại cuộc chat đó.

### Trường hợp 2

Nhập nhiều email.

Nếu tất cả email hợp lệ: - tạo group chat. - tất cả thành viên đều được
thêm vào group. - người tạo cũng là thành viên.

Không tạo group nếu có email không hợp lệ.

## Tin nhắn

Chỉ gồm: - nội dung text - người gửi - thời gian gửi

## Giao diện

Tham khảo Messenger.

Bao gồm: - danh sách cuộc trò chuyện bên trái - khung chat bên phải - ô
nhập text - nút gửi - danh sách thành viên đối với group

Không sao chép toàn bộ Messenger.

Chỉ tham khảo bố cục và chức năng chat cơ bản.

## Backend

Thực hiện đầy đủ API cần thiết phục vụ: - tạo chat - tạo group - lấy
danh sách conversation - lấy lịch sử tin nhắn - gửi tin nhắn - lấy thông
tin conversation

Không tạo API ngoài phạm vi.

## Frontend

Thực hiện: - Conversation List - Chat Window - Message List - Message
Input - Create Chat Dialog (nhập email)

## Quy tắc triển khai

-   Không thay đổi các module không liên quan.
-   Không sửa cấu trúc database nếu chưa được yêu cầu.
-   Không thêm tính năng ngoài mô tả.
-   Chỉ sử dụng dữ liệu đã tồn tại trong `database.sql`.
-   Nếu phát hiện thiếu cấu trúc trong `database.sql`, dừng triển khai
    và báo rõ phần còn thiếu, không tự ý bổ sung.

## Thứ tự thực hiện

1.  Đọc `database.sql`.
2.  Hiểu schema hiện có.
3.  Xác định các bảng liên quan.
4.  Thiết kế chức năng chat dựa trên schema đó.
5.  Triển khai backend.
6.  Triển khai frontend.
7.  Kiểm tra toàn bộ luồng.

AI phải tuyệt đối tuân thủ tài liệu này.
