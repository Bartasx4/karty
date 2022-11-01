#pylint:disable=R1705
import random


class Deck:
	
	def __init__(self):
		random.seed()
		self.colors = ['heart', 'diamonds', 'spades', 'clubs']
		self.values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'D', 'K', 'A']
		self.deck_count = 1
		self.special = []
		self.deck = []
		
	def add(self, card):
		self.deck = [card] + self.deck
		
	def get(self):
		return self.pop()
		
	def new_deck(self):
		self.deck = [(value, color) for _ in range(self.deck_count) for value in self.values for color in self.colors]
		
	def pop(self):
		return self.deck.pop()
		
	def set(self, decks=1, colors=None, values=None):
		self.colors = colors if colors else self.colors
		self.values = values if values else self.values
		self.deck_count = decks
		
	def shuffle(self):
		random.shuffle(self.deck)
		
	def __exit__(self, exception_type, exception_value, traceback):
		print('Exit')
		
	def __iter__(self):
		return self
		
	def __next__(self):
		if self.deck:
			return self.deck.pop()
		else:
			raise StopIteration
			
	def __repr__(self):
		return '\n'.join([str(card) for card in self.deck])
	
			
if __name__ == '__main__':
	d = Deck()
	d.set(decks=1, values=[2], colors=['S', 'D', 'P', 'K'])
	d.new_deck()
	d.add(('A', 'S'))
	d.shuffle()
	print(d)
