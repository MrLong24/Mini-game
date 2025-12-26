# Mini-game
# Tower of Hanoi - Multiplayer Race (Socket Programming)

## Giới thiệu
Dự án Mini Game giữa kỳ môn Lập trình mạng. Ứng dụng mô hình **Multi-Client Server** sử dụng ngôn ngữ **Python** để xây dựng trò chơi Tháp Hà Nội dưới dạng thi đấu trực tiếp (Race Mode).

## 👥 Thành viên nhóm
1. **Nguyễn Phi Long** - Leader: Phát triển Server và Quản lý kết nối.
2. **Lê Minh Đức** - Developer: Xử lý Logic trò chơi & Thuật toán.
3. **Chung Tiểu Phi** - Developer: Xây dựng giao diện Client & Xử lý sự kiện.

## Cấu trúc thư mục
Mini-game/  
├── server/  
│   └── server.py           # Xử lý kết nối, luồng và trọng tài  
├── client/
│   └── client.py           # Giao diện người dùng (UI) và nhận input  
├── core/
│   └── hanoi_logic.py      # Thuật toán tháp Hà Nội (Dùng chung cho cả 2 bên)  
└── README.md               # Hướng dẫn dự án

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
   ```
  - Mở 1 terminal mới và gõ lệnh phía dưới để chơi:
    ```bash
    python client/client.py
2. **Cách xử lý khi lỡ tắt terminal mà Server đang chạy:**
    Cần phải giải phóng Port server đó.
    - Mở Terminal và gõ lệnh sau để tìm ID của tiến trình:
    ```bash
    netstat -ano | findstr :5555
    ```
    - Kết quả sẽ hiện ra một dòng có số ở cuối (ví dụ: 1234). Đó là **PID**.
    - Gõ lệnh sau để tắt nó (thay 1234 bằng số PID bạn thấy):
    ```bash
    taskkill /F /PID 1234