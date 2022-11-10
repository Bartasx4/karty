import random


class Card:

    def __init__(self, value: str, color: str, points: int):
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
        self.points = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.deck_count = 1
        self.special = []
        self.deck = []

    def add(self, to_add):
        if isinstance(to_add, Deck):
            self.deck += to_add.deck
        else:
            self.deck = [to_add] + self.deck

    def check_lowest_card(self):
        lowest = 99
        lowest_deck = Deck()
        for card in self.deck:
            lowest = card.points if card.points < lowest else lowest
        for card in self.deck:
            if card.points == lowest:
                lowest_deck.add(card)
        return lowest_deck

    def clear(self):
        self.deck = []

    @property
    def count(self) -> int:
        return int(len(self.deck))

    def create_stack(self, name):
        self.__setattr__(name, Deck())

    @property
    def empty(self):
        if self.count > 0:
            return False
        return True

    @property
    def first(self):
        if not self.empty:
            return self.deck[0]
        raise IndexError("Can't get a first card. The deck is empty.")

    def get(self, index=-1):
        return self.pop(index)

    def get_card(self, card_to_find: Card):
        for index, card_deck in enumerate(self.deck):
            if self.is_same(card_deck, card_to_find):
                return self.pop(index)
        return False

    def get_card_by_value(self, card_to_find):
        for index, card_deck in enumerate(self.deck):
            if self.is_same_dict(card_deck, card_to_find)['value']:
                return self.pop(index)
        return False

    def new_deck(self):
        for _ in range(self.deck_count):
            for value in self.values:
                for color in self.colors:
                    points = self.points[self.values.index(value)]
                    card = Card(value, color, points)
                    self.deck.append(card)
        return self

    def pop(self, index=-1):
        return self.deck.pop(index)

    def set(self, decks=1, colors=None, values=None, points=None):
        self.colors = colors if colors else self.colors
        self.values = values if values else self.values
        self.points = points if points else self.points
        self.deck_count = decks

    @property
    def last(self) -> Card:
        if not self.empty:
            return self.deck[-1]
        raise Exception("Can't get a last card. The deck is empty.")

    def print_all(self, columns=6):
        for i, card in enumerate(self.deck):
            print(card, end=', ')
            if (i + 1) % columns == 0:
                print('')
        print('')

    def shuffle(self):
        random.shuffle(self.deck)

    def sort(self, format_):
        pass

    def is_same_dict(self, card1: Card, card2: Card):
        result = {'value': card1.value == card2.value,
                  'color': card1.color == card2.color,
                  'points': card1.points == card2.points}
        return result

    def is_same(self, card1, card2):
        is_same = self.is_same_dict(card1, card2)
        if all([is_same['value'], is_same['color'], is_same['points']]):
            return True
        return False

    def __add__(self, other):
        self.deck = self.deck + other.deck
        return self

    def __getitem__(self, index):
        return self.deck[index]

    def __iter__(self):
        return self.deck.__iter__()

    def __next__(self):
        pass
        # return self.deck.__next__()

# def __repr__(self):
# return '\n'.join([str(card) for card in self.deck])
