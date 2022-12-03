class PlayerWarning(Warning):
    """ Base class for player warnings. """


class DeckAlredyExistWarning(PlayerWarning):
    """ Deck you are creating already exists. """
