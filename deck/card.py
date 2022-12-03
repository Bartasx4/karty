#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains the 'Card' class. Each 'Card' instance represents a
single playing card, of a given value and suit.
"""


class Card:
    """The Card class, each instance representing a single playing card.
    You can create your own cards for different games.
    Cards can have custom values and suits.

    Args:
        value (str): A number or character that represents the card.
        suit (str): The suit of card. Default is ♡, ♢, ♠, ♣.
        points (int): Card value. It is used to determine which card is "higher" and which is "lower".
        special (bool): Does this card have a special effect specified in the rules.
    """

    def __init__(self, value: str, suit: str, points: int, special=False):
        self._value = value
        self._suit = suit
        self._points = points
        self._special = special

    @property
    def points(self):
        """int: Card value."""
        return self._points

    @property
    def special(self):
        """bool: Does this card have a special effect specified in the rules."""
        return self._special

    def set_special(self):
        """Make this card special."""
        self._special = True

    @property
    def suit(self):
        """str: The suit of card. Default is ♡, ♢, ♠, ♣."""
        return self._suit

    @property
    def value(self):
        """str: A number or character that represents the card."""
        return self._value

    def unset_special(self):
        """Unmake this card special."""
        self._special = False

    def __lt__(self, other):
        return self.points < other.points

    def __le__(self, other):
        return self.points <= other.points

    def __eq__(self, other):
        return self.points == other.points

    def __ne__(self, other):
        return self.points != other.points

    def __ge__(self, other):
        return self.points >= other.points

    def __repr__(self):
        return f'({self.value}, {self.suit})'
