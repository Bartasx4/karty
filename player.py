from deck import Card
from deck import Deck
from interface import Interface
from ai import AI


class Player:

    def __init__(self, table, nick='', computer=True):
        self.nick = nick
        self.computer = computer
        self.table = table
        self.points = 0
        self.hand_deck = Deck()
        self.down_deck = Deck()
        self.up_deck = Deck()
        self.interface = AI(player=self, table=table) if computer else Interface(player=self, table=table)
        self.move = self.interface.move

    def can_deal_card(self, card: Card):
        if self.table.table.last <= card:
            return True
        return False

    def can_deal_deck(self, player_hand: Deck):
        can_deal = []
        for in_hand in player_hand:
            if self.table.table.last <= in_hand:
                can_deal.append(in_hand)
        return sorted(can_deal, key=lambda card: card.points)

    def take_cards(self):
        while self.hand_deck.count < 3 and self.table.dealer.get() > 0:
            self.hand_deck.add(self.table.dealer.get())

    def print_hand(self):
        print('Hand:')
        self.hand_deck.print_all()
        print('Cards up:')
        self.up_deck.print_all()
        print('')

    def __repr__(self):
        descr = 'Bot' if self.computer else 'Human'
        return f'({self.nick}, {descr})'
