import random

class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.pieces = [0, 0, 0, 0]  # 0 يعني القطعة في القاعدة
        self.finished_pieces = 0

    def has_pieces_in_base(self):
        return any(piece == 0 for piece in self.pieces)

    def has_pieces_on_board(self):
        return any(piece > 0 for piece in self.pieces)

    def move_piece(self, piece_index, steps):
        if self.pieces[piece_index] == 0 and steps != 6:
            return False  # لا يمكن تحريك القطعة من القاعدة إلا برقم 6
        self.pieces[piece_index] += steps
        if self.pieces[piece_index] > 57:  # افترضنا أن اللوحة تحتوي على 57 خانة
            self.pieces[piece_index] = 57
        return True

class Board:
    def __init__(self):
        self.safe_spots = {1, 9, 14, 22, 27, 35, 40, 48}  # الخانات الآمنة
        self.players_pieces = {}  # لتخزين مواقع قطع اللاعبين

    def is_safe_spot(self, position):
        return position in self.safe_spots

    def is_occupied(self, position):
        return any(position in pieces for pieces in self.players_pieces.values())

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.board = Board()
        self.current_player_index = 0

    def roll_dice(self):
        return random.randint(1, 6)

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def play_turn(self):
        current_player = self.players[self.current_player_index]
        dice_roll = self.roll_dice()
        print(f"{current_player.name} rolled a {dice_roll}")

        if dice_roll == 6 and current_player.has_pieces_in_base():
            # تحريك قطعة من القاعدة إلى موضع البداية
            for i in range(4):
                if current_player.pieces[i] == 0:
                    current_player.move_piece(i, 1)
                    break
        elif current_player.has_pieces_on_board():
            # اختيار قطعة لتحريكها
            piece_index = int(input(f"{current_player.name}, choose a piece to move (0-3): "))
            if 0 <= piece_index < 4:
                if current_player.move_piece(piece_index, dice_roll):
                    print(f"Moved piece {piece_index} to position {current_player.pieces[piece_index]}")
                else:
                    print("Invalid move")
            else:
                print("Invalid piece index")
        else:
            print("No pieces on board to move")

        if dice_roll == 6:
            print("You rolled a 6, you get another turn!")
        else:
            self.switch_player()

    def check_win(self):
        for player in self.players:
            if all(piece == 57 for piece in player.pieces):
                return player
        return None

    def play_game(self):
        winner = None
        while not winner:
            self.play_turn()
            winner = self.check_win()
        print(f"{winner.name} has won the game!")

# إنشاء اللاعبين وبدء اللعبة
player1 = Player("Player 1", "Red")
player2 = Player("Player 2", "Blue")
game = Game(player1, player2)
game.play_game()