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
    	if self.hand_deck.count > 0:
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
    		if self.table_deck.last <= in_hand:
    			return True
    	return False
    	
    def __put_on_table(self, player_deck):
    	cards_can_put = []
    	for card in player_deck:
    		if self.__can_put_card(card):
    			cards_can_put.append(card)
    	to_put_index = min(cards_can_put, key=lambda card: card.points)
    	to_put_card = cards_can_put[to_put_index]
    	while card:= player_deck.get_card_by_value:
    		self.table_deck.table.add(card)
    		if self.table_deck.count > 0:
    			player_deck.add(self.table_deck.get())
    	
    	
