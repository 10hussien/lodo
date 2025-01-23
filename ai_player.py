from player import Player
from board import Board

class AIPlayer(Player):
    def __init__(self, name, color, board, depth=3, verbose=False):
        super().__init__(name, color)
        self.board = board
        self.depth = depth
        self.verbose = verbose
        self.nodes_visited = 0

    def expectiminimax(self, board, players, current_player_index, depth, is_maximizing_player, dice_roll):
        self.nodes_visited += 1

        if depth == 0 or self.has_won() or players[1 - current_player_index].has_won():
            value = self.heuristic(board, players)
            if self.verbose:
                #هي الخطورة هي لعرض تفاصيل الخوارزمية 
                print(f"Node: Depth={depth}, Value={value}, Player={players[current_player_index].name}, Dice={dice_roll}")
            return value

        current_player = players[current_player_index]
        if is_maximizing_player:
            value = -float('inf')
            for piece_index in current_player.get_available_pieces(dice_roll):
                new_position = current_player.pieces[piece_index] + dice_roll
                if new_position > 56:
                    new_position = 56
                original_position = current_player.pieces[piece_index]
                current_player.pieces[piece_index] = new_position
                child_value = self.expectiminimax(board, players, current_player_index, depth - 1, False, dice_roll)
                current_player.pieces[piece_index] = original_position 
                value = max(value, child_value)
            return value
        else:
            value = 0
            for dice in range(1, 7):  # رح يعطيني كل قيم النرد الخاص  1-6
                probability = 1 / 6  # هون باخذ احتمالية كل نتيحة 
                child_value = self.expectiminimax(board, players, 1 - current_player_index, depth - 1, True, dice)
                value += probability * child_value
            return value

    def heuristic(self, board, players):
        current_player = self
        opponent = players[1 - players.index(current_player)]
        score = 0
        #هون رح رقملكن الشروط يلي على اساسها رح نمشي على بهذا التابع 
        
        # 1. اذا وصلت للنهاية بزيدلي المحصلة بمقدار 30 
        score += current_player.finished_pieces * 30

        # 2. هون بشوف الخصم اذا قطعة وصلت للنهاية بنقصلي من محصلتي 30 
        score -= opponent.finished_pieces * 30

        # 3. هون بفحص القطع يلي على اللوحة وبزيد حسب وين هي طبعا بس تكون اقرب للنهاية فهي اكبر زيادة للعدد
        for piece in current_player.pieces:
            if piece != -1:
                score += piece 

        # 4. هون عندي اذا القطع تبعي موجودين بخانة  امنة من هلخانات تبعاتي
        for piece in current_player.pieces:
            if piece != -1 and board.is_safe_spot(piece):
                score += 20

        # 5. هون بشوف القطع اذا كانت موقعن باخر خمس خطوات اي الاماكن الخاصة فيني انا لوصل للهدف وبزيد للمحصلة عكل قطعة مموجودة الي هينك
        for piece in current_player.pieces:
            if piece != -1 and piece >= 50:
                score += 25

        # 6. هون اذا كان فيني اقتل اي قطعة للخصم وارسلها للقاعدة فهي الها هدف اكبر من انو وصل للهدف لانو هيك بتكبر احتمالية فوزي 
        for piece in current_player.pieces:
            if piece != -1:
                for opponent_piece in opponent.pieces:
                    if opponent_piece == piece and not board.is_safe_spot(piece):
                        score += 40  # زيادة كبيرة إذا قتلت قطعة الخصم

        # 7. هون اخر شرط هو حالة الخطر علقطعة تبعي يعني اذا القطعة بتعبد عن قطعةة الخصم ممقدار بين 1-6 فهي عليها خطر اكبر من مقدار فوق 7 مثلا وهيك 
        for piece in current_player.pieces:
            if piece != -1:
                for opponent_piece in opponent.pieces:
                    if opponent_piece == piece and not board.is_safe_spot(piece):
                        score -= 25  

        return score

    def choose_piece(self, dice_roll, board):
        self.nodes_visited = 0
        best_value = -float('inf')
        best_piece = None

        for piece_index in self.get_available_pieces(dice_roll):
            new_position = self.pieces[piece_index] + dice_roll
            if new_position > 56:
                new_position = 56
            original_position = self.pieces[piece_index]
            self.pieces[piece_index] = new_position
            value = self.expectiminimax(board, [self, self], 0, self.depth, False, dice_roll)
            #هون علمنا تراجع عن الحركة 
            self.pieces[piece_index] = original_position 

            if value > best_value:
                best_value = value
                best_piece = piece_index

        if self.verbose:
            print(f"AI chose piece {best_piece} with evaluation value {best_value}")
            print(f"Total nodes visited: {self.nodes_visited}")
        return best_piece