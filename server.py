import socket
import threading

clients = []
scores = {}

def handle_client(conn, addr):
    # Gửi đề bài cho client
    # Nhận từng nước đi của client và kiểm tra qua hanoi_logic
    # Nếu client nào báo is_won() đầu tiên -> Thông báo người thắng cho tất cả
    pass

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen()