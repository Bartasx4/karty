from deck import Card
from deck import Deck
from interface import Interface


class Player:

    def __init__(self, table, nick='', computer=True):
        self.nick = nick
        self.computer = computer
        self.table = table
        self.points = 0
        self.hand_deck = Deck()
        self.down_deck = Deck()
        self.up_deck = Deck()
        self.interface = Interface(self)
        self.move = self.interface.move

    '''
    def move(self):
        if self.table.phase == 'start':
            return self.__swap_cards()
        if not self.hand_deck.empty:
            if self.__can_dealt_deck(self.hand_deck):
                self.__dealt_on_table(self.hand_deck)
            else:
                self.__last_chance()
        return True
    '''

    def print_hand(self):
        print('Hand:')
        self.hand_deck.print_all()
        print('Cards up:')
        self.up_deck.print_all()
        print('')

    def __swap_cards(self):
        changing = True
        while changing:
            changing = False
            for hand_card in self.hand_deck:
                for up_card in self.up_deck:
                    if (hand_card > up_card or Deck().is_special(hand_card)) and (not Deck().is_special(up_card)):
                        self.hand_deck.add(self.up_deck.get_card(up_card))
                        self.up_deck.add(self.hand_deck.get_card(hand_card))
                        changing = True
                        break
                if changing:
                    break

    def __can_dealt_card(self, card: Card):
        if self.table.table.last <= card:
            return True
        return False

    def __can_dealt_deck(self, player_hand: Deck):
        for in_hand in player_hand:
            if self.table.table.last <= in_hand:
                return True
        return False

    def __last_chance(self):
        if not self.table.table.empty:
            last_chance_card = self.table.dealer.get()
            if last_chance_card >= self.table.table.last:
                self.table.table.add(last_chance_card)
                return True
            self.hand_deck.add(last_chance_card)
            self.hand_deck.add(self.table.table)
            self.table.table.clear()
        return False

    def __dealt_on_table(self, player_deck: Deck):
        cards_can_dealt = [card for card in player_deck if self.__can_dealt_card(card)]
        cards_to_dealt = Deck()
        cards_to_dealt.add(player_deck.get_card(cards_can_dealt[0]))
        while True:
            if cards_can_dealt and Deck().is_same_dict(cards_to_dealt[0], cards_can_dealt[0])['value']:
                cards_to_dealt.add(player_deck.get_card(cards_can_dealt[0]))
            else:
                break
        self.table.table.add(cards_to_dealt)
        while player_deck.count < 3 and self.table.table.count > 0:
            player_deck.add(self.table.table.get())

    def __repr__(self):
        descr = 'Bot' if self.computer else 'Human'
        return f'({self.nick}, {descr})'
