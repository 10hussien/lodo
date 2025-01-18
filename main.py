from game import Game

if __name__ == "__main__":
    num_players = 4
    game = Game(num_players)

    while True:
        if game.next_turn():
            break