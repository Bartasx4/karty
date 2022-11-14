import random
from deck import Deck
from player import Player


class Table:

    def __init__(self, players=None, bot_count=3):
        values = [0, 3, 4, 5, 6, 7, 8, 9, 0, 11, 12, 13, 14]
        self.phase = 'start'  # start, main, end
        Deck().SPECIAL['values'] = ['2', '10']
        self.players: list[Player] = players if players else []
        self.__create_players(bot_count)
        self.dealer = Deck()
        self.table = Deck()
        self.special = Deck()
        self.special.set(values=['2', '10'])
        self.special.new_deck()
        self.dealer.set(values=values)

    def start(self):
        self.dealer = Deck()
        self.dealer.new_deck().shuffle()
        random.shuffle(self.players)
        self.__split_cards()
        self.__start_phase()
        self.__game_loop()

    def __check_win(self):
        for player in self.players:
            empty = [player.hand_deck.count == 0,
                     player.up_deck.count == 0,
                     player.down_deck == 0]
            if all(empty):
                return player
        return False

    def __create_players(self, bots_count=4):
        for player in self.players:
            player.table = self
        for i in range(bots_count):
            bot = Player(table=self, nick=f'Bot_{i + 1}', computer=True)
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
                    player_deck.add(self.dealer.get())

    def __start_phase(self):
        self.phase = 'start'
        for player in self.players:
            player.move()
        self.phase = 'main'
