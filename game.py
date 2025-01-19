from board import Board
from dice import Dice
from board_renderer import BoardRenderer

class Game:
    def __init__(self):
        self.board = Board(2)  # 2 لاعبين فقط
        self.dice = Dice()
        self.current_player = 0
        self.renderer = BoardRenderer(self.board)

    def start(self):
        print("The board before the game starts:")
        self.renderer.render()

    def play_turn(self):
        player = self.board.players[self.current_player]
        print(f"Player role {self.current_player + 1}")
        input("Press Enter to roll the dice....")
        roll = self.dice.roll()
        print(f"The number appeared: {roll}")

        # عرض القطع المتاحة للتحريك
        print("Available pieces for movement:")
        for i, piece in enumerate(player.pieces):
            if piece.position == -1 and roll == 6:
                print(f"{i + 1}: piece at the base")
            elif piece.position != -1:
                print(f"{i + 1}: piece in place {piece.position}")

        # اختيار قطعة للتحريك
        piece_id = int(input("Select the part number you want to move.: ")) - 1
        if 0 <= piece_id < 4:
            self.board.move_piece(self.current_player, piece_id, roll)

        # عرض الرقعة بعد الحركة
        self.renderer.render()

        # التحقق من الفوز
        if player.has_won():
            print(f"The player {self.current_player + 1} won!")
            return True

        # الانتقال إلى اللاعب التالي
        self.current_player = (self.current_player + 1) % 2
        return False