import random
from deck import Deck
from deck import Card
from player import Player


class Table:

    def __init__(self, bot_count=3):
        points = [0, 3, 4, 5, 6, 7, 8, 9, 0, 11, 12, 13, 14]
        self.phase = 'start'  # start, main, end
        self.players = {}
        self.turn_id = 0
        self.bot_count = bot_count
        self.dealer = Deck()
        self.__create_special_cards()
        self.game_started = False
        self.table = Deck()
        self.dealer.set(points=points)

    def create_player(self, nick):
        id_ = len(self.players)
        self.players[id_] = Player(nick, False)

    def game_status(self):
        return {'turn_id': self.turn_id,
                'phase': self.phase,
                'game_started': self.game_started
                }

    @property
    def whose_turn(self):
        return self.turn_id

    def start(self):
        self.turn_id = random.choice(list(self.players.keys()))
        self.__reset_players()
        self.dealer = Deck()
        self.dealer.new_deck().shuffle()
        self.__split_cards()
        self.game_started = True
        self.phase = 'start'

    def take_cards(self, player_id):
        id_ = player_id
        while self.players[id_].hand_deck.count > 3 and self.dealer.count > 0:
            self.players[id_].hand_deck.add(self.dealer.draw())
        return True

    def put_card(self, put_card):
        if isinstance(put_card, Card):
            put_card = [put_card]



    def swap_card(self, player_id, hand_card: Card, up_card: Card):
        player = self.players[player_id]
        player.hand_deck.add(player.up_deck.get_by_card(up_card))
        player.up_deck.add(player.hand_deck.get_by_card(hand_card))

    def __can_deal_card(self, card) -> bool:
        if card >= self.table.last or card.special:
            return True
        return False

    def __can_deal_deck(self, deck: Deck) -> bool:
        for card in deck:
            if self.__can_deal_card(card):
                return True
            return False

    def __check_win(self) -> bool:
        for id_, player in self.players.items():
            empty = [player.hand_deck.count == 0,
                     player.up_deck.count == 0,
                     player.down_deck == 0]
            if all(empty):
                return id_
        return False

    def __create_bots(self, bots_count=4):
        for i in range(bots_count):
            id_ = len(self.players)
            bot = Player(nick=f'Bot_{i + 1}', computer=True)
            self.players[id_] = bot

    def __create_special_cards(self):
        cards = []
        for color in Deck().suits:
            cards.append(Card(value='2', color=color, points=0, special=True))
            cards.append(Card(value='10', color=color, points=0, special=True))
        self.dealer.add_special_cards(cards)

    def __end_game(self):
        self.game_started = False

    def __last_four(self):
        if self.table.count < 4:
            return False
        last_cards = self.table[-4:]
        last_one = self.table.last
        for card in last_cards:
            same = Deck().is_same_dict(card, last_one)['value']
            if not same:
                return False
            self.table.clear()
        return True

    def __reset_players(self):
        for player in self.players.values():
            player.reset()

    def __split_cards(self):
        for player in self.players.values():
            stacks = [player.hand_deck, player.up_deck, player.down_deck]
            for player_deck in stacks:
                for _ in range(3):
                    player_deck.add(self.dealer.draw())
