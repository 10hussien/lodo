from colorama import Fore, Back, Style, init
from lodo_rulse import Rules  
init(autoreset=True)

class Board:
    def __init__(self):
        self.rules = Rules()

    def is_safe_spot(self, position):
        return self.rules.is_safe_spot(position)

    def is_wall(self, players, position):
        return self.rules.is_wall(players, position)

    def should_return_piece(self, players, position):
        return self.rules.should_return_piece(players, position)

    def get_pieces_at_position(self, players, position):
        return self.rules.get_pieces_at_position(players, position)
    
    def get_board_state(self, players):
        return self.rules.get_board_state(players)

    def print_base_pieces(self, players):
        print("\nPieces in the Base:")
        for player in players:
            pieces_in_base = player.pieces.count(-1)
            if pieces_in_base > 0:
                if player.color == "Red":
                    squares = Fore.RED + " ■ " * pieces_in_base
                elif player.color == "Blue":
                    squares = Fore.BLUE + " ■ " * pieces_in_base
                print(f"{player.name} ({player.color}): {squares}")
            else:
                if player.color == "Red":
                    circles = Fore.RED + " ● "
                elif player.color == "Blue":
                    circles = Fore.BLUE + " ● "
                print(f"{player.name} ({player.color}): {circles}")

    def print_board(self, players):
        self.print_base_pieces(players) 
        print("\nGame Board:")
        print("=" * 80)

        for player in players:
            print(f"\n{player.name}'s Board ({player.color}):")
            print("-" * 80)
            for i in range(0, self.rules.path_length + 1, 10):  
                for j in range(i, min(i + 10, self.rules.path_length + 1)):
                    pieces = self.get_pieces_at_position(players, j)
                    if j in self.rules.safe_spots:  
                        cell_color = Back.YELLOW + Fore.BLACK  
                    elif len(pieces) >= 2 and all(p[1] == pieces[0][1] for p in pieces):
                        cell_color = Back.BLUE + Fore.WHITE if pieces[0][1] == "Blue" else Back.RED + Fore.WHITE
                    elif len(pieces) >= 1:
                        cell_color = Back.WHITE + Fore.BLACK
                    else:
                        cell_color = Back.WHITE + Fore.BLACK
                    cell_content = f" {j:2} "
                    if pieces:
                        if j in self.rules.safe_spots:  
                            cell_content = f" {j:2} "
                            for p in pieces:
                                if p[1] == player.color:  
                                    cell_content += Fore.RED + "■" if p[1] == "Red" else Fore.BLUE + "■"
                        else:
                            cell_content = f" {j:2} "
                            for p in pieces:
                                if p[1] == player.color:  
                                    cell_content += Fore.RED + "■" if p[1] == "Red" else Fore.BLUE + "■"
                    print(cell_color + cell_content, end="")
                print("\n" + "-" * 80)
        print("=" * 80)