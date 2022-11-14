from table import Table
from player import Player
from deck import Deck


if __name__ == '__main__':
    player = Player(table=None, nick='Bartek', computer=False)
    game = Table(players=[player])
    print(game.players)
    game.start()
    game.players[0].print_hand()
    print('')
    game.players[0].print_hand()
