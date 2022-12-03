from deck import Deck
from deck import Card
from deck import WrongDeckNameError
from deck import DeckAlredyExistWarning
from deck import MaxCardsError
import logging
from typing import Iterable
import warnings

log = logging.getLogger(__name__)


class Player:
    """The 'Player' class represents one player (human or computer).
    The 'Player' class includes the name of the player, the cards the player
    has in hand or on the table, the number of points the player has scored.

    Args:
        nick (str): The name that will be displayed.
        interface (objcect): The method that will be called to make the player make his move.
        _id (int): ID of player used by PlayersGroup class.
        computer (bool): Will it be played by a human or a computer.

    Attributes:
        hand_deck (Deck): Cards in hand. The basic deck that contains the player's cards.
        nick (str) Default True: The name that will be displayed.

    Methods:
        make_move():
            Call the method provided in the interface.
        create_deck(name: str, max_cards: int, show_name: str = '', can_draw=True, hidden=False) -> Deck:
            Create a new deck where the player can hold the cards.
        deck(self, deck_name: str) -> Deck:
            Take the deck by name.
        draw_card(player_deck_name: str, dealer_deck: Deck) -> Card:
            Take a card from the dealer and put it in the given deck.
        id() -> int: @Property
            Get player id.
        print_hand():
            Print cards from the deck that are not hidden.
        reset():
            Clear all decks so they are empty.
        swap_cards(deck_name1: str, deck_name2: str, card1: Card, card2: Card):
            Swap cards from two different decks.
        swap_cards_by_id(deck_name1: str, deck_name2: str, card1_id: int, card2_id: int):
            Swap cards from two different decks by id.
    """

    def __init__(self, nick: str, interface, _id: int, computer: bool = True):
        self.hand_deck = Deck()
        self.nick = nick
        self._computer = computer
        self._points = 0
        self._id = _id
        self.make_move = interface
        self._deck_settings = {'hand_deck': {'hidden': False,
                                             'show-name': 'Hand',
                                             'max-cards': 3,
                                             'can-draw': True
                                             }
                               }

    def create_deck(self, name: str, max_cards: int, show_name: str = '', can_draw=True, hidden=False) -> Deck:
        """Create a new deck where the player can hold the cards.
        In various games, the player has one or more extra piles of cards.

        Args:
            name (str): Attribute name for the new deck.
            max_cards (int): Maximum number of cards in the deck.
                Note: There may be more cards in the deck than
                the maximum number if they are added other than from the dealer.
            show_name (str): The name of the deck that will be displayed when the print_hand() method is called
            can_draw (bool): Set whether you can draw cards from the dealer.
            hidden (bool): Set whether the deck will be displayed after the print_hand() method is called.

        Warnings:
            DeckAlredyExistWarning: If deck already exists.

        Returns:
            Deck: Returns the deck that was created.
        """
        if self.__deck_exist(name):
            warnings.warn(DeckAlredyExistWarning('Deck you are creating already exists.'))
        new_deck = Deck()
        self.__setattr__(name, new_deck)
        show_name = show_name if show_name != '' else name.title().replace('_', ' ')
        self._deck_settings[name] = {'hidden': hidden,
                                     'name': name,
                                     'show-name': show_name,
                                     'max-cards': max_cards,
                                     'can-draw': can_draw}
        return new_deck

    def deck(self, deck_name: str) -> Deck:
        """Return the deck with the given name."""
        return self.__get_deck(deck_name)

    def draw_card(self, player_deck_name: str, dealer_deck: Deck) -> Card:
        """Take a card from the dealer and add it to the chosen deck.

        Args:
            player_deck_name (str): The name of the deck to add the card to.
            dealer_deck (Deck): The dealer's deck from which to take a card.

        Returns:
            Card: Card taken by the player.

        Raises:
            MaxCardsError: If deck has the maximum number of cards.
        """
        player_deck: Deck = self.deck(player_deck_name)
        if player_deck.count >= self._deck_settings[player_deck_name]['max-cards']:
            raise MaxCardsError('Player has the maximum number of cards.')
        card = dealer_deck.draw()
        player_deck.add_card(card)
        return card

    @property
    def id(self) -> int:
        """Get id.
        Returns:
            int: ID.
        """
        return self._id

    def print_hand(self):
        """Display all cards in a deck with attribute hidden=False"""
        for deck in self._deck_settings.keys():
            if self._deck_settings[deck]['hidden']:
                continue
            deck_name = self._deck_settings[deck]['show-name']
            deck_object = self.__getattribute__(deck)
            print(f'\n{deck_name}:')
            deck_object.print_all()
        print('')

    def reset(self):
        """Recreate all decks to clear them."""
        for deck in self._deck_settings.keys():
            self.__setattr__(deck, Deck())

    def swap_cards(self, deck_name1: str, deck_name2: str, card1: Card, card2: Card):
        """Swap cards from two different decks.

        Args:
            deck_name1 (str): The name of the first deck.
            deck_name2 (str): The name of the second deck.
            card1 (Card): A card to swap from the first deck.
            card2 (Card): A card to swap from the second deck.
        Note:
            card1 must be from deck named deck_name1 and
            card2 must be from deck named deck_name2.
            card1 will be added to the deck named deck_name2 and
            card2 will be added to the deck named deck_name1
        """
        self.__swap_cards(deck_name1, deck_name2, card1, card2)

    def swap_cards_by_id(self, deck_name1: str, deck_name2: str, card1_id: int, card2_id: int):
        """Swap cards from two different decks.
        Cards are identified by their deck index.

        Args:
            deck_name1 (str): The name of the first deck.
            deck_name2 (str): The name of the second deck.
            card1_id (int): A card id to swap from the first deck.
            card2_id (int): A card id to swap from the second deck.
        """
        card1 = self.deck(deck_name1)[card1_id]
        card2 = self.deck(deck_name2)[card2_id]
        self.__swap_cards(deck_name1, deck_name2, card1, card2)

    def __deck_exist(self, deck_name: str | Iterable, raise_: bool = False) -> bool:
        decks_list = []
        if isinstance(deck_name, str):
            decks_list.append(deck_name)
        else:
            decks_list = deck_name
        deck_exist = []
        for deck_to_check in decks_list:
            exist = deck_to_check in list(self._deck_settings.keys())
            if not exist and raise_:
                raise WrongDeckNameError('Player %s doesn\'t have a deck with name %s.', self.nick, deck_to_check)
            deck_exist.append(exist)
        return all(deck_exist)

    def __get_deck(self, deck_name) -> Deck:
        self.__deck_exist(deck_name, raise_=True)
        return self.__getattribute__(deck_name)

    def __swap_cards(self, deck_name1: str, deck_name2: str, card1: Card, card2: Card):
        swap_card1 = self.deck(deck_name1).draw_by_card(card1)
        swap_card2 = self.deck(deck_name2).draw_by_card(card2)
        self.deck(deck_name1).add_card(swap_card2)
        self.deck(deck_name2).add_card(swap_card1)

    def __getitem__(self, item: str):
        if isinstance(item, str):
            return self.__get_deck(item)
        raise TypeError(f'Expected str but get {type(item)}.')

    def __repr__(self):
        descr = 'Bot' if self._computer else 'Human'
        return f'({self.nick}, {descr})'
