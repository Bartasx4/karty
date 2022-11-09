from deck import Card
from deck import Deck


class Player:

    def __init__(self, table_deck: Deck, nick='', computer=True):
        self.nick = nick
        self.computer = computer
        self.table_deck = table_deck
        self.points = 0
        self.hand_deck = Deck()
        self.down_deck = Deck()
        self.up_deck = Deck()

    def move(self):
        if not self.hand_deck.empty:
            if self.__can_put_deck(self.hand_deck):
                self.__put_on_table(self.hand_deck)
        return True

    def hand(self):
        print('Hand:')
        self.hand_deck.print_all()
        print('Cards up:')
        self.up_deck.print_all()
        print('')

    def __can_put_card(self, card: Card):
        if self.table_deck.last <= card:
            return True
        return False

    def __can_put_deck(self, player_hand: Deck):
        for in_hand in player_hand:
            if self.table_deck.table.last <= in_hand:
                return True
        return False

    def __last_chance(self):
        if not self.table_deck.empty:
            last_chance_card = self.table_deck.get()
            if last_chance_card >= self.table_deck.table.last:
                self.table_deck.add(last_chance_card)
            else:
                self.hand_deck.add(last_chance_card)
                self.hand_deck.add(self.table_deck.table)

    def __put_on_table(self, player_deck):
        cards_can_put = []
        for card in player_deck:
            if self.__can_put_card(card):
                cards_can_put.append(card)
        to_put_index = min(cards_can_put, key=lambda card_: card_.points)
        to_put_card = cards_can_put[to_put_index]
        self.table_deck.table.add(player_deck.get_card_by_value(to_put_card))
        if not self.table_deck.empty:
            player_deck.add(self.table_deck.get())
        while card := player_deck.get_card_by_value(self.table_deck.last):
            self.table_deck.table.add(card)
            if not self.table_deck.empty:
                player_deck.add(self.table_deck.get())
