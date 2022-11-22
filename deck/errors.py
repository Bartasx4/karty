

class DeckException(Exception):
    """ Base exception class for deck. """


class NotACardError(DeckException):
    """ The object is not a Card. """


class NoCardsError(DeckException):
    """ No more cards in deck. """


class CardNotFoundError(DeckException):
    """ File not found. """
