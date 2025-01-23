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
        """خوارزمية Expectiminimax لاتخاذ القرار."""
        self.nodes_visited += 1

        if depth == 0 or self.has_won() or players[1 - current_player_index].has_won():
            value = self.heuristic(board, players)
            if self.verbose:
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
                current_player.pieces[piece_index] = original_position  # التراجع عن الحركة
                value = max(value, child_value)
            return value
        else:
            value = 0
            for dice in range(1, 7):  # جميع النتائج الممكنة لرمي النرد (1 إلى 6)
                probability = 1 / 6  # احتمالية كل نتيجة
                child_value = self.expectiminimax(board, players, 1 - current_player_index, depth - 1, True, dice)
                value += probability * child_value
            return value

    def heuristic(self, board, players):
        """تابع التقييم لحساب قيمة الوضع الحالي."""
        current_player = self
        opponent = players[1 - players.index(current_player)]
        score = 0

        # 1. زيادة النقاط بناءً على عدد القطع التي وصلت للنهاية
        score += current_player.finished_pieces * 20

        # 2. تقليل النقاط بناءً على عدد القطع التي وصلت للنهاية للخصم
        score -= opponent.finished_pieces * 20

        # 3. زيادة النقاط بناءً على القطع الموجودة على اللوحة
        for piece in current_player.pieces:
            if piece != -1:
                score += piece  # كلما كانت القطعة أقرب للنهاية، تزداد النقاط

        # 4. زيادة النقاط إذا كانت القطعة في خانة آمنة
        for piece in current_player.pieces:
            if piece != -1 and board.is_safe_spot(piece):
                score += 10

        # 5. زيادة النقاط إذا كانت القطعة قريبة من النهاية
        for piece in current_player.pieces:
            if piece != -1 and piece >= 50:
                score += 15

        # 6. زيادة النقاط إذا كانت القطعة تقتل قطعة الخصم
        for piece in current_player.pieces:
            if piece != -1:
                for opponent_piece in opponent.pieces:
                    if opponent_piece == piece and not board.is_safe_spot(piece):
                        score += 30  # زيادة كبيرة إذا قتلت قطعة الخصم

        # 7. تقليل النقاط إذا كانت القطعة في خطر القتل
        for piece in current_player.pieces:
            if piece != -1:
                for opponent_piece in opponent.pieces:
                    if opponent_piece == piece and not board.is_safe_spot(piece):
                        score -= 15  # تقليل النقاط إذا كانت القطعة في خطر

        return score

    def choose_piece(self, dice_roll, board):
        """اختيار قطعة للتحريك باستخدام خوارزمية Expectiminimax."""
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
            # التراجع عن الحركة
            self.pieces[piece_index] = original_position 

            if value > best_value:
                best_value = value
                best_piece = piece_index

        if self.verbose:
            print(f"AI chose piece {best_piece} with evaluation value {best_value}")
            print(f"Total nodes visited: {self.nodes_visited}")
        return best_piece