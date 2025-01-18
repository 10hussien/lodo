from board import Board
from dice import Dice

class Game:
    def __init__(self, num_players):
        self.board = Board(num_players)
        self.dice = Dice()
        self.current_player = 0

    def next_turn(self):
        player = self.board.players[self.current_player]
        print(f"Player {self.current_player}'s turn")
        roll = self.dice.roll()
        print(f"Rolled a {roll}")

        # اختيار قطعة للتحريك
        for piece_id, piece in enumerate(player.pieces):
            if piece.position != -1 or roll == 6:
                self.board.move_piece(self.current_player, piece_id, roll)
                break

        # التحقق من الفوز
        if player.has_won():
            print(f"Player {self.current_player} has won!")
            return True

        # الانتقال إلى اللاعب التالي
        self.current_player = (self.current_player + 1) % self.board.num_players
        return False