import random

from .player import Player
from deck import PlayerAlreadyFinishedError
from deck import PlayerDoesNotExist
from typing import Dict
from typing import List
from typing import Tuple
from random import shuffle
from random import choice


class PlayersGroup:

    def __init__(self):
        random.seed()
        self._players: Dict[int:Player] = {}
        self._winner: List[int] = []
        self._current_turn: int = 0
        self._custom_decks: List[Tuple[str, int, str, bool, bool]] = []

    def add_loser(self, player_id: int):
        self.__player_finished(player_id, raise_=True)
        for index, _ in enumerate(self._winner):
            new_index = -(index + 1)
            if self._winner[new_index] == -1:
                self._winner[new_index] = player_id
                break

    def add_player(self, nick: str, interface, computer=True):
        id_ = len(self._players)
        player = Player(nick, interface, id_, computer)
        self._players[id_] = player
        self.__create_decks(players_list=[player])
        self._winner = [-1] * len(self._players)

    def add_winner(self, player_id: int):
        self.__player_finished(player_id, raise_=True)
        for index, value in enumerate(self._winner):
            if value == -1:
                self._winner[index] = player_id
                break

    def create_deck(self, name: str, max_cards: int, show_name: str, can_draw=True, hidden=False):
        deck = (name, max_cards, show_name, can_draw, hidden)
        self._custom_decks.append(deck)
        self.__create_decks(decks_list=[deck])

    @property
    def current_id(self) -> int:
        return self._current_turn

    @property
    def current_player(self) -> Player:
        return self._players[self._current_turn]

    @property
    def ids(self) -> List[int]:
        return list(self._players.keys())

    def next(self) -> int:
        id_ = self._current_turn
        if id_ == -1:
            self._current_turn = random.choice(self.ids)
            return self._current_turn
        id_ += 1
        if id_ >= len(self._players):
            id_ = 0
        if id_ in self._winner:
            return self.next()
        self._current_turn = id_
        return self._current_turn

    def reset(self):
        for player in self._players.values():
            player.reset()

    def shuffle(self):
        self._current_turn = choice(list(self._players.keys()))
        players_id = list(self._players.keys())
        shuffle(players_id)

        new_list = {}
        for id_ in players_id:
            new_list[id_] = self._players[id_]
        self._players = new_list

    @property
    def winner(self):
        return self._winner

    def __create_decks(self,
                       players_list: List[Player] = None,
                       decks_list: List[Tuple[str, int, str, bool, bool]] = None
                       ):
        players_list = players_list if players_list else []
        decks_list = decks_list if decks_list else []
        for player in players_list:
            for deck in self._custom_decks:
                player.create_deck(*deck)
        for deck in decks_list:
            for player in self._players.values():
                player.create_deck(*deck)

    def __player_exist(self, player_id: int, raise_: bool = False) -> bool:
        exist = player_id in self._players
        if not exist and raise_:
            raise PlayerDoesNotExist('The player does not exist.')
        return exist

    def __player_finished(self, player_id: int, raise_: bool = False) -> bool:
        finished = player_id in self._winner
        if finished and raise_:
            raise PlayerAlreadyFinishedError('The player has already finished the game.')
        return finished

    def __getitem__(self, index: int) -> Player:
        self.__player_exist(index, raise_=True)
        return self._players[index]

    def __iter__(self):
        return self._players.values().__iter__()

    def __len__(self) -> int:
        return len(self._players)

    def __repr__(self):
        return str(list(self._players.values()))
