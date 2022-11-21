from deck import Deck
from random import choice


class AI:

    def __init__(self, player, table):
        self.player = player
        self.table = table

    def move(self):
        hand_deck = self.player.hand_deck
        up_deck = self.player.up_deck
        down_deck = self.player.down_deck
        if self.table.phase == 'start':
            return self.__swap_cards()
        if not hand_deck.empty:
            if self.player.can_deal_deck(hand_deck):
                return self.__put_on_table(hand_deck)
        elif not up_deck.empty:
            if self.player.can_deal_deck(up_deck):
                return self.__put_on_table(up_deck)
        else:
            if self.player.can_deal_deck(down_deck):
                return self.__put_on_table(down_deck)

        if self.__put_on_table(hand_deck): return True
        if self.__put_on_table(up_deck): return True
        if self.__put_on_table(down_deck): return True
        if self.__play_down_deck(): return True
        return self.__last_chance()

    def __swap_cards(self):
        changing = True
        hand_deck = self.player.hand_deck
        up_deck = self.player.up_deck
        while changing:
            changing = False
            for hand_card in hand_deck:
                for up_card in up_deck:
                    if (hand_card > up_card or Deck().is_special(hand_card)) and (not Deck().is_special(up_card)):
                        hand_deck.add(up_deck.get_card(up_card))
                        up_deck.add(hand_deck.get_card(hand_card))
                        changing = True
                        break
                if changing:
                    break
        return True

    def __last_chance(self):
        hand_deck = self.player.hand_deck
        if not self.table.dealer.empty:
            if last_chance_card := self.table.dealer.get() >= self.table.table.last:
                self.table.table.add(last_chance_card)
                return True
            hand_deck.add(last_chance_card)
        hand_deck.add(self.table.table)
        self.table.table.clear()
        return False

    def __put_on_table(self, player_deck: Deck):
        cards_can_dealt = self.player.can_deal_deck(self.player.hand_deck)
        if not cards_can_dealt:
            return False
        cards_to_deal = Deck()
        cards_to_deal.add(player_deck.get_card(cards_can_dealt[0]))
        while True:
            if cards_can_dealt and Deck().is_same_dict(cards_to_deal[0], cards_can_dealt[0])['value']:
                cards_to_deal.add(player_deck.get_card(cards_can_dealt[0]))
                self.player.take_cards()
            else:
                break
        self.table.table.add(cards_to_deal)
        return True

    def __play_down_deck(self):
        if self.player.hand_deck.count == 0 and \
        	self.player.up_deck.count == 0:
        	pass
        down_deck = self.player.down_deck
        hand_deck = self.player.hand_deck
        table_deck = self.table.table
        card = choice(down_deck)
        if card > self.table.table_deck.last:
        	self.table.add(down_deck.get_card(card))
        	return True
        hand_deck.add(down_deck.get_card(card))
        hand_deck.add(table_deck)
        table_deck.clear()