from deck import Player
from deck import Card
from typing import Dict
import os


clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')


def make_move(game_status: Dict, end_turn):
    player: Player
    last_card: Card
    phase: str
    started: bool
    player, last_card, phase, started = game_status.values()
    if not started:
        return False
    if phase == 'start':
        swap_cards(player)
        end_turn(game_status['player'])
        return True
    main_game(player, last_card)


def main_game(player: Player, last_card: Card):
    pass


def swap_cards(player: Player):
    while True:
        print(player)
        player.print_hand()
        print('Do you want to swap cards?')
        print('Enter two numbers separated by a comma.')
        print('The first number is the card in your hand, the second number is the board card.')
        print('Press enter if you don\'t want to swap.')
        choice = input().strip()
        if choice == '':
            break
        card1_id, card2_id = choice.split(',')
        card1_id = int(card1_id)
        card2_id = int(card2_id)
        player.swap_cards_by_id('hand_deck', 'up_deck', card1_id-1, card2_id-1)
        # clear()
