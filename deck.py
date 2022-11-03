import random


class Card:

	def __init__(self, value, color, points):
		self.value = value
		self.color = color
		self.points = points

	def __lt__(self, other):
		return self.points < other.points

	def __le__(self, other):
		return self.points <= other.points

	def __eq__(self, other):
		return self.points == other.points

	def __ge__(self, other):
		return self.points >= other.points

	def __repr__(self):
		return f'({self.value}, {self.color})'


class Deck:
	
	def __init__(self):
		random.seed()
		self.colors = ['heart', 'diamonds', 'spades', 'clubs']
		self.values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'D', 'K', 'A']
		self.points = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
		self.deck_count = 1
		self.special = []
		self.deck = []
		
	def add(self, card):
		if isinstance(card, Deck):
			self.deck += card.deck
		else:
			self.deck = [card] + self.deck

	@property
	def card(self):
		return self.pop()

	def clear(self):
		self.deck = []
		
	def get(self):
		return self.pop()
		
	def new_deck(self):
		for _ in range(self.deck_count):
			for value in self.values:
				for color in self.colors:
					points = self.points[self.values.index(value)]
					self.deck.append(Card(value, color, points))
		return self
		
	def pop(self):
		return self.deck.pop()
		
	def set(self, decks=1, colors=None, values=None):
		self.colors = colors if colors else self.colors
		self.values = values if values else self.values
		self.deck_count = decks

	@property
	def last(self):
		return self.deck[-1]

	def print_all(self, columns=6):
		for i, card in enumerate(self.deck):
			print(card, end=', ')
			if (i+1) % columns == 0:
				print('')
		print('')
		
	def shuffle(self):
		random.shuffle(self.deck)

	def __add__(self, other):
		self.deck = self.deck + other.deck
		return self

	def __getitem__(self, item):
		return self.deck[item]

	def __iter__(self):
		return self
		
	def __next__(self):
		if self.deck:
			return self.deck.pop()
		else:
			raise StopIteration
			
	def __repr__(self):
		return '\n'.join([str(card) for card in self.deck])
