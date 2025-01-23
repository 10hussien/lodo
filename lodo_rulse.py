import random
class Rules:
    def __init__(self):
        self.safe_spots = {0, 8, 13, 21, 26, 34, 39, 47}  # الخانات الآمنة
        self.path_length = 56  # طول المسار من البداية إلى النهاية

    def roll_dice(self):
        """رمي النرد وإرجاع نتيجة عشوائية بين 1 و6."""
        return random.randint(1, 6)
    
    def is_safe_spot(self, position):
        """تحقق إذا كانت الخانة آمنة."""
        return position in self.safe_spots

    def is_wall(self, players, position):
        """تحقق إذا كان هناك جدار في الخانة (قطعتان أو أكثر من نفس اللاعب)."""
        for player in players:
            count = player.pieces.count(position)
            if count >= 2:
                return True
        return False

    def should_return_piece(self, players, position):
        """تحقق إذا كان يجب إعادة القطعة إلى القاعدة."""
        if (self.is_safe_spot(position) or
            position == 0 or
            51 <= position <= 55):
            return False
        if self.is_wall(players, position):
            return False
        return True

    def get_pieces_at_position(self, players, position):
        """احصل على القطع في موقع معين مع ألوانها."""
        pieces = []
        for player in players:
            for i, pos in enumerate(player.pieces):
                if pos == position:
                    pieces.append((i, player.color))
        return pieces

    def get_board_state(self, players):
        """احصل على حالة اللوحة الحالية (مواقع جميع قطع اللاعبين)."""
        board_state = {}
        for player in players:
            board_state[player.name] = player.pieces.copy()
        return board_state
    
    def check_and_displace_piece(self, players, current_player, new_position):
        """
        تحقق من الشروط وإرسال قطعة اللاعب الآخر إلى القاعدة إذا تم استيفاء الشروط.
        """
        for player in players:
            if player != current_player:
                for i, pos in enumerate(player.pieces):
                    if pos != -1 and abs(new_position - pos) == 26:  # الفرق بين المواقع يساوي 26
                        if not self.is_safe_spot(pos):  # القطعة ليست في خانة آمنة
                            if not self.is_wall(players, pos):  # لا يوجد جدار في الموقع
                                player.pieces[i] = -1  # إرسال القطعة إلى القاعدة
                                print(f"{current_player.name} displaced {player.name}'s piece!")
                                return True  # تم إرسال قطعة
        return False  