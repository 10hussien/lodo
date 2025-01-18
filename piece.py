class Piece:
    def __init__(self, player_id, piece_id):
        self.player_id = player_id
        self.piece_id = piece_id
        self.position = -1  # -1 يعني أن القطعة في القاعدة

    def move(self, steps):
        self.position += steps

    def reset(self):
        self.position = -1