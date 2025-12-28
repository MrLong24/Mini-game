import pygame
import socket
import threading
import sys
import re
import time

# Configuration
SERVER_IP = '127.0.0.1'
PORT = 5555
WIDTH, HEIGHT = 900, 600

# Colors
BG_COLOR = (30, 30, 30)
TOWER_COLOR = (149, 165, 166)
DISK_COLORS = [
    (231, 76, 60), (230, 126, 34), (241, 196, 15),
    (46, 204, 113), (52, 152, 219), (155, 89, 182), (52, 73, 94)
]

class HanoiGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tower of Hanoi - Nhom 7")
        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 40)
        
        self.client = None
        self.towers = [[], [], []]
        self.num_disks = 3
        self.current_state = "MENU"  # MENU, SELECT_DISK, PLAYING, GAME_OVER
        self.selected_tower = None
        self.message = "Chao mung den voi game Thap Ha Noi!"
        self.running = True
        self.connected = False
        self.game_over = False
        
    def connect_to_server(self, mode, disks):
        """Connect to server and start game"""
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(10)
            self.client.connect((SERVER_IP, PORT))
            self.client.settimeout(None)
            self.connected = True
            
            # Send mode and disk count
            self.client.send(mode.encode())
            time.sleep(0.1)
            self.client.send(str(disks).encode())
            
            # Start receive thread
            threading.Thread(target=self.receive_data, daemon=True).start()
            self.current_state = "PLAYING"
            self.message = "Game bat dau!"
            
        except Exception as e:
            self.message = f"Loi ket noi: {e}"
            self.current_state = "MENU"
            print(f"[ERROR] Connection failed: {e}", flush=True)
    
    def receive_data(self):
        """Receive data from server in separate thread"""
        buffer = ""
        
        while self.running and self.connected:
            try:
                data = self.client.recv(4096).decode()
                if not data:
                    print("[RECV] Server closed connection", flush=True)
                    self.connected = False
                    break
                
                buffer += data
                
                # Process complete messages
                if "TRANG THAI THAP" in buffer:
                    self.parse_towers(buffer)
                    buffer = ""
                
                # Check for game over messages (BOTH SOLO AND RACE)
                if any(keyword in data for keyword in ["GAME OVER", "CHIEN THANG", "THANG CUOC", "CHUC MUNG", "GIAI XONG"]):
                    self.game_over = True
                    self.current_state = "GAME_OVER"
                    
                    if "BAN LA NGUOI CHIEN THANG" in data:
                        self.message = "★★★ BAN DA THANG! ★★★"
                    elif "CHUC MUNG" in data or "GIAI XONG" in data:
                        # Solo mode completion
                        # Extract time if available
                        import re
                        time_match = re.search(r'(\d+\.?\d*)\s*GIAY', data)
                        moves_match = re.search(r'(\d+)\s*nuoc', data)
                        
                        msg = "★★★ HOAN THANH! ★★★"
                        if time_match:
                            msg += f"\nThoi gian: {time_match.group(1)}s"
                        if moves_match:
                            msg += f"\nSo nuoc: {moves_match.group(1)}"
                        
                        self.message = msg
                    elif "da thang cuoc" in data or "THUA" in data.upper():
                        self.message = "Ban da thua! Doi thu thang cuoc!"
                    
                    print(f"[GAME OVER] {self.message}", flush=True)
                
                # Update message for user feedback
                if ">>>" in data:
                    lines = data.split('\n')
                    for line in lines:
                        if ">>>" in line:
                            feedback = line.replace(">>>", "").strip()
                            if feedback and not self.game_over:
                                self.message = feedback
                                
            except ConnectionAbortedError:
                print("[RECV] Connection aborted by server", flush=True)
                self.connected = False
                if not self.game_over:
                    self.message = "Ket noi bi ngat!"
                    self.current_state = "GAME_OVER"
                break
            except ConnectionResetError:
                print("[RECV] Connection reset", flush=True)
                self.connected = False
                if not self.game_over:
                    self.message = "Mat ket noi voi server!"
                    self.current_state = "GAME_OVER"
                break
            except Exception as e:
                print(f"[RECV ERROR] {e}", flush=True)
                break
    
    def parse_towers(self, data):
        """Parse tower state from server data"""
        new_towers = [[], [], []]
        lines = data.split('\n')
        
        tower_lines = []
        for line in lines:
            if any(skip in line for skip in ["TRANG THAI", "COT", "---", ">>>"]):
                continue
            if "|" in line or "[" in line:
                tower_lines.append(line)
        
        for line in tower_lines:
            if not line.strip():
                continue
            
            width = len(line)
            col_width = width // 3
            
            columns = [
                line[0:col_width],
                line[col_width:2*col_width],
                line[2*col_width:]
            ]
            
            for col_idx, col_text in enumerate(columns):
                matches = re.findall(r'\[(\d+)\]', col_text)
                if matches:
                    disk_num = int(matches[0])
                    new_towers[col_idx].append(disk_num)
        
        # Reverse towers (we read top to bottom)
        for i in range(3):
            new_towers[i] = new_towers[i][::-1]
        
        if any(new_towers):
            self.towers = new_towers
    
    def send_move(self, from_tower, to_tower):
        """Send move to server with error handling"""
        if not self.connected or self.game_over:
            return
        
        try:
            move = f"{from_tower} {to_tower}"
            self.client.send(move.encode())
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            print("[SEND] Connection lost while sending move", flush=True)
            self.connected = False
            self.game_over = True
            self.current_state = "GAME_OVER"
            self.message = "Mat ket noi voi server!"
        except Exception as e:
            print(f"[SEND ERROR] {e}", flush=True)
    
    def draw_menu(self):
        """Draw main menu"""
        self.screen.fill(BG_COLOR)
        title = self.big_font.render("TOWER OF HANOI", True, (0, 255, 255))
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        
        self.btn_solo = self.draw_button("1. CHE DO DOC LAP", 300, 220, 300, 50, (46, 204, 113))
        self.btn_race = self.draw_button("2. CHE DO THI DAU", 300, 300, 300, 50, (231, 76, 60))
        self.btn_exit = self.draw_button("3. THOAT GAME", 300, 380, 300, 50, (149, 165, 166))
    
    def draw_select_disk(self):
        """Draw disk selection screen"""
        self.screen.fill(BG_COLOR)
        txt = self.font.render("CHON SO TANG (3 - 7):", True, (255, 255, 255))
        self.screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 150))
        
        self.disk_btns = {}
        for i in range(3, 8):
            self.disk_btns[i] = self.draw_button(str(i), 120 + (i-3)*140, 250, 80, 80, (52, 152, 219))
    
    def draw_button(self, text, x, y, w, h, color):
        """Draw a button and return its rect"""
        pygame.draw.rect(self.screen, color, (x, y, w, h), border_radius=8)
        txt_surf = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(txt_surf, (x + (w - txt_surf.get_width())//2, y + (h - txt_surf.get_height())//2))
        return pygame.Rect(x, y, w, h)
    
    def draw_playing(self):
        """Draw game board"""
        self.screen.fill(BG_COLOR)
        tower_x = [225, 450, 675]
        base_y = 450
        
        # Draw towers
        for x in tower_x:
            pygame.draw.rect(self.screen, TOWER_COLOR, (x - 10, 200, 20, 250))
            pygame.draw.rect(self.screen, TOWER_COLOR, (x - 100, base_y, 200, 20))
        
        # Draw disks
        for t_idx, tower in enumerate(self.towers):
            for d_idx, disk_val in enumerate(tower):
                disk_width = 40 + (disk_val * 20)
                disk_height = 25
                
                disk_x = tower_x[t_idx] - disk_width // 2
                disk_y = base_y - (d_idx + 1) * (disk_height + 2)
                
                color = DISK_COLORS[disk_val % len(DISK_COLORS)]
                pygame.draw.rect(self.screen, color, (disk_x, disk_y, disk_width, disk_height), border_radius=5)
                
                val_txt = self.font.render(str(disk_val), True, (255, 255, 255))
                self.screen.blit(val_txt, (disk_x + disk_width//2 - 5, disk_y + 2))
        
        # Draw message
        msg_surf = self.font.render(self.message, True, (255, 255, 255))
        self.screen.blit(msg_surf, (20, 20))
        
        # Draw selected tower indicator
        if self.selected_tower is not None:
            pygame.draw.circle(self.screen, (255, 255, 0), (tower_x[self.selected_tower], 480), 10)
    
    def draw_game_over(self):
        """Draw game over screen"""
        self.screen.fill(BG_COLOR)
        
        # Display final board
        self.draw_playing()
        
        # Overlay game over message
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Message
        msg_surf = self.big_font.render(self.message, True, (255, 255, 0))
        self.screen.blit(msg_surf, (WIDTH//2 - msg_surf.get_width()//2, HEIGHT//2 - 50))
        
        # Back to menu button
        self.btn_menu = self.draw_button("TRO VE MENU", 300, 400, 300, 50, (52, 152, 219))
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_state == "MENU":
                        if self.btn_solo.collidepoint(mouse_pos):
                            self.mode = "1"
                            self.current_state = "SELECT_DISK"
                        elif self.btn_race.collidepoint(mouse_pos):
                            self.mode = "2"
                            self.current_state = "SELECT_DISK"
                        elif self.btn_exit.collidepoint(mouse_pos):
                            self.running = False
                    
                    elif self.current_state == "SELECT_DISK":
                        for val, rect in self.disk_btns.items():
                            if rect.collidepoint(mouse_pos):
                                self.num_disks = val
                                self.connect_to_server(self.mode, val)
                    
                    elif self.current_state == "PLAYING":
                        if self.game_over:
                            continue
                        
                        x, y = mouse_pos
                        col = -1
                        if 125 < x < 325: col = 0
                        elif 350 < x < 550: col = 1
                        elif 575 < x < 775: col = 2
                        
                        if col != -1:
                            if self.selected_tower is None:
                                self.selected_tower = col
                                self.message = f"Da chon cot {col}. Chon cot dich..."
                            else:
                                self.send_move(self.selected_tower, col)
                                self.selected_tower = None
                    
                    elif self.current_state == "GAME_OVER":
                        if hasattr(self, 'btn_menu') and self.btn_menu.collidepoint(mouse_pos):
                            # Reset game
                            if self.client:
                                try:
                                    self.client.close()
                                except:
                                    pass
                            self.client = None
                            self.connected = False
                            self.game_over = False
                            self.towers = [[], [], []]
                            self.selected_tower = None
                            self.current_state = "MENU"
                            self.message = "Chao mung den voi game Thap Ha Noi!"
            
            # Draw appropriate screen
            if self.current_state == "MENU":
                self.draw_menu()
            elif self.current_state == "SELECT_DISK":
                self.draw_select_disk()
            elif self.current_state == "PLAYING":
                self.draw_playing()
            elif self.current_state == "GAME_OVER":
                self.draw_game_over()
            
            pygame.display.flip()
            clock.tick(30)
        
        # Cleanup
        if self.client:
            try:
                self.client.close()
            except:
                pass
        pygame.quit()

if __name__ == "__main__":
    game = HanoiGUI()
    game.run()