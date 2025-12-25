import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('IP_SERVER', 5555))

while True:
    # Nhận trạng thái tháp từ Server
    # Vẽ tháp ra màn hình Console (dùng các ký tự | và -)
    # Nhập nước đi (Ví dụ: "0 2" để chuyển đĩa từ tháp 0 sang tháp 2)
    # Gửi về Server 
    pass