import socket
import os

HOST = '127.0.0.1'
PORT = 5555

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(10)
    
    print("Dang ket noi den Server...", flush=True)
    
    try:
        client.connect((HOST, PORT))
        client.settimeout(None)  # Remove timeout after connection
        print("Ket noi thanh cong!", flush=True)
    except socket.timeout:
        print("Loi: Khong the ket noi (timeout)", flush=True)
        return
    except Exception as e:
        print(f"Loi ket noi: {e}", flush=True)
        return
    
    try:
        buffer = ""  # Buffer for incomplete messages
        
        while True:
            # Receive data from server
            data = client.recv(4096).decode()
            
            if not data:
                print("\nServer da ngat ket noi", flush=True)
                break
            
            buffer += data
            
            # Check if we need to clear screen for tower display
            if "TRANG THAI THAP" in buffer:
                clear_screen()
                print(buffer, end="", flush=True)
                buffer = ""
                continue
            
            # Display the received data
            print(buffer, end="", flush=True)
            
            # Check if server is requesting input
            # Look for prompts that end with ':' or contain 'Nhap'
            if buffer.strip().endswith(":") or "Nhap" in buffer:
                # Clear buffer after displaying prompt
                buffer = ""
                
                # Get user input
                user_input = input()
                
                # Send input to server
                client.sendall(user_input.encode())
            
            # Check for game over messages
            elif "CHUC MUNG" in buffer or "GAME OVER" in buffer or "THANG" in buffer:
                # Game ended, wait a moment then continue receiving
                buffer = ""
                continue
            
            # If buffer is getting too long without a prompt, display and clear it
            elif len(buffer) > 500:
                buffer = ""
                
    except KeyboardInterrupt:
        print("\n\nNgat ket noi boi nguoi dung", flush=True)
    except Exception as e:
        print(f"\nMat ket noi: {e}", flush=True)
    finally:
        client.close()
        print("Da dong ket noi.", flush=True)

if __name__ == "__main__":
    start_client()