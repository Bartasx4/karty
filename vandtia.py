from deck import Deck
from player import Player


class Vandtia:

    def __init__(self, ):
        self.players_count = 4
        self.rounds = 1
        self.players = []
        self.deck = Deck()

    def start(self, players=4, rounds=1):
        self.players_count = players
        self.rounds = rounds
        self.deck.new_deck().shuffle()
        self.players.append(Player(nick='Bartek', computer=False))
        for i in range(players-1):
            self.players.append(Player(nick='', computer=True))
        for player in self.players:
            for player_deck in [player.hand_deck, player.up_deck, player.down_deck]:
                for card in range(3):
                    player_deck.add(self.deck.card)
        self.__game_loop()

    def __game_loop(self):
        while not self.__win_check():
            for player in self.players:
                pass

    def __set_attr(self):
        pass

    def __win_check(self):
        return False

    def __move(self):
        pass
