from deck import Player
from deck import Card
from deck import Deck
from typing import Dict


class AI:
    end_turn = None

    @classmethod
    def make_move(cls, game_status: Dict, next_turn):
        player: Player
        last_card: Card
        phase: str
        started: bool
        player, last_card, phase, started = game_status.values()
        if not started:
            return False
        if phase == 'start':
            cls.swap_cards(player)
            next_turn(game_status['player'])
            return True

    @classmethod
    def swap_cards(cls, player: Player):
        hand_deck: Deck = player.hand_deck
        up_deck: Deck = player.up_deck
        for hand_index, hand_card in enumerate(hand_deck):
            for up_index, up_card in enumerate(up_deck):
                if hand_card > up_card or (hand_card.special and not up_card.special):
                    player.swap_cards_by_id(deck_name1='hand_deck',
                                            deck_name2='up_deck',
                                            card1_id=hand_index,
                                            card2_id=up_index)
                    return cls.swap_cards(player)
