from player import Player

class Board:
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = [Player(i) for i in range(num_players)]
        self.safe_spots = [0, 8, 13, 21, 26, 34, 39, 47]  # الخانات الآمنة

    def is_safe_spot(self, position):
        return position in self.safe_spots

    def move_piece(self, player_id, piece_id, steps):
        player = self.players[player_id]
        piece = player.pieces[piece_id]

        if piece.position == -1 and steps == 6:
            piece.position = 0  # بدء اللعب
        elif piece.position != -1:
            new_position = piece.position + steps
            if new_position > 57:
                new_position = 57 - (new_position - 57)  # تجاوز منطقة التباية
            piece.position = new_position

        # التحقق من الفوز
        if player.has_won():
            print(f"Player {player_id} has won!")