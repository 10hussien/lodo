from game import Game

if __name__ == "__main__":
    game = Game()

    # عرض الرقعة قبل بدء اللعبة
    game.start()

    # بدء اللعبة
    while True:
        if game.play_turn():
            break