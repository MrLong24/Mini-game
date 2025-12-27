import socket
import threading
import sys
import os
import time

# Add path to import 'core' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.hanoi_logic import HanoiGame

# Server Configuration
HOST = '127.0.0.1'
PORT = 5555

# Global variables for Race Mode
race_room = []          # List of waiting players
race_lock = threading.Lock()
race_winner = None      # Winner name
game_active = False     # Game status


def handle_client(conn, addr):
    """
    Handle each client connection in a separate thread
    """
    print(f"[NEW CONNECTION] {addr} connected.", flush=True)
    
    try:
        # Send welcome message
        welcome_msg = (
            "CHAO MUNG DEN VOI GAME THAP HA NOI!\n"
            "1. Choi Don (Solo)\n"
            "2. Thi Dau (Race)\n"
            "Chon che do (1/2): "
        )
        conn.send(welcome_msg.encode())
        
        # 1. Receive game mode (1: Solo, 2: Race)
        mode = conn.recv(1024).decode().strip()
        print(f"[{addr}] Selected mode: {mode}", flush=True)
        
        if not mode or mode not in ['1', '2']:
            conn.send("Lua chon khong hop le!\n".encode())
            return
        
        # 2. Send disk selection prompt
        disk_prompt = "\nChon so tang (3-7): "
        conn.send(disk_prompt.encode())
        
        # 3. Receive number of disks
        disk_data = conn.recv(1024).decode().strip()
        print(f"[{addr}] Disk selection received: '{disk_data}'", flush=True)
        
        num_disks = int(disk_data) if disk_data.isdigit() else 3
        num_disks = max(3, min(7, num_disks))  # Limit to 3-7
        print(f"[{addr}] Number of disks: {num_disks}", flush=True)
        
        # Route to appropriate game mode
        if mode == '1':
            play_solo(conn, addr, num_disks)
        elif mode == '2':
            play_race(conn, addr, num_disks)
            
    except Exception as e:
        print(f"[ERROR] {addr}: {e}", flush=True)
    finally:
        print(f"[DISCONNECTED] {addr}", flush=True)
        conn.close()

def play_solo(conn, addr, num_disks):
    """
    Solo game mode - single player against the puzzle
    Args:
        conn: socket connection
        addr: client address
        num_disks: number of disks (3-7)
    """
    print(f"[SOLO MODE] {addr} started with {num_disks} disks", flush=True)
    
    conn.send("--- BAT DAU SOLO MODE ---\n".encode())
    time.sleep(0.1)  # Small delay for message ordering
    
    game = HanoiGame(disks=num_disks)
    start_time = time.time()
    
    while not game.is_won():
        try:
            # Send current board state
            board_state = game.render_str()
            conn.send(board_state.encode())
            
            # Request move
            conn.send("Nhap nuoc di (Vi du: 0 1): ".encode())
            
            # Receive move
            move_data = conn.recv(1024).decode().strip()
            if not move_data:
                print(f"[SOLO] {addr} disconnected during game", flush=True)
                break
            
            # Parse and validate move
            try:
                parts = move_data.split()
                if len(parts) != 2:
                    conn.send("\n>>> Loi cu phap! Nhap 2 so (VD: 0 2)\n".encode())
                    continue
                    
                from_tower = int(parts[0])
                to_tower = int(parts[1])
                
                # Execute move
                success, msg = game.move_disk(from_tower, to_tower)
                conn.send(f"\n>>> {msg}\n".encode())
                
            except ValueError:
                conn.send("\n>>> Loi: Vui long nhap so (VD: 0 2)\n".encode())
            except Exception as e:
                conn.send(f"\n>>> Loi: {str(e)}\n".encode())
                
        except Exception as e:
            print(f"[SOLO ERROR] {addr}: {e}", flush=True)
            break
    
    # Game completed
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    
    # Send final state and congratulations
    conn.send(game.render_str().encode())
    victory_msg = f"\nCHUC MUNG! BAN DA GIAI XONG TRONG {duration} GIAY!\n"
    victory_msg += f"Tong so nuoc di: {game.moves_count}\n"
    conn.send(victory_msg.encode())
    
    print(f"[SOLO COMPLETED] {addr} finished in {duration}s with {game.moves_count} moves", flush=True)

