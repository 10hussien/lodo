from player import Player
from ai_player import AIPlayer
from game import Game
from board import Board

def main():
    print("Welcome to Ludo Game!")
    mode = input("Do you want to play against the computer? (yes/no): ").strip().lower()
    
    if mode == "yes":
        depth = int(input("Enter the depth for the AI (e.g., 3): "))
        verbose = input("Do you want to see AI decision details? (yes/no): ").strip().lower() == "yes"
        board = Board()  
        player1 = Player("Player 1", "Red")
        player2 = AIPlayer("AI Player", "Blue",board, depth, verbose)
    else:
        player1 = Player("Player 1", "Red")
        player2 = Player("Player 2", "Blue")

    game = Game(player1, player2)
    game.play_game()

if __name__ == "__main__":
    main()