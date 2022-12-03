from typing import Dict

import deck
from deck import Card
from deck import Deck
from deck import PlayersGroup
from deck import CantDealCardError
from deck import NotYourTurnError
from deck.deck import is_same_dict
from ai import AI


class Table:

    def __init__(self):
        AI.end_turn = self.end_turn
        points = [0, 3, 4, 5, 6, 7, 8, 9, 0, 11, 12, 13, 14]
        self.players = PlayersGroup()
        self.dealer = Deck()
        self.dealer.set(points=points)
        self.discard_pile = Deck()
        self.phase = 'start'  # start, main, end
        self.game_started = False

    def add_player(self, nick: str, interface, computer=True):
        self.players.add_player(nick, interface, computer=computer)

    def create_bots(self, interface, bots_count=4):
        for i in range(bots_count):
            self.add_player(f'Bot_{i + 1}', interface)

    def deal_card(self, player_id: int, deck_name: str, card: Card):
        self.__deal_card(player_id, deck_name, card)

    def deal_card_by_id(self, player_id: int, deck_name: str, index: int):
        card = self.players[player_id].deck(deck_name)[index]
        self.__deal_card(player_id, deck_name, card)

    def end_turn(self, player: deck.Player):
        player_id = player.id
        if player_id != self.whose_turn:
            raise NotYourTurnError('Wrong player.')
        if self.__check_end(player_id):
            print(self.players.winner)
            exit()
        self.draw_cards(self.players.current_id)
        if (self.discard_pile.empty or self.discard_pile.last.special) and self.phase != 'start':
            return False
        self.players.next()
        return True

    @property
    def game_status(self) -> Dict:
        last_card = self.discard_pile.last if not self.discard_pile.empty else None
        return {'player': self.players[self.players.current_id],
                'last_card': last_card,
                'phase': self.phase,
                'game_started': self.game_started
                }

    def make_move(self):
        player = self.players.current_player
        return player.make_move(self.game_status, self.end_turn)

    @property
    def whose_turn(self) -> int:
        return self.players.current_id

    def start(self):
        self.__create_decks()
        self.__create_special_cards()
        self.players.reset()
        self.dealer = Deck()
        self.discard_pile = Deck()
        self.dealer.new_deck().shuffle()
        self.__split_cards()
        self.game_started = True
        self.phase = 'start'
        # self.players.current_player.make_move()

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

    def __can_deal_card(self, card: Card, raise_=False) -> bool:
        if card >= self.discard_pile.last or card.special:
            return True
        if raise_:
            raise CantDealCardError('Can\'t deal the card.')
        return False

    def __can_deal_deck(self, player_deck: Deck) -> bool:
        for card in player_deck:
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

    def __create_decks(self):
        self.players.create_deck('up_deck', show_name='Up deck', hidden=False, max_cards=3, can_draw=False)
        self.players.create_deck('down_deck', show_name='Down deck', hidden=True, max_cards=3, can_draw=False)

    def __create_special_cards(self):
        cards = []
        for suit in Deck().suits:
            cards.append(Card(value='2', suit=suit, points=0, special=True))
            cards.append(Card(value='10', suit=suit, points=0, special=True))
        self.dealer.set_special_cards(cards)

    def __deal_card(self, player_id: int, deck_name: str, card: Card) -> bool:
        player_deck = self.players[player_id].deck(deck_name)
        self.__can_deal_card(card, raise_=True)
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
