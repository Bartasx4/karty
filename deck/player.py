from deck import Deck
from .errors import TooManyCardsError
from .errors import NotDrawableDeck
from .errors import WrongDeckName


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
        player_deck: Deck = self.get_deck(player_deck_name)
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

    def get_deck(self, deck_name: str):
        if deck_name not in self._deck_settings:
            raise WrongDeckName('Player %s dosn\'t have deck with name %s', self.nick, deck_name)
        # if not self._deck_settings[deck_name]['can-draw']:
            # raise NotDrawableDeck('Can\'t draw to deck %s.', deck_name)
        # if self._deck_settings[deck_name]['max-cards'] <= self.__getattribute__(deck_name).count:
            # raise TooManyCardsError('Player can\'t draw more cards.')
        return self.__getattribute__(deck_name)

    def __repr__(self):
        descr = 'Bot' if self.computer else 'Human'
        return f'({self.nick}, {descr})'
