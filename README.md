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
│   ├── client.py           # Giao diện dòng lệnh (Terminal/Console)
│   └── client_gui.py       # Giao diện đồ họa trực quan (Pygame)
├── core/  
│   └── hanoi_logic.py      # Thuật toán tháp Hà Nội (Dùng chung cho cả 2 bên)
└── README.md               # Hướng dẫn dự án

## 🛠 Công nghệ sử dụng
- **Ngôn ngữ:** Python 3.x
- **Thư viện chính:** - `socket`: Truyền tải dữ liệu TCP.
  - `threading`: Xử lý đa luồng (nhiều người chơi cùng lúc).
  - `json`: Đóng gói dữ liệu trao đổi giữa Client và Server.

## ⚙️ Cài đặt & Yêu cầu
Trước khi chạy, hãy đảm bảo máy tính đã cài Python và thư viện đồ họa:
pip install pygame

## 🚀 Hướng dẫn Khởi chạy (Localhost)
Bước 1: Khởi động Server
Luôn phải chạy Server trước để mở cổng kết nối.
python server/server.py
Server sẽ lắng nghe tại cổng 5555.

Bước 2: Khởi động Client (Người chơi)
Bạn có thể mở nhiều terminal để giả lập nhiều người chơi.
- Giao diện Đồ họa (GUI): Trải nghiệm kéo thả, chọn tầng.
  python client/client_gui.py
- Giao diện Dòng lệnh (Terminal): Dành cho máy cấu hình thấp hoặc debug.
  python client/client.py

## 🌐 Hướng dẫn chơi Online (2 máy khác nhau)
Sử dụng Radmin VPN để tạo mạng LAN ảo thi đấu giữa các máy tính khác mạng Wifi.
1. Cài đặt: Tải Radmin VPN cho cả 2 máy (Máy Server và Máy Client).
2. Kết nối:
- Máy A (Server): Bấm Create Network -> Đặt tên & Mật khẩu.
- Máy B (Client): Bấm Join Network -> Nhập tên & Mật khẩu của Máy A.
3. Lấy IP: Tại Radmin VPN của Máy A, click chuột phải vào tên máy mình -> Copy IP Address (Ví dụ: 26.155.20.10).
4. Cấu hình Code:
- Mở file client/client_gui.py trên Máy B.
- Tìm dòng SERVER_IP = '127.0.0.1' và đổi thành IP vừa copy:
  SERVER_IP = '26.155.20.10' # Thay bằng IP Radmin của máy Server

## 🕹 Quy tắc & Cách chơi
1. Chế độ chơi
- Solo Mode: Chơi một mình để luyện tập thuật toán.
- Race Mode: Thi đấu nhiều người. Ai hoàn thành tháp nhanh nhất sẽ thắng. Server tự động thông báo kết quả cho tất cả người chơi.

2. Tùy chọn độ khó
- Người chơi được chọn số tầng tháp từ 3 đến 7 tầng.

3. Thao tác điều khiển
- Trên GUI: Click chuột vào Cột Nguồn (để nhấc đĩa) -> Click vào Cột Đích (để thả đĩa).
- Trên Terminal: Nhập tọa độ [Nguồn] [Đích]. Ví dụ: 0 2 (Chuyển từ cột 0 sang cột 2).

## 🔧 Khắc phục lỗi thường gặp
Lỗi: "Address already in use" hoặc không bật được Server
  - Nguyên nhân: Cổng 5555 chưa được giải phóng do lần chạy trước tắt không đúng cách.
  - Cách sửa (Windows): Mở Terminal và chạy lệnh:
    netstat -ano | findstr :5555
    taskkill /F /PID <PID_TIM_DUOC>
    (Thay <PID_TIM_DUOC> bằng số PID hiện ra ở lệnh trên).