from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

class Board:
    def __init__(self):
        self.safe_spots = {0, 8, 13, 21, 26, 34, 39, 47}  # Safe spots
        self.path_length = 56  # Length of the path from start to finish

    def is_safe_spot(self, position):
        """Check if the position is a safe spot."""
        return position in self.safe_spots

    def is_wall(self, players, position):
        """Check if there is a wall at the position (two or more pieces of the same player)."""
        for player in players:
            count = player.pieces.count(position)
            if count >= 2:
                return True
        return False

    def get_board_state(self, players):
        """Get the current state of the board (positions of all pieces)."""
        board_state = {}
        for player in players:
            board_state[player.name] = player.pieces.copy()
        return board_state

    def get_pieces_at_position(self, players, position):
        """Get the pieces at a specific position with their colors."""
        pieces = []
        for player in players:
            for i, pos in enumerate(player.pieces):
                if pos == position:
                    pieces.append((i, player.color))
        return pieces

    def print_base_pieces(self, players):
        """Print the pieces in the base as colored squares."""
        print("\nPieces in the Base:")
        for player in players:
            pieces_in_base = player.pieces.count(-1)
            if pieces_in_base > 0:
                # Colored squares for each player
                if player.color == "Red":
                    squares = Fore.RED + " ■ " * pieces_in_base
                elif player.color == "Blue":
                    squares = Fore.BLUE + " ■ " * pieces_in_base
                print(f"{player.name} ({player.color}): {squares}")
            else:
                # Circles if no pieces are left in the base
                if player.color == "Red":
                    circles = Fore.RED + " ● "
                elif player.color == "Blue":
                    circles = Fore.BLUE + " ● "
                print(f"{player.name} ({player.color}): {circles}")

    def print_board(self, players):
        """Print the game board in a horizontal layout with formatting."""
        self.print_base_pieces(players)  # Print pieces in the base
        print("\nGame Board:")
        print("=" * 80)
        for i in range(0, self.path_length + 1, 10):  # Print 10 cells per row
            for j in range(i, min(i + 10, self.path_length + 1)):
                # Get the pieces at this position
                pieces = self.get_pieces_at_position(players, j)
                # Determine the cell color and content
                if j in self.safe_spots:
                    cell_color = Back.YELLOW + Fore.BLACK  # Safe spots
                elif len(pieces) >= 2 and all(p[1] == pieces[0][1] for p in pieces):
                    # Two or more pieces of the same player
                    cell_color = Back.BLUE + Fore.WHITE if pieces[0][1] == "Blue" else Back.RED + Fore.WHITE
                elif len(pieces) >= 1:
                    # Mixed pieces or single piece
                    cell_color = Back.WHITE + Fore.BLACK
                else:
                    # Empty cell
                    cell_color = Back.WHITE + Fore.BLACK
                # Prepare the cell content
                cell_content = f" {j:2} "
                if pieces:
                    if j in self.safe_spots:
                        # Safe spot: keep the background color, change the text color
                        cell_content = f" {j:2} "
                        for p in pieces:
                            if p[1] == "Red":
                                cell_content += Fore.RED + "■"
                            elif p[1] == "Blue":
                                cell_content += Fore.BLUE + "■"
                    else:
                        # Normal spot: change the background color, keep the text color
                        cell_content = f" {j:2} "
                        for p in pieces:
                            if p[1] == "Red":
                                cell_content += Fore.RED + "■"
                            elif p[1] == "Blue":
                                cell_content += Fore.BLUE + "■"
                # Print the cell
                print(cell_color + cell_content, end="")
            print("\n" + "-" * 80)
        print("=" * 80)