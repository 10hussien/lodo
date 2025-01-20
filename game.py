import random
from board import Board
class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.board = Board()
        self.current_player_index = random.randint(0, 1)  # Randomly choose a player to start
        self.last_board_state = None  # Track the last state of the board

    def roll_dice(self):
        """Roll the dice by pressing Enter."""
        input("Press Enter to roll the dice...")
        return random.randint(1, 6)

    def switch_player(self):
        """Switch turns between players."""
        self.current_player_index = 1 - self.current_player_index

    def should_return_piece(self, players, position):
        """Check if a piece should be sent back to the base."""
        # If the piece is in a safe spot, position 0, or positions 51-55, do not return it
        if (self.board.is_safe_spot(position) or
            position == 0 or
            51 <= position <= 55):
            return False
        # If there is a wall (two or more pieces of the same player), do not return it
        if self.board.is_wall(players, position):
            return False
        return True

    def play_turn(self):
        """Play the current player's turn."""
        current_player = self.players[self.current_player_index]
        print(f"\n{current_player.name}'s turn ({current_player.color})")
        dice_roll = self.roll_dice()
        print(f"Dice roll: {dice_roll}")

        # Get available pieces to move
        available_pieces = current_player.get_available_pieces(dice_roll)
        if not available_pieces:
            print(f"{current_player.name} cannot move any pieces. Turn passes to the next player.")
            self.switch_player()
            return

        # Display available pieces to move
        print("Available pieces to move:")
        for piece_index in available_pieces:
            if current_player.pieces[piece_index] == -1:
                print(f"{piece_index}: Piece in the base")
            else:
                print(f"{piece_index}: Piece at position {current_player.pieces[piece_index]}")

        # Choose a piece to move
        while True:
            piece_index = int(input("Choose a piece to move (enter the number): "))
            if piece_index not in available_pieces:
                print("Invalid choice. You cannot move this piece. Try again.")
                continue
            # Move the piece
            if current_player.move_piece(piece_index, dice_roll):
                new_position = current_player.pieces[piece_index]
                print(f"{current_player.name} moved piece {piece_index} to position {new_position}.")
                # Check if an opponent's piece is displaced
                for player in self.players:
                    if player != current_player:
                        for i, pos in enumerate(player.pieces):
                            if pos == new_position and self.should_return_piece(self.players, new_position):
                                player.pieces[i] = -1  # Send the piece back to the base
                                print(f"{current_player.name} displaced {player.name}'s piece!")
                                if dice_roll != 6:
                                    self.switch_player()  # Extra turn
                break
            else:
                print("Invalid move. You cannot move this piece. Try again.")

        if dice_roll != 6:
            self.switch_player()

    def check_win(self):
        """Check if a player has won."""
        for player in self.players:
            if player.has_won():
                return player
        return None

    def play_game(self):
        """Start the game."""
        print("Starting Ludo Game!")
        self.board.print_board(self.players)
        self.last_board_state = self.board.get_board_state(self.players)  # Initialize the last board state
        winner = None
        while not winner:
            self.play_turn()
            # Check if the board state has changed
            current_board_state = self.board.get_board_state(self.players)
            if current_board_state != self.last_board_state:
                self.board.print_board(self.players)
                self.last_board_state = current_board_state  # Update the last board state
            winner = self.check_win()
        print(f"{winner.name} ({winner.color}) has won the game!")