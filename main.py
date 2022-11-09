from vandtia import Vandtia

if __name__ == '__main__':
    game = Vandtia()
    # game.start()
    # print(game.players[0].hand_deck)
    from deck import Deck
    from deck import Card
    test = Deck()
    test.new_deck()
    test.create_table()
    print(test.last)
    test.get_card(test.last)
    print(test.last)
    