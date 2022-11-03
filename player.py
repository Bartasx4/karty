from deck import Deck


class Player:

    def __init__(self, nick='', computer=True):
        self.nick = nick
        self.computer = computer
        self.points = 0
        self.hand_deck = Deck()
        self.down_deck = Deck()
        self.up_deck = Deck()

    def move(self, table):
        pass

    def hand(self):
        print('Hand:')
        self.hand_deck.print_all()
        print('Cards up:')
        self.up_deck.print_all()
        print('')