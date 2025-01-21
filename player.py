class Player:
    def __init__(self, name, color, start_position=0):
        self.name = name
        self.color = color
        self.pieces = [-1, -1, -1, -1]  # -1 يعني القطعة في القاعدة
        self.finished_pieces = 0  # عدد القطع التي وصلت للنهاية
        self.start_position = start_position  # نقطة البداية الخاصة باللاعب

    def has_all_pieces_in_base(self):
        """تحقق إذا كانت كل القطع في القاعدة."""
        return all(piece == -1 for piece in self.pieces)

    def has_pieces_on_board(self):
        """تحقق إذا كان هناك قطع على لوحة اللعب."""
        return any(piece != -1 for piece in self.pieces)

    def move_piece(self, piece_index, steps):
        """تحريك قطعة معينة بعدد معين من الخطوات."""
        if self.pieces[piece_index] == -1 and steps != 6:
            return False  # لا يمكن تحريك القطعة من القاعدة إلا برقم 6
        if self.pieces[piece_index] == -1:
            self.pieces[piece_index] = self.start_position  # نقل القطعة من القاعدة إلى نقطة البداية الخاصة باللاعب
        else:
            self.pieces[piece_index] += steps
            if self.pieces[piece_index] > 56:  # إذا تجاوزت القطعة النهاية
                self.pieces[piece_index] = 56
        return True

    def get_available_pieces(self, steps):
        """إرجاع قائمة بالقطع التي يمكن تحريكها بناءً على نتيجة النرد."""
        available_pieces = []
        if steps == 6:
            # إذا كان النرد 6، يمكن تحريك القطع من القاعدة
            for i in range(4):
                if self.pieces[i] == -1:
                    available_pieces.append(i)
        # يمكن تحريك القطع الموجودة على اللوحة
        for i in range(4):
            if self.pieces[i] != -1 and self.pieces[i] + steps <= 56:
                available_pieces.append(i)
        return available_pieces

    def has_won(self):
        """تحقق إذا فاز اللاعب (وصلت جميع القطع إلى النهاية)."""
        return all(piece == 56 for piece in self.pieces)