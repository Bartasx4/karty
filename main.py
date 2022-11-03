from vandtia import Vandtia

if __name__ == '__main__':
    game = Vandtia()
    game.start()
    print(game.players[0].hand_deck)
