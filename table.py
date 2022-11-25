import random
from typing import Dict
from deck import Card
from deck import Deck
from deck import Player
from deck import CantDealCardError
from deck.deck import is_same_dict


class Table:

    def __init__(self):
        points = [0, 3, 4, 5, 6, 7, 8, 9, 0, 11, 12, 13, 14]
        self.players: Dict[int:Player] = {}
        self.phase = 'start'  # start, main, end
        self.turn_id = 0
        self.game_started = False
        self.dealer = Deck()
        self.discard_pile = Deck()
        self.dealer.set(points=points)
        self.__create_special_cards()

    def add_player(self, nick: str, computer=True):
        id_ = len(self.players)
        self.players[id_] = Player(nick, computer=computer)
        self.players[id_].create_deck('up_deck', hidden=False, max_cards=3, can_draw=False)
        self.players[id_].create_deck('down_deck', hidden=True, max_cards=3, can_draw=False)

    def create_bots(self, bots_count=4):
        for i in range(bots_count):
            self.add_player(f'Bot_{i + 1}')

    def deal_card(self, player_id: int, deck_name: str, card: Card):
        self.__deal_card(player_id, deck_name, card)

    def deal_card_by_id(self, player_id: int, deck_name: str, index: int):
        card = self.players[player_id].get_deck(deck_name)[index]
        self.__deal_card(player_id, deck_name, card)

    def end_turn(self):
        self.__check()
        self.turn_id += 1
        if self.turn_id >= len(self.players):
            self.turn_id = 0

    @property
    def game_status(self) -> Dict[str, str]:
        return {'turn_id': self.turn_id,
                'phase': self.phase,
                'game_started': self.game_started
                }

    @property
    def whose_turn(self) -> int:
        return self.turn_id

    def start(self):
        self.turn_id = random.choice(list(self.players.keys()))
        self.__reset_players()
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

    def __check_win(self) -> bool:
        for id_, player in self.players.items():
            empty = [player.hand_deck.count == 0,
                     player.up_deck.count == 0,
                     player.down_deck == 0]
            if all(empty):
                return id_
        return False

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
        self.discard_pile.add(player_deck.draw_by_card(card))
        return True

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

    def __reset_players(self):
        for player in self.players.values():
            player.reset()

    def __split_cards(self):
        for player in self.players.values():
            stacks = [player.hand_deck, player.up_deck, player.down_deck]
            for player_deck in stacks:
                for _ in range(3):
                    player_deck.add_card(self.dealer.draw())
