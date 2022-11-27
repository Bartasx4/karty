from deck import Deck
from deck import Card
from .errors import TooManyCardsError
from .errors import NotDrawableDeckError
from .errors import WrongDeckNameError
from .errors import CardNotFoundError


class Player:

    def __init__(self, nick='', computer=True):
        self.nick = nick
        self.computer = computer
        self.points = 0
        self.hand_deck = Deck()
        self._deck_settings = {'hand_deck': {'hidden': False,
                                             'name': 'Hand',
                                             'max-cards': 3,
                                             'can-draw': True
                                             }
                               }

    def create_deck(self, name: str, max_cards: int, show_name: str = '', can_draw=True, hidden=False):
        self.__setattr__(name, Deck())
        show_name = show_name if show_name else name
        self._deck_settings[name] = {'hidden': hidden,
                                     'name': name,
                                     'max-cards': max_cards,
                                     'can-draw': can_draw}

    def draw_card(self, player_deck_name: str, dealer_deck: Deck):
        player_deck: Deck = self.deck(player_deck_name)
        player_deck.add_card(dealer_deck.draw())

    def print_hand(self):
        for deck in self._deck_settings.keys():
            if self._deck_settings[deck]['hidden']:
                continue
            deck_name = self._deck_settings[deck]['name']
            deck_object = self.__getattribute__(deck)
            print(f'\n{deck_name}:')
            deck_object.print_all()

    def reset(self):
        for deck in self._deck_settings.keys():
            self.__setattr__(deck, Deck())
            
    def swap_cards(self, deck_name1:str, deck_name2: str, card1: Card, card2:Card):
            self.__swap_cards(deck_name1, deck_name2, card1, card2)
            
    def swap_cards_by_id(self, deck_name1: str, deck_name2: str, card1: int, card2: int):
            pass
            
    def __swap_cards(self, deck_name1: str, deck_name2: str, card1: Card, card2: Card):
    	if deck_name1 not in self._deck_settings or deck_name2 not in self._deck_settings:
    		raise WrongDeckNameError
    	if card1 not in self.deck(deck_name1) or card2 not in self.deck(deck_name2):
    		raise CardNotFoundError
    	swap_card1 = self.deck(deck_name1).draw(card1)
    	swap_card2 = self.deck(deck_name2).draw(card2)
    	self.deck(deck_name1).add(swap_card2)
    	self.deck(deck_name2).add(swap_card1)

    def deck(self, deck_name: str):
        if deck_name not in self._deck_settings:
            raise WrongDeckNameError('Player %s dosn\'t have deck with name %s', self.nick, deck_name)
        # if not self._deck_settings[deck_name]['can-draw']:
            # raise NotDrawableDeck('Can\'t draw to deck %s.', deck_name)
        # if self._deck_settings[deck_name]['max-cards'] <= self.__getattribute__(deck_name).count:
            # raise TooManyCardsError('Player can\'t draw more cards.')
        return self.__getattribute__(deck_name)

    def __repr__(self):
        descr = 'Bot' if self.computer else 'Human'
        return f'({self.nick}, {descr})'
