import logging
import random
from typing import List
from deck.card import Card
from deck import DeckIsEmptyError
from deck import DeckIndexError
from deck import CardNotFoundError

log = logging.getLogger(__name__)


class Deck:
    """The Deck class, representing the deck that the cards will be in.

    You can create your own decks and cards for different games.
    Cards can have custom values and suits.
    Values, suits and points are only used when calling new_deck().
    The new_deck() method creates a deck of cards by combining suits and values.
    Cards created in a different way are not checked for the correctness of values and suits.

    Methods:
        add_card(card: Card):
            Add a card to the rest of the cards.
        add_deck(deck):
            Add cards from another deck to the pile of cards.
        clear():
            Clear the pile of cards.
        count() -> int: @Property
            The number of cards in the pile.
        deck() -> List[Card]: @Property
            A pile of cards.
        draw(index: int = 0) -> Card:
            Discard a card with the given index. By default index=0
        draw_by_card(card: Card) -> Card:
            Discard a card by checking with a card.
        empty() -> bool: @Property
            Is the stack empty.
        find(value: str = None, suit: str = None, points: int = None, special: bool = None) -> List[Card]:
            Find a card by giving one or more arguments.
        last(self) -> Card: @Property
            Check the last (or first) card in the pile.
        new_deck() -> deck.__class__:
            Create a deck of cards by combining values and suits. By default, 52 playing cards.
        print_all(columns=6):
            Print all cards in a nicer way.
        set(colors: List[str] = None,
            values: List[str] = None,
            points: List[int] = None,
            specials: List[str] = None
        ) -> object:
            Change the default values for creating cards.
        set_special_cards(cards: List[Card] | deck.__class__):
            Add cards with a special effect.
        shuffle() -> deck.__class__:
            Shuffle the cards.
        suits() -> List[str]: @Property
            Take the suits.
    """
    _SPECIALS: List[Card] = []

    def __init__(self):
        random.seed()
        self._points: List[int] = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self._suits: List[str] = ['♡', '♢', '♠', '♣']
        self._values: List[str] = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'D', 'K', 'A']
        self._deck: List[Card] = []

    def add_card(self, card: Card):
        """Add a card to the pile.
        Args:
            card (Card): The card to be added.
        """
        self._deck = [card] + self._deck

    def add_deck(self, deck):
        """Add cards from another deck to the pile of cards.
        Args:
            deck (Deck): The deck from which the cards will be added.
        """
        self._deck = self._deck + deck.deck

    def clear(self):
        """Clear the pile of cards."""
        self._deck = []

    @property
    def count(self) -> int:
        """The number of cards in the pile.
        Returns:
            int: number of cards in the pile.
        """
        return int(len(self.deck))

    @property
    def deck(self) -> List[Card]:
        """A pile of cards.
        Returns:
            list[Card, ...]: pile (List) with cards.
        """
        return self._deck

    def draw(self, index: int = 0) -> Card:
        """Discard a card with the given index. By default index=0
        Args:
            index (int): The number of the deck slot from which to take the card.
                         By default, the last (or first) card, index=0.
        Returns:
            Card: Card removed from the deck.
        """
        return self.__pop(index)

    def draw_by_card(self, card: Card) -> Card:
        """Discard a card by checking with a card.
        Args:
            card (Card): A card that we take out of the deck.

        Returns:
            Card: Card removed from the deck.

        Raises:
            CardNotFoundError: Card not found.
        """
        for index, card_deck in enumerate(self.deck):
            if is_same(card_deck, card):
                return self.__pop(index)
        raise CardNotFoundError('Card not found {card=}.')

    @property
    def empty(self) -> bool:
        """Is the stack empty.

        Returns:
            bool: True if empty, False otherwise.
        """
        if self.count > 0:
            return False
        return True

    def find(self,
             value: str = None,
             suit: str = None,
             points: int = None,
             special: bool = None
             ) -> List[Card]:
        """Find a card by giving one or more arguments.

        Args:
            value (str): The value of the card we are looking for.
            suit (str): The suit of the card we are looking for.
            points (int): The points of the card we are looking for.
            special (bool): Whether the card you are looking for is a special one.

        Returns:
            List[Card, ...]: List of cards that meet the given criteria.
        """
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
            if special is not None:
                if card.special != special:
                    continue
            else:
                found.append(card)
        return found

    @property
    def last(self) -> Card:
        """Check the last (or first) card in the pile.

        Returns:
            Card: The last (or first) card of the deck.
        """
        if self.empty:
            raise DeckIsEmptyError('Deck is empty.')
        return self.deck[0]

    def new_deck(self) -> deck.__class__:
        """Create a deck of cards by combining values and suits. By default, 52 playing cards.

        Returns:
            Deck: return self
        """
        self.__new_deck()
        return self

    def print_all(self, columns=6):
        """Print all cards in a nicer way.
        Print cards in columns to take up less space in the console.

        Args:
            columns (int): The number of columns to print.
        """
        for i, card in enumerate(self.deck):
            print(card, end=', ')
            if (i + 1) % columns == 0:
                print('')
        print('')

    def set(self,
            suits: List[str] = None,
            values: List[str] = None,
            points: List[int] = None,
            ) -> object:
        """Change the default values for creating cards.

        Args:
            suits (list[str, ...]): Suits used to create a deck of cards.
            values (list[str, ...]): Values used to create a deck of cards.
            points (list[int, ...]): Points used to build a deck of cards.

        Returns:
            Deck: return self.
        """
        self._suits = suits if suits else self._suits
        self._values = values if values else self._values
        self._points = points if points else self._points
        return self

    def set_special_cards(self, cards: List[Card] | deck.__class__):
        """Add cards with a special effect.
        Cards are added to Deck._SPECIALS and used to create
        a new deck of cards by calling the new_deck() method.
        After creating a new deck, the _SPECIAL variable is no longer used.
        The Card class contains information whether the card is special or regular.

        Args:
            cards (list[Cards] | Deck): A list or other deck from which special cards will be added.

        """
        if isinstance(cards, list):
            self._SPECIALS = cards
        elif isinstance(cards, Deck):
            self._SPECIALS = [card for card in self.deck]

    def shuffle(self) -> deck.__class__:
        """Shuffle the cards.

        Returns:
            Deck: return self.
        """
        random.shuffle(self.deck)
        return self

    @property
    def suits(self) -> List[str]:
        """Take the suits.

        Returns:
            list[str, ...]: Suits set in the deck, used to create new cards. Default ♡, ♢, ♠, ♣.
        """
        return self._suits

    def __new_deck(self):
        self._deck = []
        for value in self._values:
            for color in self._suits:
                points = self._points[self._values.index(value)]
                card = Card(value, color, points)
                if self.__is_special(card):
                    card.set_special()
                self._deck.append(card)

    def __is_special(self, card_to_check: Card) -> bool:
        for special_card in self._SPECIALS:
            compare = is_same_dict(card_to_check, special_card)
            if compare['color'] and compare['value']:
                return True
        return False

    def __pop(self, index=0) -> Card:
        if self.empty:
            raise DeckIsEmptyError('Deck is empty.')
        if index not in range(self.count):
            raise DeckIndexError('Ceck index out of range')
        return self._deck.pop(index)

    def __add__(self, other):
        self._deck = self.deck + other.dealer
        return self

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
    if all([is_same_['value'], is_same_['color'], is_same_['_points']]):
        return True
    return False


def is_same_dict(card1: Card, card2: Card) -> dict[str:bool]:
    result = {'value': card1.value == card2.value,
              'color': card1.suit == card2.suit,
              '_points': card1.points == card2.points}
    return result
