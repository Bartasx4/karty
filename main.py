from table import Table
from player import Player
from deck import Deck


if __name__ == '__main__':
    player = Player(table=None, nick='Bartek', computer=False)
    game = Table(players=[player])
    print(game.players)
    from random import choice
    game.dealer.new_deck()
    print(choice(game.dealer))
    exit()
    game.start()
    game.players[0].print_hand()
    print('')
    game.players[0].print_hand()
