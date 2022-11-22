from deck import Deck


class Player:

    def __init__(self, nick='', computer=True):
        self.nick = nick
        self.computer = computer
        self.points = 0
        self.hand_deck = Deck()
        self.deck_settings = {'hand_deck': {'hidden': False,
                                            'name': 'Hand'}}

    def add_deck(self, name, hidden=False):
        if name in self.deck_settings:
            raise AttributeError('Deck alredy exists')
        self.__setattr__(name, Deck())
        self.deck_settings[name] = {'hidden': hidden}

    def print_hand(self):
        for deck in self.deck_settings.keys():
            if self.deck_settings[deck]['hidden']:
                continue
            deck_name = self.deck_settings[deck]['name']
            deck_object = self.__getattribute__(deck)
            print(f'{deck_name}:')
            deck_object.print_all()

    def reset(self):
        for deck in self.deck_settings.keys():
            self.__setattr__(deck, Deck())

    def __repr__(self):
        descr = 'Bot' if self.computer else 'Human'
        return f'({self.nick}, {descr})'
