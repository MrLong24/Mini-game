import socket
import os

HOST = '127.0.0.1' # IP của Server (Nếu chạy khác máy thì đổi IP này)
PORT = 5555

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Dang ket noi den Server...", flush=True) # Thêm dòng này để theo dõi
    try:
        client.connect((HOST, PORT))
        print("Ket noi thanh cong!", flush=True)
    except Exception as e:
        print(f"Loi ket noi: {e}", flush=True)
        return

    while True:
        try:
            data = client.recv(4096).decode()
            if not data: break
            
            if "TRANG THAI THAP" in data:
                clear_screen()
                print(data, flush=True)
            else:
                # Quan trọng: Thêm flush=True ở đây
                print(data, end="", flush=True) 

            if data.strip().endswith(":"):
                user_input = input()
                client.send(user_input.encode())
        except Exception as e:
            print(f"Loi: {e}", flush=True)
            break

if __name__ == "__main__":
    start_client()