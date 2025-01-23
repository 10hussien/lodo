import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from lodo_rulse import Rules
from player import Player 
from ai_player import AIPlayer
from tkinter import Toplevel, Label
import time

COLORS = ["white", "red", "green", "yellow", "blue", "black", 'gray']

BOARD_SIZE = 800 
CELL_SIZE = BOARD_SIZE // 16  

colorMatrix = [
    [2, 2, 2, 2, 2, 2, 0, 0, 0, 4, 4, 4, 4, 4, 4],
    [2, 0, 2, 2, 0, 2, 6, 4, 4, 4, 0, 4, 4, 0, 4],
    [2, 2, 2, 2, 2, 2, 0, 4, 0, 4, 4, 4, 4, 4, 4],
    [2, 2, 2, 2, 2, 2, 0, 4, 0, 4, 4, 4, 4, 4, 4],
    [2, 0, 2, 2, 0, 2, 0, 4, 0, 4, 0, 4 , 4, 0, 4],
    [2, 2, 2, 2, 2, 2, 0, 4, 0, 4, 4, 4, 4, 4, 4],
    [0, 2, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 6, 0],
    [0, 2, 2, 2, 2, 2, 6, 5 , 6, 3, 3, 3, 3,3, 0],
    [0, 6, 0, 0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 6, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 3, 3, 3, 3, 3, 3],
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 3, 0, 3, 3, 0, 3],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 3, 3, 3, 3, 3, 3],
    [1, 1, 1, 1, 1, 1, 0, 1, 0, 3, 3, 3, 3, 3, 3],
    [1, 0, 1, 1, 0, 1, 1, 1, 3, 3, 0, 3, 3, 0, 3],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 3, 3, 3, 3, 3, 3]
]

#لكل لاعب مسار معين رح يمشي فيه ورح يبلش وينهي فيه  هون للاول
player1_path= [
    (6,13),(6,12),(6,11),(6,10),(6,9),
    (5,8),(4,8),(3,8),(2,8),(1,8),(0,8),
    (0,7),(0,6),
    (1,6),(2,6),(3,6),(4,6),(5,6),
    (6,5),(6,4),(6,3),(6,2),(6,1),(6,0),
    (7,0),(8,0),
    (8,1),(8,2),(8,3),(8,4),(8,5),
    (9,6),(10,6),(11,6),(12,6),(13,6),(14,6),
    (14,7),(14,8),
    (13,8),(12,8),(11,8),(10,8),(9,8),
    (8,9),(8,10),(8,11),(8,12),(8,13),(8,14),
    (7,14),(7,13),(7,12),(7,11),(7,10),(7,9),(7,8)
]
#هون للثاني 
player2_path = [
    (8,1),(8,2),(8,3),(8,4),(8,5),
    (9,6),(10,6),(11,6),(12,6),(13,6),(14,6),
    (14,7),(14,8),
    (13,8),(12,8),(11,8),(10,8),(9,8),
    (8,9),(8,10),(8,11),(8,12),(8,13),(8,14),
    (7,14),(6,14),
    (6,13),(6,12),(6,11),(6,10),(6,9),
    (5,8),(4,8),(3,8),(2,8),(1,8),(0,8),
    (0,7),(0,6),
    (1,6),(2,6),(3,6),(4,6),(5,6),
    (6,5),(6,4),(6,3),(6,2),(6,1),(6,0),
    (7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6)
]

