from piece import Piece

class Player:
    def __init__(self,player_id):
        self.player_id=player_id
        self.pieces=[Piece(player_id,i)for i in range(4)]
        self.home=False
    
    def has_won(self):
        return all(piece.position >=57 for piece in self.pieces ) #هي بداية منطقة 