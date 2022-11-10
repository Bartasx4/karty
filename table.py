import random
from deck import Deck
from player import Player


class Table:

    def __init__(self):
        values = [0, 3, 4, 5, 6, 7, 8, 9, 0, 11, 12, 13, 14]
        self.players = []
        self.deck = Deck()
        self.table = Deck()
        self.special = Deck()
        self.special.set(values=['2', '10'])
        self.special.new_deck()
        self.deck.set(values=values)

    def start(self, players=None, bot_count=3):
        self.deck = Deck()
        self.deck.new_deck().shuffle()
        players = players if players else []
        self.__create_players(bot_count)
        self.players += players
        random.shuffle(self.players)
        self.__split_cards()
        self.__game_loop()

    def __check_win(self):
        for player in self.players:
            empty = [player.hand_deck.count == 0,
                     player.up_deck.count == 0,
                     player.down_deck == 0]
            if all(empty):
                return player
        return False

    def __create_players(self, players_count):
        self.players = []
        human = Player(dealer_deck=self.deck, table_deck=self.table, nick='Bartek', computer=False)
        self.players.append(human)
        for i in range(players_count):
            bot = Player(dealer_deck=self.deck, table_deck=self.table, nick=f'{i + 1}', computer=True)
            self.players.append(bot)

    def __end_game(self):
        pass

    def __game_loop(self):
        for player in self.players:
            while player.move():
                if self.__check_win():
                    return self.__end_game()

    def __last_four(self):
        if self.table.count < 4:
            return False
        last_cards = self.table[-4:]
        last_one = self.table.last
        for card in last_cards:
            same = Deck().is_same_dict(card, last_one)['value']
            if not same:
                return False
        return True

    def __split_cards(self):
        for player in self.players:
            stacks = [player.hand_deck, player.up_deck, player.down_deck]
            for player_deck in stacks:
                for _ in range(3):
                    player_deck.add(self.deck.get())

    def __start_phase(self):
        pass
