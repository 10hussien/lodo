import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from lodo_rulse import Rules
from player import Player 

# تعريف الألوان المستخدمة في اللعبة
COLORS = ["white", "red", "green", "yellow", "blue", "black", 'gray']

# حجم اللوحة
BOARD_SIZE = 800  # حجم اللوحة (يمكن تعديله)
CELL_SIZE = BOARD_SIZE // 16  # حجم الخلية

# مصفوفة الألوان
colorMatrix = [
    [2, 2, 2, 2, 2, 2, 0, 0, 0, 4, 4, 4, 4, 4, 4],
    [2, 0, 2, 2, 0, 2, 6, 4, 4, 4, 0, 4, 4, 0, 4],
    [2, 2, 2, 2, 2, 2, 0, 4, 0, 4, 4, 4, 4, 4, 4],
    [2, 2, 2, 2, 2, 2, 0, 4, 0, 4, 4, 4, 4, 4, 4],
    [2, 0, 2, 2, 0, 2, 0, 4, 0, 4, 0, 4 , 4, 0, 4],
    [2, 2, 2, 2, 2, 2, 0, 4, 0, 4, 4, 4, 4, 4, 4],
    [0, 2, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 6, 0],
    [0, 2, 2, 2, 2, 2, 6, 5 , 6, 3, 3, 3, 3,3, 0],
    [0, 6, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 6, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 3, 3, 3, 3, 3, 3],
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 3, 0, 3, 3, 0, 3],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 3, 3, 3, 3, 3, 3],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 3, 3, 3, 3, 3, 3],
    [1, 0, 1, 1, 0, 1, 1, 1, 3, 3, 0, 3, 3, 0, 3],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 3, 3, 3, 3, 3, 3]
]

# مسار اللاعب الأول (الأحمر)
player1_path= [
    (6,13),(6,12),(6,11),(6,10),(6,9),
    (5,8),(4,8),(3,8),(2,8),(1,8),(0,8),
    (0,7),(0,6),
    (1,6),(2,6),(3,6),(4,6),(5,6),
    (6,5),(6,4),(6,3),(6,2),(6,1),(6,0),
    (7,0),(8,0),
    (8,1),(8,2),(8,3),(8,4),(8,5),
    (9,6),(10,6),(11,6),(12,6),(13,6),(14,6),
    (14,7),(14,8),
    (13,8),(12,8),(11,8),(10,8),(9,8),
    (8,9),(8,10),(8,11),(8,12),(8,13),(8,14),
    (7,14),(7,13),(7,12),(7,11),(7,10),(7,9),(7,8)
]

player2_path = [
    (8,1),(8,2),(8,3),(8,4),(8,5),
    (9,6),(10,6),(11,6),(12,6),(13,6),(14,6),
    (14,7),(14,8),
    (13,8),(12,8),(11,8),(10,8),(9,8),
    (8,9),(8,10),(8,11),(8,12),(8,13),(8,14),
    (7,14),(6,14),
    (6,13),(6,12),(6,11),(6,10),(6,9),
    (5,8),(4,8),(3,8),(2,8),(1,8),(0,8),
    (0,7),(0,6),
    (1,6),(2,6),(3,6),(4,6),(5,6),
    (6,5),(6,4),(6,3),(6,2),(6,1),(6,0),
    (7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6)
]

class LudoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("لعبة لودو")
        self.canvas = tk.Canvas(root, width=BOARD_SIZE, height=BOARD_SIZE, bg="bisque")
        self.canvas.pack()

        # إنشاء كائن من فئة Rules
        self.rules = Rules()

        # تعريف اللاعبين ككائنات من فئة Player
        self.players = [
            Player("Player 1", "red"),
            Player("Player 2", "blue")
        ]

        self.base_positions = {
            "blue": [(10, 1), (10, 4), (13, 1), (13, 4)],  # مواقع القطع الحمراء
            "red": [(1, 10), (1, 13), (4, 10), (4, 13)]  # مواقع القطع الزرقاء
        }

        # اختيار لاعب عشوائي لبدء اللعبة
        self.current_player_index = random.randint(0, 1)

        # رسم اللوحة
        self.draw_board()

        # بدء اللعبة
        self.play_turn()
    
    
    def roll_dice(self):
        """رمي النرد باستخدام الدالة من rules.py."""
        return self.rules.roll_dice()
    
    def draw_base_pieces(self):
        """رسم القطع الموجودة في القاعدة لكل لاعب."""
        for player in self.players:
            color = player.color
            positions = self.base_positions[color]  # الحصول على المواقع المخصصة للاعب
            pieces_in_base = player.pieces.count(-1)  # عدد القطع في القاعدة

            for i in range(4):  # لكل موقع من المواقع الأربعة
                x, y = positions[i]
                if i < pieces_in_base:
                    # إذا كانت القطعة موجودة في القاعدة، نرسمها
                    self.canvas.create_oval(
                        x * CELL_SIZE + 10, y * CELL_SIZE + 10,
                        (x + 1) * CELL_SIZE - 10, (y + 1) * CELL_SIZE - 10,
                        fill="white", outline="black", width=2
                    )
                    self.canvas.create_oval(
                        x * CELL_SIZE + 15, y * CELL_SIZE + 15,
                        (x + 1) * CELL_SIZE - 15, (y + 1) * CELL_SIZE - 15,
                        fill=color, outline="black", width=1
                    )
                else:
                    # إذا كانت القطعة غير موجودة في القاعدة، نترك المكان فارغًا
                    self.canvas.create_rectangle(
                        x * CELL_SIZE, y * CELL_SIZE,
                        (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                        fill="bisque", outline="black"
                    )

    def draw_board(self):
        """رسم اللوحة بالكامل باستخدام colorMatrix."""
        # مسح اللوحة الحالية
        self.canvas.delete("all")

        # رسم الخلايا بناءً على colorMatrix
        for i in range(15):
            for j in range(15):
                x1, y1 = i * CELL_SIZE, j * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = COLORS[colorMatrix[j][i]]  # استخدام colorMatrix لتحديد لون الخلية
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                #رسم القطع الموجودة في القاعدة
        self.draw_base_pieces()
        # رسم القطع بناءً على مواقعها الحالية
        self.draw_pieces()
        

    def draw_pieces(self):
        """رسم القطع بناءً على مواقعها الحالية."""
        for player_index, player in enumerate(self.players):
            for piece_index, position in enumerate(player.pieces):
                if position != -1:  # إذا كانت القطعة على اللوحة
                    x, y = self.get_position_coordinates(player_index, position)
                    self.canvas.create_oval(
                        x * CELL_SIZE + 10, y * CELL_SIZE + 10,
                        (x + 1) * CELL_SIZE - 10, (y + 1) * CELL_SIZE - 10,
                        fill=player.color, outline="black", width=2
                    )

    def get_position_coordinates(self, player_index, position):
        """تحويل الموقع (من 0 إلى 56) إلى إحداثيات (x, y) على اللوحة بناءً على مسار اللاعب."""
        if player_index == 0:  # اللاعب الأول (الأحمر)
            if position < len(player1_path):
                return player1_path[position]
        elif player_index == 1:  # اللاعب الثاني (الأزرق)
            if position < len(player2_path):
                return player2_path[position]
        return (0, 0)  # حالة افتراضية (لا ينبغي الوصول إليها)

    def get_available_pieces(self, player, steps):
        """إرجاع قائمة بالقطع التي يمكن تحريكها بناءً على نتيجة النرد."""
        available_pieces = []
        if steps == 6:
            # إذا كان النرد 6، يمكن تحريك القطع من القاعدة
            for i in range(4):
                if player.pieces[i] == -1:
                    available_pieces.append(i)
        # يمكن تحريك القطع الموجودة على اللوحة
        for i in range(4):
            if player.pieces[i] != -1 and player.pieces[i] + steps <= 56:
                available_pieces.append(i)
        return available_pieces

    def move_piece(self, player, piece_index, steps):
        """تحريك قطعة معينة بعدد معين من الخطوات."""
        if player.pieces[piece_index] == -1 and steps != 6:
            return False  # لا يمكن تحريك القطعة من القاعدة إلا برقم 6
        if player.pieces[piece_index] == -1:
            player.pieces[piece_index] = 0  # نقل القطعة من القاعدة إلى نقطة البداية
        else:
            new_position = player.pieces[piece_index] + steps
            if new_position > 56:  # إذا تجاوزت القطعة النهاية
                new_position = 56

            # # التحقق من الشروط باستخدام فئة Rules
            # if self.rules.is_safe_spot(new_position):
            #     messagebox.showinfo("خانة آمنة", "هذه الخانة آمنة!")
            # if self.rules.is_wall(self.players, new_position):
            #     messagebox.showinfo("جدار", "هناك جدار هنا!")
            # if self.should_return_piece(new_position):
            #     messagebox.showinfo("إعادة القطعة", "يجب إعادة القطعة إلى القاعدة!")

            player.pieces[piece_index] = new_position

            # التحقق من إرسال قطعة اللاعب الآخر إلى القاعدة
            self.rules.check_and_displace_piece(self.players, player, new_position)

        # تحديث الواجهة الرسومية بعد تحريك القطعة
        self.update_board()
        return True


    def should_return_piece(self, position):
        """تحقق إذا كان يجب إعادة القطعة إلى القاعدة."""
        return self.rules.should_return_piece(self.players, position)

    def update_board(self):
        """تحديث اللوحة بناءً على مواقع القطع الحالية."""
        self.draw_board()   # إعادة رسم اللوحة بالكامل

    def play_turn(self):
        """لعب دور اللاعب الحالي."""
        current_player = self.players[self.current_player_index]

        # رمي النرد بشكل متكرر إذا كانت النتيجة 6
        dice_results = []
        while True:
            dice_roll = self.roll_dice()
            dice_results.append(dice_roll)
            messagebox.showinfo("current player :", f"{current_player.name} \n {dice_roll}")
            if dice_roll != 6:
                break  # التوقف إذا لم تكن النتيجة 6
            
        # التحقق من وجود قطع قابلة للتحريك لأي من نتائج النرد
        has_available_pieces = any(current_player.get_available_pieces(dice) for dice in dice_results)

        if not has_available_pieces:
            messagebox.showinfo("لا يمكن التحريك", f"{current_player.name} لا يمكنه تحريك أي قطعة.")
            self.switch_player()  # الانتقال إلى اللاعب التالي
            self.play_turn()  # استدعاء اللعبة مرة أخرى للاعب التالي
            return  # إنهاء الدور الحالي

        # السماح للاعب بتحريك قطع بناءً على عدد نتائج النرد
        for dice_roll in dice_results:
            # الحصول على القطع المتاحة للتحريك بناءً على النتيجة الحالية
            available_pieces = current_player.get_available_pieces(dice_roll)
            if not available_pieces:
                messagebox.showinfo("لا يمكن التحريك", f"{current_player.name} لا يمكنه تحريك أي قطعة للنرد: {dice_roll}.")
                continue  # الانتقال إلى النتيجة التالية

            # عرض القطع المتاحة للتحريك بشكل أكثر وضوحًا
            piece_info = "القطع المتاحة للتحريك:\n"
            for piece_index in available_pieces:
                if current_player.pieces[piece_index] == -1:
                    piece_info += f"{piece_index}: القطعة في القاعدة\n"
                else:
                    new_position = current_player.pieces[piece_index] + dice_roll
                    if new_position > 56:
                        new_position = 56
                    piece_info += f"{piece_index}: القطعة في الموقع {current_player.pieces[piece_index]}\n"

            # عرض القطع المتاحة للتحريك في نافذة منبثقة
            piece_index = simpledialog.askinteger("اختيار قطعة", f"النرد: {dice_roll}\n{piece_info}\nاختر قطعة للتحريك (0-3):")
            if piece_index is not None and piece_index in available_pieces:
                self.move_piece(current_player, piece_index, dice_roll)
                if self.check_win(current_player):
                    messagebox.showinfo("الفوز", f"{current_player.name} فاز باللعبة!")
                    return
            else:
                messagebox.showwarning("خطأ", "اختيار غير صحيح. حاول مرة أخرى.")

        # إذا كانت آخر نتيجة نرد 6، يلعب اللاعب مرة أخرى
        if dice_results[-1] == 6:
            self.play_turn()
        else:
            self.switch_player()  # الانتقال إلى اللاعب التالي
            self.play_turn()  # استدعاء اللعبة مرة أخرى للاعب التالي # استدعاء اللعبة مرة أخرى للاعب التالي  # استدعاء اللعبة مرة أخرى للاعب التالي # استدعاء اللعبة مرة أخرى للاعب التالي

    def switch_player(self):
        """تبديل الأدوار بين اللاعبين."""
        self.current_player_index = 1 - self.current_player_index

    def check_win(self, player):
        """تحقق إذا فاز اللاعب (وصلت جميع القطع إلى النهاية)."""
        return all(piece == 56 for piece in player.pieces)

if __name__ == "__main__":
    root = tk.Tk()
    game = LudoGame(root)
    root.mainloop()