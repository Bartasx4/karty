#pylint:disable=R0913
from .player import Player
from typing import Dict
from typing import List
from random import shuffle
from random import choice


class PlayersGroup:
	
	def __init__(self):
		self._players: Dict[Player] = {}
		self._winner: List[int] = []
		self._current_turn: int = None
		self._custom_decks = []
	
	def add_player(self, nick: str, computer = True):
		id_ = len(self._players)
		self._players[id_] = Player(nick, computer)
		self.__shuffle()
		self.__create_decks()
		self._winner = [-1 for _ in self._players]
		
	def create_deck(self, name: str, max_cards: int, show_name: str, can_draw= True, hidden=False):
		self._custom_decks.append([name, max_cards, show_name, can_draw, hidden])
		self.__create_decks()
	
	@property	
	def current(self):
		return self._current_turn
		
	def loser(self, player_id: int):
		if player_id in self._winner:
			raise Exception
		for index, _ in enumerate(self._winner):
			new_index = -(index+1)
			if self._winner[new_index] == -1:
				self._winner[new_index] = player_id
		
	def next(self) -> int:
		id_ = self._current_turn
		id_ += 1
		if id_ >= len(self._players):
			id_ = 0
		if id_ in self._winner:
			return self.next()
		return self._current_turn
		
	def reset(self):
		for player in self._players:
			player.reset()
		self.__shuffle()
		
	def winner(self, player_id: int):
		if player_id in self._winner:
			raise Exception
		for index, value in enumerate(self._winner):
			if value == -1:
				self._winner[index] = player_id
				break
		
	def __create_decks(self):
		for player in self._players:
			for deck in self._custom_decks:
				player.create_deck(*deck)
		
	def __shuffle(self):
		self._current_turn = choice(list(self._players.keys))
		players_id = list(self._players.keys())
		shuffle(players_id)
		
		new_list = {}
		for id_ in players_id:
			new_list[id_] = self._players[id_]
		self._players = new_list

	def __getitem__(self, index):
		return self._players[index]
		
	def __iter__(self):
		return self._players.__iter__()
