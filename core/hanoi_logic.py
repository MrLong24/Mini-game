class HanoiGame:
    def __init__(self, disks=3):
        self.disks = disks
        self.towers = [list(range(disks, 0, -1)), [], []]
        self.moves_count = 0

    def move_disk(self, from_tower, to_tower):
        # 1. Validate đầu vào
        if from_tower not in [0, 1, 2] or to_tower not in [0, 1, 2]:
            return False, "Cot khong hop le (Chon 0, 1, 2)!"
        
        # 2. Kiểm tra cột đi
        if not self.towers[from_tower]:
            return False, "Cot di khong co dia!"
        
        disk_to_move = self.towers[from_tower][-1]

        # 3. Kiểm tra cột đến (Luật: Đĩa lớn không đè đĩa nhỏ)
        if self.towers[to_tower]:
            if disk_to_move > self.towers[to_tower][-1]:
                return False, "Loi: Dia lon khong duoc de len dia nho!"

        # 4. Thực hiện di chuyển
        self.towers[from_tower].pop()
        self.towers[to_tower].append(disk_to_move)
        self.moves_count += 1
        return True, "Di chuyen thanh cong"

    def is_won(self):
        # Thắng khi tất cả đĩa nằm ở cột cuối cùng (Cột 2)
        return len(self.towers[2]) == self.disks

    def render_str(self):
        # Vẽ tháp dạng chuỗi để gửi sang Client hiển thị
        res = "\n--- TRANG THAI THAP ---\n"
        # Tìm chiều cao lớn nhất để vẽ
        max_height = self.disks
        
        # Vẽ từng tầng từ trên xuống
        for i in range(max_height - 1, -1, -1):
            row = ""
            for t in range(3):
                if i < len(self.towers[t]):
                    disk_val = self.towers[t][i]
                    row += f"  [{disk_val}]  " 
                else:
                    row += "   |   " 
            res += row + "\n"
        
        res += "  COT 0    COT 1    COT 2  \n"
        res += "---------------------------\n"
        return res