class LudoGame:
    def __init__(self, root, player1, player2):
        self.root = root
        self.root.title("Ludo Game")
        self.canvas = tk.Canvas(root, width=BOARD_SIZE, height=BOARD_SIZE, bg="bisque")
        self.canvas.pack()
        self.players = [player1, player2]  

        self.rules = Rules()

        self.base_positions = {
            "blue": [(10, 1), (10, 4), (13, 1), (13, 4)],
            "red": [(1, 10), (1, 13), (4, 10), (4, 13)]  
        }

        self.current_player_index = random.randint(0, 1)

        self.draw_board()

        self.play_turn()
    
    
    def roll_dice(self):
        return self.rules.roll_dice()
    
    def draw_base_pieces(self):
        for player in self.players:
            color = player.color
            positions = self.base_positions[color]  
            pieces_in_base = player.pieces.count(-1)  

            for i in range(4):  
                x, y = positions[i]
                if i < pieces_in_base:
                    self.canvas.create_oval(
                        x * CELL_SIZE + 10, y * CELL_SIZE + 10,
                        (x + 1) * CELL_SIZE - 10, (y + 1) * CELL_SIZE - 10,
                        fill="white", outline="black", width=2
                    )
                    self.canvas.create_oval(
                        x * CELL_SIZE + 15, y * CELL_SIZE + 15,
                        (x + 1) * CELL_SIZE - 15, (y + 1) * CELL_SIZE - 15,
                        fill=color, outline="black", width=1
                    )
                else:
                    self.canvas.create_rectangle(
                        x * CELL_SIZE, y * CELL_SIZE,
                        (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
                        fill="bisque", outline="black"
                    )

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(15):
            for j in range(15):
                x1, y1 = i * CELL_SIZE, j * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                color = COLORS[colorMatrix[j][i]]  
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        self.draw_base_pieces()
        self.draw_pieces()
        

    def draw_pieces(self):
        for player_index, player in enumerate(self.players):
            for piece_index, position in enumerate(player.pieces):
                if position != -1:  
                    x, y = self.get_position_coordinates(player_index, position)
                    pieces_in_cell = self.rules.get_pieces_at_position(self.players, position)
                    num_pieces = len(pieces_in_cell)
                    piece_size = CELL_SIZE // (num_pieces + 1)
                    
                    for i, (piece_idx, piece_color) in enumerate(pieces_in_cell):
                        offset_x = x * CELL_SIZE + (i + 1) * (piece_size // 2)
                        offset_y = y * CELL_SIZE + (i + 1) * (piece_size // 2)
                        self.canvas.create_oval(
                            offset_x, offset_y,
                            offset_x + piece_size, offset_y + piece_size,
                            fill=piece_color, outline="black", width=2
                        )

    def get_position_coordinates(self, player_index, position):
        if player_index == 0:  
            if position < len(player1_path):
                return player1_path[position]
        elif player_index == 1:  
            if position < len(player2_path):
                return player2_path[position]
        return (0, 0) 

    def get_available_pieces(self, player, steps):
        available_pieces = []
        if steps == 6:
            for i in range(4):
                if player.pieces[i] == -1:
                    available_pieces.append(i)
        for i in range(4):
            if player.pieces[i] != -1 and player.pieces[i] + steps <= 56:
                available_pieces.append(i)
        return available_pieces

    def move_piece(self, player, piece_index, steps):
        if player.pieces[piece_index] == -1 and steps != 6:
            return False  
        if player.pieces[piece_index] == -1:
            player.pieces[piece_index] = 0 
        else:
            new_position = player.pieces[piece_index] + steps
            if new_position > 56: 
                new_position = 56

            player.pieces[piece_index] = new_position

            self.rules.check_and_displace_piece(self.players, player, new_position)

        self.update_board()
        return True


    def should_return_piece(self, position):
        return self.rules.should_return_piece(self.players, position)

    def update_board(self):
        self.draw_board()

    def play_turn(self):
        current_player = self.players[self.current_player_index]

        if isinstance(current_player, AIPlayer):
            dice_results = []
            while True:
                dice_roll = self.roll_dice()
                dice_results.append(dice_roll)
                if dice_roll != 6:
                    break  
            self.show_dice_result(current_player.name, dice_results)

            for dice_roll in dice_results:
                available_pieces = current_player.get_available_pieces(dice_roll)
                if not available_pieces:
                    continue 

                piece_index = current_player.choose_piece(dice_roll, self.rules)
                self.move_piece(current_player, piece_index, dice_roll)
                if self.check_win(current_player):
                    messagebox.showinfo("Winner", f"{current_player.name} has won the game!")
                    return

            if dice_results[-1] == 6:
                self.play_turn()
            else:
                self.switch_player()
                self.play_turn()

        else:
            messagebox.showinfo("Your Turn", "Press OK to roll the dice...")

            dice_results = []
            while True:
                dice_roll = self.roll_dice()
                dice_results.append(dice_roll)
                messagebox.showinfo("Dice Roll", f"{current_player.name} rolled: {dice_roll}")
                if dice_roll != 6:
                    break  

            for dice_roll in dice_results:
                available_pieces = current_player.get_available_pieces(dice_roll)
                if not available_pieces:
                    messagebox.showinfo("No Moves", f"{current_player.name} cannot move any pieces for dice: {dice_roll}.")
                    continue  

                piece_info = "Available pieces to move:\n"
                for piece_index in available_pieces:
                    if current_player.pieces[piece_index] == -1:
                        piece_info += f"{piece_index}: Piece in the base\n"
                    else:
                        new_position = current_player.pieces[piece_index] + dice_roll
                        if new_position > 56:
                            new_position = 56
                        piece_info += f"{piece_index}: Piece at position {current_player.pieces[piece_index]}\n"

                piece_index = simpledialog.askinteger("Choose Piece", f"Dice: {dice_roll}\n{piece_info}\nChoose a piece to move (0-3):")
                if piece_index is not None and piece_index in available_pieces:
                    self.move_piece(current_player, piece_index, dice_roll)
                    if self.check_win(current_player):
                        messagebox.showinfo("Winner", f"{current_player.name} has won the game!")
                        return
                else:
                    messagebox.showwarning("Error", "Invalid choice. Please try again.")

            if dice_results[-1] == 6:
                self.play_turn()
            else:
                self.switch_player() 
                self.play_turn()  

    def show_dice_result(self, player_name, dice_results):
        self.dice_label = Label(
            self.root,
            text=f"{player_name} rolled: {dice_results}",  
            font=("Arial", 14),
            bg="white",  
            fg="black"   
        )
        
        self.dice_label.place(x=10, y=10)  

        self.root.after(5000, self.remove_dice_label)

    def remove_dice_label(self):
        if hasattr(self, 'dice_label'):
            self.dice_label.destroy()

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def check_win(self, player):
        return all(piece == 56 for piece in player.pieces)