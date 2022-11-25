

class Card:

    def __init__(self, value: str, color: str, points: int, special=True):
        self.value = value
        self.suit = color
        self.points = points
        self._special = special

    def set_special(self):
        self._special = True

    @property
    def special(self):
        return self._special

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
