from deck import Deck


class Player:

    def __init__(self, id_, nick='', computer=True):
        self.id_ = id_
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
        self.hand_deck.show()
        print('Cards up:')
        self.up_deck.show()
        print('')
