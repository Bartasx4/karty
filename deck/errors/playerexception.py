class PlayerException(Exception):
    """ Base exception class for player. """


class MaxCardsError(PlayerException):
    """ Player has the maximum number of cards. """


class NoMoreCardsError(PlayerException):
    """ Player have not more cards in that deck. """


class NotDrawableDeckError(PlayerException):
    """ Player can't draw to this deck. """


class PlayerAlreadyFinishedError(PlayerException):
    """ The player has already finished the game. """


class PlayerDoesNotExist(PlayerException):
    """ The player does not exist. """


class TooManyCardsError(PlayerException):
    """ Player can't draw more cards. """


class WrongDeckNameError(PlayerException):
    """ Wrong name of player's deck. """
