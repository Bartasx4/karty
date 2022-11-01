from deck import Deck
from player import Player


if __name__ == '__main__':
    deck = Deck()
    deck.new_deck().shuffle()
    player_1 = Player(id_=1, nick='Bartek', computer=False)
    player_2 = Player(id_=2, nick='Noob', computer=True)

    for player in [player_1, player_2]:
        for player_deck in [player.hand_deck, player.down_deck, player.up_deck]:
            for i in range(3):
                player_deck.add(deck.get())

    player_1.hand()
    player_1.hand_deck.add(player_1.up_deck)
    player_1.up_deck.clear()
    player_1.hand()
