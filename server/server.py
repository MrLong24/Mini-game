import socket
import threading
import sys
import os

# Thêm đường dẫn để import được package 'core'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.hanoi_logic import HanoiGame

# Cấu hình Server
HOST = '127.0.0.1'
PORT = 5555

# Biến toàn cục cho Race Mode
race_room = []          # Danh sách người chơi đang đợi
race_lock = threading.Lock()
race_winner = None      # Lưu tên người thắng cuộc
game_active = False     # Trạng thái game đang chạy hay chưa

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("CHAO MUNG DEN VOI GAME THAP HA NOI!\n1. Choi Don (Solo)\n2. Thi Dau (Race)\nChon che do (1/2): ".encode())
    
    try:
        mode = conn.recv(1024).decode().strip()
        if mode == '1':
            play_solo(conn)
        elif mode == '2':
            play_race(conn, addr)
        else:
            conn.send("Lua chon khong hop le. Bye!".encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def play_solo(conn):
    conn.send("--- BAT DAU SOLO MODE ---\n".encode())
    game = HanoiGame(disks=3)
    
    while not game.is_won():
        # Gửi bàn cờ hiện tại
        conn.send(game.render_str().encode())
        conn.send("Nhap nuoc di (Vi du: 0 1): ".encode())
        
        # Nhận nước đi
        move_data = conn.recv(1024).decode().strip()
        if not move_data: break
        
        try:
            parts = move_data.split()
            f, t = int(parts[0]), int(parts[1])
            success, msg = game.move_disk(f, t)
            conn.send(f"\n>>> {msg}\n".encode())
        except:
            conn.send("\n>>> Loi cu phap! Nhap lai (VD: 0 2)\n".encode())

    # Thắng
    conn.send(game.render_str().encode())
    conn.send("\nCHUC MUNG! BAN DA GIAI THANH CONG!\n".encode())

def play_race(conn, addr):
    global race_room, game_active, race_winner
    
    conn.send("Dang tim doi thu... Vui long doi...\n".encode())
    
    # Thêm vào phòng chờ
    with race_lock:
        race_room.append(conn)
    
    # Chờ đủ 2 người
    while len(race_room) < 2:
        pass # Chờ đợi (Busy wait đơn giản cho demo)
    
    if not game_active:
        game_active = True
        race_winner = None

    conn.send("DOI THU DA VAO! START GAME!!!\n".encode())
    
    game = HanoiGame(disks=3)
    
    while not game.is_won():
        # Kiểm tra xem có ai thắng chưa
        if race_winner:
            conn.send(f"\nGAME OVER! Nguoi thang la: {race_winner}\n".encode())
            return

        conn.send(game.render_str().encode())
        conn.send("Nhap nuoc di (Race): ".encode())
        
        move_data = conn.recv(1024).decode().strip()
        if not move_data: break
        
        try:
            parts = move_data.split()
            f, t = int(parts[0]), int(parts[1])
            success, msg = game.move_disk(f, t)
            conn.send(f"\n>>> {msg}\n".encode())
        except:
            conn.send("\n>>> Loi cu phap!\n".encode())

    # Nếu thoát vòng lặp -> Người này thắng
    if race_winner is None:
        race_winner = str(addr)
        conn.send("\nBAN LA NGUOI CHIEN THANG!!! VO DICH THIEN HA!\n".encode())

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
    except OSError:
        print(f"Loi: Port {PORT} dang bi chiem. Hay thu doi PORT khac!")
        return
    server.listen()
    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()