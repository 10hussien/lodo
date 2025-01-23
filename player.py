class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.pieces = [-1, -1, -1, -1] 
        self.finished_pieces = 0  

    def has_all_pieces_in_base(self):
        return all(piece == -1 for piece in self.pieces)

    def has_pieces_on_board(self):
        return any(piece != -1 for piece in self.pieces)

    def move_piece(self, piece_index, steps):
        if self.pieces[piece_index] == -1 and steps != 6:
            return False
        if self.pieces[piece_index] == -1:
            self.pieces[piece_index] = 0 
        else:
            self.pieces[piece_index] += steps
            if self.pieces[piece_index] > 56:
                self.pieces[piece_index] = 56
        return True

    def get_available_pieces(self, steps):
        available_pieces = []
        if steps == 6:
            for i in range(4):
                if self.pieces[i] == -1:
                    available_pieces.append(i)
        for i in range(4):
            if self.pieces[i] != -1 and self.pieces[i] + steps <= 56:
                available_pieces.append(i)
        return available_pieces

    def has_won(self):
        return all(piece == 56 for piece in self.pieces)