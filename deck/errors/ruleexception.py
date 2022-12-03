class RulesException(Exception):
    """ Base exception class for rules error. """


class CantDealCardError(RulesException):
    """ Can't deal card. """


class NotYourTurnError(RulesException):
    """ Another player turn. """
