import random
class Rules:
    def __init__(self):
        self.safe_spots = {0, 8, 13, 21, 26, 34, 39, 47}  # الخانات الامنة باللعبة
        self.path_length = 56  # طول المسار بالنسبة للاعب 56 هي الحالة النهائية 

    def roll_dice(self):
        return random.randint(1, 6)
    
    def is_safe_spot(self, position):
        return position in self.safe_spots

    def is_wall(self, players, position):
        for player in players:
            count = player.pieces.count(position)
            if count >= 2:
                return True
        return False

    def should_return_piece(self, players, position):
        if (self.is_safe_spot(position) or
            position == 0 or
            51 <= position <= 55):
            return False
        if self.is_wall(players, position):
            return False
        return True

    def get_pieces_at_position(self, players, position):
        pieces = []
        for player in players:
            for i, pos in enumerate(player.pieces):
                if pos == position:
                    pieces.append((i, player.color))
        return pieces

    def get_board_state(self, players):
        board_state = {}
        for player in players:
            board_state[player.name] = player.pieces.copy()
        return board_state
    
    def check_and_displace_piece(self, players, current_player, new_position):
        #هذا التابع يلي بياخذ كل الشروط مع بعضن وبفحصن لحتى يقرر اذا فينو يرسل قطعة للقاعدة او لا 
        for player in players:
            if player != current_player:
                for i, pos in enumerate(player.pieces):
                    if pos != -1 and abs(new_position - pos) == 26:  # هي الحركة يلي اتفقنا عليها انو والله اذا عملنا اللعبة على اشارة + فالفرق بين اللاعبين 26 خانة 
                        if not self.is_safe_spot(pos):  
                            if not self.is_wall(players, pos): 
                                player.pieces[i] = -1  
                                print(f"{current_player.name} displaced {player.name}'s piece!")
                                return True 
        return False  