# Mini-game
# Tower of Hanoi - Multiplayer Race (Socket Programming)

## Giới thiệu
Dự án Mini Game giữa kỳ môn Lập trình mạng. Ứng dụng mô hình **Multi-Client Server** sử dụng ngôn ngữ **Python** để xây dựng trò chơi Tháp Hà Nội dưới dạng thi đấu trực tiếp (Race Mode).

## 👥 Thành viên nhóm
1. **Nguyễn Phi Long** - Leader: Phát triển Server và Quản lý kết nối.
2. **Lê Minh Đức** - Developer: Xử lý Logic trò chơi & Thuật toán.
3. **Chung Tiểu Phi** - Developer: Xây dựng giao diện Client & Xử lý sự kiện.

## 🛠 Công nghệ sử dụng
- **Ngôn ngữ:** Python 3.x
- **Thư viện chính:** - `socket`: Truyền tải dữ liệu TCP.
  - `threading`: Xử lý đa luồng (nhiều người chơi cùng lúc).
  - `json`: Đóng gói dữ liệu trao đổi giữa Client và Server.

## 🕹 Quy tắc trò chơi (Race Mode)
1. Server khởi tạo một bàn cờ Tháp Hà Nội với số tầng quy định.
2. Nhiều người chơi có thể kết nối vào Server cùng một lúc.
3. Khi Server ra lệnh **"START"**, tất cả người chơi bắt đầu giải đố.
4. Client nào giải xong tháp (di chuyển toàn bộ đĩa sang cột mục tiêu) nhanh nhất sẽ gửi tín hiệu về Server.
5. Server dừng cuộc chơi và thông báo người chiến thắng cho toàn bộ người tham gia.

## 🚀 Hướng dẫn cài đặt & Chạy
1. **Khởi động Server:**
   ```bash
   python server/server.py