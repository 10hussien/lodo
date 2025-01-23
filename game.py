import random
from board import Board
from ai_player import AIPlayer
from lodo_rulse import Rules  # استيراد فئة Rules

class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.board = Board()
        self.rules = Rules()  # إنشاء كائن من فئة Rules
        self.current_player_index = random.randint(0, 1)  # اختيار لاعب عشوائي لبدء اللعبة
        self.last_board_state = None  # تتبع آخر حالة للوحة

    def roll_dice(self):
        input("Press Enter to roll the dice :")
        return self.rules.roll_dice()

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def play_turn(self):
        current_player = self.players[self.current_player_index]
        print(f"\n{current_player.name}'s turn ({current_player.color})")

        dice_results = []
        while True:
            dice_roll = self.roll_dice()
            print(f"Dice roll: {dice_roll}")
            dice_results.append(dice_roll)
            if dice_roll != 6 :
                break  

        print(f"All dice results: {dice_results}")

        
        for dice_roll in dice_results:
            print(f"\nUsing dice result: {dice_roll}")
            available_pieces = current_player.get_available_pieces(dice_roll)
            if not available_pieces:
                print(f"{current_player.name} cannot move any pieces with this dice roll.")
                continue 

            print("Available pieces to move:")
            for piece_index in available_pieces:
                if current_player.pieces[piece_index] == -1:
                    print(f"{piece_index}: Piece in the base")
                else:
                    new_position = current_player.pieces[piece_index] + dice_roll
                    if new_position > 56:
                        new_position = 56
                    print(f"{piece_index}: Piece at position {current_player.pieces[piece_index]}")

            if isinstance(current_player, AIPlayer):
                piece_index = current_player.choose_piece(dice_roll, self.board) 
            else:
                while True:
                    try:
                        piece_index = int(input("Choose a piece to move (enter the number): "))
                        if piece_index not in available_pieces:
                            print("Invalid choice. You cannot move this piece. Try again.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. You must enter a number. Try again.")

            if current_player.move_piece(piece_index, dice_roll):
                new_position = current_player.pieces[piece_index]
                print(f"{current_player.name} moved piece {piece_index} to position {new_position}.")

                self.rules.check_and_displace_piece(self.players, current_player, new_position)
            else:
                print("Invalid move. You cannot move this piece. Try again.")

        if dice_results[-1] != 6:
            self.switch_player()

    def check_win(self):
        for player in self.players:
            if player.has_won():
                return player
        return None

    def play_game(self):
        print("Starting Ludo Game!")
        self.board.print_board(self.players)
        self.last_board_state = self.board.get_board_state(self.players)  
        winner = None
        while not winner:
            self.play_turn()
            current_board_state = self.board.get_board_state(self.players)
            if current_board_state != self.last_board_state:
                self.board.print_board(self.players)
                self.last_board_state = current_board_state
            winner = self.check_win()
        print(f"{winner.name} ({winner.color}) has won the game!")