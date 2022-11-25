

class DeckException(Exception):
    """ Base exception class for deck. """


class PlayerException(Exception):
    """ Base exception class for player. """


class RulesException(Exception):
    """ Base exception class for rules error. """


class CantDealCardError(RulesException):
    """ Can't deal card. """


class CardNotFoundError(DeckException):
    """ File not found. """


class DeckIndexError(DeckException):
    """ Index out of range """


class DeckIsEmptyError(DeckException):
    """ Try draw card when deck is empty """


class NoMoreCardsError(PlayerException):
    """ Player have not more cards in that deck. """


class NotACardError(DeckException):
    """ The object is not a Card. """


class NotDrawableDeck(PlayerException):
    """ Player can't draw to this deck. """


class TooManyCardsError(PlayerException):
    """ Player can't draw more cards. """


class WrongDeckName(PlayerException):
    """ Wrong name of player's deck. """
