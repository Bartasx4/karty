from typing import Dict
from typing import List
from deck import Card
from deck import Deck
from deck import PlayersGroup
from deck import CantDealCardError
from deck import NotYourTurnError
from deck.deck import is_same_dict


class Table:

    def __init__(self):
        points = [0, 3, 4, 5, 6, 7, 8, 9, 0, 11, 12, 13, 14]
        self.players = PlayersGroup()
        self.phase = 'start'  # start, main, end
        self.game_started = False
        self.dealer = Deck()
        self.discard_pile = Deck()
        self.dealer.set(points=points)
        self.__create_special_cards()

    def add_player(self, nick: str, computer=True):
        self.players.add_player(nick, computer=computer)

    def create_bots(self, bots_count=4):
        for i in range(bots_count):
            self.add_player(f'Bot_{i + 1}')

    def deal_card(self, player_id: int, deck_name: str, card: Card):
        self.__deal_card(player_id, deck_name, card)

    def deal_card_by_id(self, player_id: int, deck_name: str, index: int):
        card = self.players[player_id].get_deck(deck_name)[index]
        self.__deal_card(player_id, deck_name, card)

    def end_turn(self, player_id):
        if player_id != self.whose_turn:
        	raise NotYourTurnError('Wrong player.')
        if self.__check_end(player_id):
        	self.__end_player(player_id)
        self.draw_cards(self.players.current)
        if self.discard_pile.empty or self.discard_pile.last.special:
            return False
        return True

    @property
    def game_status(self) -> Dict[str, str]:
        return {'turn_id': self.players.current,
                'phase': self.phase,
                'game_started': self.game_started
                }

    @property
    def whose_turn(self) -> int:
        return self.players.current

    def start(self):
        self.players.reset()
        self.dealer = Deck()
        self.discard_pile = Deck()
        self.dealer.new_deck().shuffle()
        self.__split_cards()
        self.game_started = True
        self.phase = 'start'

    def draw_cards(self, player_id: int):
        id_ = player_id
        while self.players[id_].hand_deck.count > 3 and self.dealer.count > 0:
            self.players[id_].draw_card('hand_deck', self.dealer)
        return True

    def swap_cards(self, player_id: int, hand_card: Card, up_card: Card):
        if self.phase != 'start':
            raise Exception('Wrong phase of game.')
        player = self.players[player_id]
        player.hand_deck.add_card(player.up_deck.draw_by_card(up_card))
        player.up_deck.add_card(player.hand_deck.draw_by_card(hand_card))

    def swap_cards_by_id(self, player_id: int, hand_card_index: int, up_card_index: int):
        if self.phase != 'start':
            raise Exception('Wrong phase of game.')
        player = self.players[player_id]
        hand_card = player.hand_deck.draw(hand_card_index)
        up_card = player.up_deck.draw(up_card_index)
        player.hand_deck.add_card(up_card)
        player.up_deck.add_card(hand_card)

    def __can_deal_card(self, card: Card) -> bool:
        if card >= self.discard_pile.last or card.special:
            return True
        return False

    def __can_deal_deck(self, deck: Deck) -> bool:
        for card in deck:
            if self.__can_deal_card(card):
                return True
            return False

    def __check(self) -> bool:
        if not self.dealer.empty:
            for player in self.players:
                if player.hand_deck < 3:
                    return False
        if self.discard_pile.empty:
            return False
        return True

    def __check_end(self, player_id: int) -> bool:
        player = self.players[player_id]
        empty = [player.hand_deck.count == 0,
                       player.up_deck.count == 0,
                       player.down_deck == 0]
        return all(empty)
        
    def _create_decks(self):
        self.players.create_deck('up_deck', show_name='Up deck', hidden=False, max_cards=3, can_draw=False)
        self.players.create_deck('down_deck', show_name='Down deck', hidden=True, max_cards=3, can_draw=False)

    def __create_special_cards(self):
        cards = []
        for color in Deck().suits:
            cards.append(Card(value='2', color=color, points=0, special=True))
            cards.append(Card(value='10', color=color, points=0, special=True))
        self.dealer.set_special_cards(cards)

    def __deal_card(self, player_id: int, deck_name: str, card: Card) -> bool:
        player_deck = self.players[player_id].get_deck(deck_name)
        if self.discard_pile.last > card and not card.special:
            raise CantDealCardError('Can\'t deal card.')
        self.discard_pile.add_card(player_deck.draw_by_card(card))
        if card.special:
            self.__deal_special(card)
        return True
    
    def __deal_special(self, card):
    	if card.value == '10':
    		self.discard_pile.clear()
    	if card.value == '2':
    		pass

    def __end_game(self):
        self.game_started = False
        
    def __end_player(self, player_id):
    	win = False if self.discard_pile.last.special else True
    	if win:
    		for index, value in enumerate(self.winners):
    			if value == -1:
    				self.winners[index] = player_id
    				return

    def __last_four(self) -> bool:
        if self.discard_pile.count < 4:
            return False
        last_cards = self.discard_pile[-4:]
        last_one = self.discard_pile.last
        for card in last_cards:
            same = is_same_dict(card, last_one)['value']
            if not same:
                return False
            self.discard_pile.clear()
        return True

    def __split_cards(self):
        for player in self.players:
            stacks = [player.hand_deck, player.up_deck, player.down_deck]
            for player_deck in stacks:
                for _ in range(3):
                    player_deck.add_card(self.dealer.draw())
