from player import Player
from game import Game

# إنشاء اللاعبين
player1 = Player("Player 1", "Red")
player2 = Player("Player 2", "Blue")

# بدء اللعبة
game = Game(player1, player2)
game.play_game()