class DeckException(Exception):
    """ Base exception class for deck. """


class CardNotFoundError(DeckException):
    """ File not found. """


class DeckIndexError(DeckException):
    """ Index out of range """


class DeckIsEmptyError(DeckException):
    """ Try draw card when deck is empty """


class NotACardError(DeckException):
    """ The object is not a Card. """
