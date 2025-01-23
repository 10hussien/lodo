from player import Player
from ai_player import AIPlayer
from game import Game
from board import Board
from ludo_gui import LudoGame
import tkinter as tk

def main():
    print("Welcome to Ludo Game!")
    
    # اختيار الواجهة (Terminal أو GUI)
    interface_choice = input("Choose interface (1 for Terminal, 2 for GUI): ").strip()
    
    if interface_choice == "1":
        # اللعب في التيرمنال
        print("You have chosen to play in the Terminal.")
        mode = input("Do you want to play against the computer? (yes/no): ").strip().lower()
        
        if mode == "yes":
            
            verbose = input("Do you want to see AI decision details? (yes/no): ").strip().lower() == "yes"
            board = Board()  
            player1 = Player("Player 1", "Red")
            player2 = AIPlayer("AI Player", "Blue", board, 4, verbose)
        else:
            player1 = Player("Player 1", "Red")
            player2 = Player("Player 2", "Blue")

        # بدء اللعبة في التيرمنال
        game = Game(player1, player2)
        game.play_game()
    
    elif interface_choice == "2":
        # اللعب في الواجهة الرسومية (GUI)
        print("You have chosen to play in the GUI.")
        mode = input("Do you want to play against the computer? (yes/no): ").strip().lower()
        
        if mode == "yes":

            verbose = input("Do you want to see AI decision details? (yes/no): ").strip().lower() == "yes"
            board = Board()  
            player1 = Player("Player 1", "red")
            player2 = AIPlayer("AI Player", "blue", board, 4, verbose)
        else:
            # إذا كان اللعب ضد لاعب آخر في الواجهة الرسومية
            player1 = Player("Player 1", "red")
            player2 = Player("Player 2", "blue")

        # بدء الواجهة الرسومية
        root = tk.Tk()
        gui_game = LudoGame(root, player1, player2)  # بدء اللعبة مع الواجهة الرسومية
        root.mainloop()
    
    else:
        print("Invalid choice. Please choose 1 for Terminal or 2 for GUI.") 

if __name__ == "__main__":
    main()