def play_race(conn, addr, num_disks):
    """
    Race mode - two players compete to solve first
    Enhanced with proper winner notification to both players
    """
    global race_room, game_active, race_winner
    
    print(f"[RACE MODE] {addr} joining race with {num_disks} disks", flush=True)
    
    conn.send("Dang tim doi thu... Vui long doi...\n".encode())
    
    # Add to waiting room
    with race_lock:
        race_room.append((conn, addr))  # Store both conn and addr
        players_waiting = len(race_room)
    
    print(f"[RACE] Players in room: {players_waiting}/2", flush=True)
    
    # Wait for second player
    while len(race_room) < 2:
        time.sleep(0.5)
    
    # Initialize race if first player
    with race_lock:
        if not game_active:
            game_active = True
            race_winner = None
    
    conn.send("DOI THU DA VAO! START GAME!!!\n".encode())
    time.sleep(0.2)
    
    game = HanoiGame(disks=num_disks)
    start_time = time.time()
    
    # Set socket to non-blocking mode for winner checks
    conn.setblocking(False)
    
    while not game.is_won():
        # CRITICAL: Check if opponent won FIRST
        if race_winner and race_winner != str(addr):
            conn.setblocking(True)
            loss_msg = f"\n\n{'='*40}\n"
            loss_msg += f"GAME OVER!\n"
            loss_msg += f"Nguoi choi {race_winner} da thang cuoc!\n"
            loss_msg += f"{'='*40}\n"
            try:
                conn.send(loss_msg.encode())
            except:
                pass
            print(f"[RACE] {addr} notified of loss", flush=True)
            
            # Clean up and exit
            time.sleep(1)
            with race_lock:
                if (conn, addr) in race_room:
                    race_room.remove((conn, addr))
                if len(race_room) == 0:
                    game_active = False
                    race_winner = None
            return
        
        try:
            # Send board state
            board_data = game.render_str()
            conn.send(board_data.encode())
            time.sleep(0.05)  # Small delay for message ordering
            
            conn.send("Nhap nuoc di (Race): ".encode())
            
            # Try to receive move with timeout
            move_received = False
            timeout_counter = 0
            max_timeout = 20  # 2 seconds total (20 * 0.1s)
            
            while not move_received and timeout_counter < max_timeout:
                # Check winner status during wait
                if race_winner and race_winner != str(addr):
                    break
                
                try:
                    move_data = conn.recv(1024).decode().strip()
                    if move_data:
                        move_received = True
                        break
                except BlockingIOError:
                    # No data available yet
                    time.sleep(0.1)
                    timeout_counter += 1
                    continue
                except Exception as e:
                    print(f"[RACE ERROR] {addr} recv error: {e}", flush=True)
                    break
            
            # If opponent won during wait, break immediately
            if race_winner and race_winner != str(addr):
                continue  # Loop will catch this and send notification
            
            if not move_received:
                continue
            
            if not move_data:
                print(f"[RACE] {addr} disconnected", flush=True)
                break
            
            # Parse move
            try:
                parts = move_data.split()
                if len(parts) != 2:
                    conn.send("\n>>> Loi cu phap! (VD: 0 2)\n".encode())
                    continue
                
                from_tower = int(parts[0])
                to_tower = int(parts[1])
                
                success, msg = game.move_disk(from_tower, to_tower)
                conn.send(f"\n>>> {msg}\n".encode())
                
            except ValueError:
                conn.send("\n>>> Loi: Nhap so! (VD: 0 2)\n".encode())
                
        except Exception as e:
            print(f"[RACE ERROR] {addr}: {e}", flush=True)
            break
    
    # Restore blocking mode
    conn.setblocking(True)
    
    # Player finished - check if winner
    end_time = time.time()
    duration = round(end_time - start_time, 2)
    
    with race_lock:
        if race_winner is None and game.is_won():
            # This player won!
            race_winner = str(addr)
            victory_msg = f"\n\n{'='*50}\n"
            victory_msg += f"★★★ BAN LA NGUOI CHIEN THANG! ★★★\n"
            victory_msg += f"Thoi gian: {duration} giay\n"
            victory_msg += f"So nuoc di: {game.moves_count}\n"
            victory_msg += f"{'='*50}\n"
            try:
                conn.send(victory_msg.encode())
            except:
                pass
            print(f"[RACE WON] {addr} won in {duration}s", flush=True)
            
            # Notify the other player
            time.sleep(0.3)
            for other_conn, other_addr in race_room:
                if other_addr != addr:
                    try:
                        loss_msg = f"\n\n{'='*40}\n"
                        loss_msg += f"GAME OVER!\n"
                        loss_msg += f"Nguoi choi {addr} da thang cuoc!\n"
                        loss_msg += f"{'='*40}\n"
                        other_conn.send(loss_msg.encode())
                        print(f"[RACE] Notified {other_addr} of loss", flush=True)
                    except Exception as e:
                        print(f"[RACE] Failed to notify {other_addr}: {e}", flush=True)
    
    # Clean up race room
    time.sleep(2)
    with race_lock:
        if (conn, addr) in race_room:
            race_room.remove((conn, addr))
        if len(race_room) == 0:
            game_active = False
            race_winner = None
            print("[RACE] Room cleaned up", flush=True)


def start_server():
    """
    Initialize and start the TCP server
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
    except OSError as e:
        print(f"Loi: Port {PORT} dang bi chiem. Hay thu doi PORT khac!")
        print(f"Chi tiet: {e}")
        return
    
    server.listen()
    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")
    print(f"Waiting for connections...")
    
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}", flush=True)
            
    except KeyboardInterrupt:
        print("\n[SERVER SHUTDOWN] Closing server...")
        server.close()


if __name__ == "__main__":
    start_server()