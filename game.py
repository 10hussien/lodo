import random
from board import Board
from ai_player import AIPlayer

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.board = Board()
        self.current_player_index = random.randint(0, 1)  # اختيار لاعب عشوائي لبدء اللعبة
        self.last_board_state = None  # تتبع آخر حالة للوحة

    def roll_dice(self):
        """رمي النرد."""
        input("Press Enter to roll the dice...")
        return random.randint(1, 6)

    def switch_player(self):
        """تبديل الأدوار بين اللاعبين."""
        self.current_player_index = 1 - self.current_player_index

    def should_return_piece(self, players, position):
        """تحقق إذا كان يجب إعادة القطعة إلى القاعدة."""
        if (self.board.is_safe_spot(position) or
            position == 0 or
            51 <= position <= 55):
            return False
        if self.board.is_wall(players, position):
            return False
        return True

    def play_turn(self):
        """لعب دور اللاعب الحالي."""
        current_player = self.players[self.current_player_index]
        print(f"\n{current_player.name}'s turn ({current_player.color})")

        # رمي النرد وتخزين النتائج
        dice_results = []
        while True:
            dice_roll = self.roll_dice()
            print(f"Dice roll: {dice_roll}")
            dice_results.append(dice_roll)
            if dice_roll != 6:
                break  # التوقف إذا لم تكن النتيجة 6

        # عرض جميع نتائج النرد
        print(f"All dice results: {dice_results}")

        # التحرك بناءً على كل نتيجة نرد
        for dice_roll in dice_results:
            print(f"\nUsing dice result: {dice_roll}")

            # الحصول على القطع المتاحة للتحريك
            available_pieces = current_player.get_available_pieces(dice_roll)
            if not available_pieces:
                print(f"{current_player.name} cannot move any pieces with this dice roll.")
                continue  # التخطي إذا لم تكن هناك قطع متاحة

            # عرض القطع المتاحة للتحريك بشكل أكثر وضوحًا
            print("Available pieces to move:")
            for piece_index in available_pieces:
                if current_player.pieces[piece_index] == -1:
                    print(f"{piece_index}: Piece in the base")
                else:
                    new_position = current_player.pieces[piece_index] + dice_roll
                    if new_position > 56:
                        new_position = 56
                    print(f"{piece_index}: Piece at position {current_player.pieces[piece_index]}")

            # اختيار قطعة للتحريك
            if isinstance(current_player, AIPlayer):
                piece_index = current_player.choose_piece(dice_roll, self.board)  # تمرير اللوحة هنا
            else:
                while True:
                    try:
                        piece_index = int(input("Choose a piece to move (enter the number): "))
                        if piece_index not in available_pieces:
                            print("Invalid choice. You cannot move this piece. Try again.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. You must enter a number. Try again.")

            # تحريك القطعة
            if current_player.move_piece(piece_index, dice_roll):
                new_position = current_player.pieces[piece_index]
                print(f"{current_player.name} moved piece {piece_index} to position {new_position}.")

                # التحقق من إرسال قطعة اللاعب الآخر إلى القاعدة
                for player in self.players:
                    if player != current_player:
                        for i, pos in enumerate(player.pieces):
                            if pos != -1 and abs(new_position - pos) == 26:  # الفرق بين المواقع يساوي 26
                                if not self.board.is_safe_spot(pos):  # القطعة ليست في خانة آمنة
                                    if not self.board.is_wall(self.players, pos):  # لا يوجد جدار في الموقع
                                        player.pieces[i] = -1  # إرسال القطعة إلى القاعدة
                                        print(f"{current_player.name} displaced {player.name}'s piece!")
            else:
                print("Invalid move. You cannot move this piece. Try again.")

        # تبديل اللاعب إذا لم تكن آخر نتيجة نرد 6
        if dice_results[-1] != 6:
            self.switch_player()

    def check_win(self):
        """تحقق إذا فاز لاعب."""
        for player in self.players:
            if player.has_won():
                return player
        return None

    def play_game(self):
        """بدء اللعبة."""
        print("Starting Ludo Game!")
        self.board.print_board(self.players)
        self.last_board_state = self.board.get_board_state(self.players)  # تهيئة آخر حالة للوحة
        winner = None
        while not winner:
            self.play_turn()
            # التحقق من تغيير حالة اللوحة
            current_board_state = self.board.get_board_state(self.players)
            if current_board_state != self.last_board_state:
                self.board.print_board(self.players)
                self.last_board_state = current_board_state  # تحديث آخر حالة للوحة
            winner = self.check_win()
        print(f"{winner.name} ({winner.color}) has won the game!")