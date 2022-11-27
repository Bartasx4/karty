import logging
import random
from typing import List
from .card import Card
from .errors import DeckIsEmptyError
from .errors import DeckIndexError
from .errors import CardNotFoundError

log = logging.getLogger('deck')


class Deck:
    _SPECIALS: List[Card] = []

    def __init__(self):
        random.seed()
        self._points = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self._suits = ['♡', '♢', '♠', '♣']
        self._values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'D', 'K', 'A']
        self._deck_count = 1
        self._deck: List[Card] = []
        self._discard_pile: List[Card] = []

    def add_card(self, card: Card):
        self._deck = [card] + self._deck

    def add_deck(self, deck):
        self._deck = self._deck + deck.deck

    def clear(self):
	    self._deck = []

    @property
    def count(self) -> int:
        return int(len(self.deck))

    @property
    def deck(self):
        return self._deck

    @property
    def discard_pile(self) -> List[Card]:
        return self._discard_pile

    def draw(self, index=0) -> Card:
        return self.__pop(index)

    def draw_by_card(self, card: Card) -> Card:
        for index, card_deck in enumerate(self.deck):
            if is_same(card_deck, card):
                return self.__pop(index)
        raise CardNotFoundError('Card not found {card=}.')

    @property
    def empty(self) -> bool:
        if self.count > 0:
            return False
        return True
        
    def find(self, value: str = None, suit: str = None, points: int = None, special: bool = None, draw=False) -> List[Card]:
    	found = []
    	for index, card in enumerate(self.deck):
    		if value:
    			if card.value != value:
    				continue
    		if suit:
    			if card.suit != suit:
    				continue
    		if points:
    			if card.points != points:
    				continue
    		if special != None:
    			if card.special != special:
    				continue
    		if draw:
    			found.append(self.draw(index))
    		else:
    		    found.append(card)
    	return found

    def set_special_cards(self, cards: List[Card] or object):
        if isinstance(cards, list):
            self._SPECIALS = cards
        elif isinstance(cards, Deck):
            self._SPECIALS = [card for card in self.deck]

    @property
    def last(self) -> Card:
        if self.empty:
            raise DeckIsEmptyError('Deck is empty.')
        return self.deck[0]

    def new_deck(self):
        self.__new_deck()
        return self

    def print_all(self, columns=6):
        for i, card in enumerate(self.deck):
            print(card, end=', ')
            if (i + 1) % columns == 0:
                print('')
        print('')

    def set(self, decks=1,
            colors: List[str] = None,
            values: List[str] = None,
            points: List[int] = None,
            specials: List[str] = None
            ):
        self._suits = colors if colors else self._suits
        self._values = values if values else self._values
        self._points = points if points else self._points
        self._SPECIALS = specials if specials else []
        self._deck_count = decks

    def shuffle(self):
        random.shuffle(self.deck)

    @property
    def suits(self) -> List[str]:
        return self._suits

    def __new_deck(self):
        for _ in range(self._deck_count):
            for value in self._values:
                for color in self._suits:
                    points = self._points[self._values.index(value)]
                    card = Card(value, color, points)
                    if self.__is_special(card):
                        card.set_special()
                    self.deck.append(card)

    def __is_special(self, special_card: Card) -> bool:
        for card in self._SPECIALS:
            compare = is_same_dict(special_card, card)
            if compare['color'] and compare['value']:
                return True
        return False

    def __pop(self, index=0):
        if self.empty:
            raise DeckIsEmptyError('Deck is empty.')
        if index not in range(self.count):
            raise DeckIndexError('deck index out of range')
        return self._deck.pop(index)

    def __add__(self, other):
        self._deck = self.deck + other.dealer
        return self

    def __contains__(self, card):
        self._deck.__contains__()

    def __delitem__(self, indice):
        pass

    def __get__(self, instance, owner):
        return False

    def __getitem__(self, index):
        return self.deck[index]

    def __iter__(self):
        return self.deck.__iter__()

    def __len__(self):
        return self.count

    def __repr__(self):
        return str(self.deck)


def is_same(card1: Card, card2: Card) -> bool:
    is_same_ = is_same_dict(card1, card2)
    if all([is_same_['value'], is_same_['color'], is_same_['points']]):
        return True
    return False


def is_same_dict(card1: Card, card2: Card) -> dict[str:bool]:
    result = {'value': card1.value == card2.value,
              'color': card1.suit == card2.suit,
              'points': card1.points == card2.points}
    return result
