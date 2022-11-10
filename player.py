from deck import Card
from deck import Deck


class Player:

    def __init__(self, dealer_deck: Deck, table_deck: Deck, nick='', computer=True):
        self.nick = nick
        self.computer = computer
        self.dealer_deck = dealer_deck
        self.table_deck = table_deck
        self.points = 0
        self.hand_deck = Deck()
        self.down_deck = Deck()
        self.up_deck = Deck()

    def move(self):
        if not self.hand_deck.empty:
            if self.__can_dealt_deck(self.hand_deck):
                self.__dealt_on_table(self.hand_deck)
            else:
                self.__last_chance()
        return True

    def hand(self):
        print('Hand:')
        self.hand_deck.print_all()
        print('Cards up:')
        self.up_deck.print_all()
        print('')

    def __can_dealt_card(self, card: Card):
        if self.table_deck.last <= card:
            return True
        return False

    def __can_dealt_deck(self, player_hand: Deck):
        for in_hand in player_hand:
            if self.table_deck.last <= in_hand:
                return True
        return False

    def __last_chance(self):
        if not self.table_deck.empty:
            last_chance_card = self.dealer_deck.get()
            if last_chance_card >= self.table_deck.last:
                self.table_deck.add(last_chance_card)
                return True
            self.hand_deck.add(last_chance_card)
            self.hand_deck.add(self.table_deck)
            self.table_deck.clear()
        return False

    def __dealt_on_table(self, player_deck: Deck):
        cards_can_dealt = [card for card in player_deck if self.__can_dealt_card(card)]
        to_dealt_sort = sorted(cards_can_dealt, key=lambda card: card.points)
        cards_to_dealt = Deck()
        cards_to_dealt.add(player_deck.get_card(cards_can_dealt[0]))
        while True:
            if cards_can_dealt and Deck().is_same_dict(cards_to_dealt[0], cards_can_dealt[0])['value']:
                cards_to_dealt.add(player_deck.get_card(cards_can_dealt[0]))
            else:
                break
        self.table_deck.add(cards_to_dealt)
        while player_deck.count < 3 and self.table_deck.count > 0:
            player_deck.add(self.table_deck.get())
