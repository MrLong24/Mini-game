class HanoiGame:
    def __init__(self, disks=3):
        self.disks = disks
        self.towers = [list(range(disks, 0, -1)), [], []]

    def move_disk(self, from_tower, to_tower):
        # Kiểm tra logic: tháp trống, đĩa lớn đè đĩa nhỏ...
        # Trả về True nếu đi đúng, False nếu sai
        pass

    def is_won(self):
        return len(self.towers[2]) == self.disks