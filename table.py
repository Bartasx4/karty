import random
from deck import Deck
from player import Player


class Table:

    def __init__(self, bot_count=3):
        points = [0, 3, 4, 5, 6, 7, 8, 9, 0, 11, 12, 13, 14]
        self.phase = 'start'  # start, main, end
        Deck().SPECIAL['values'] = ['2', '10']
        self.players = {}
        self.turn_id = 0
        self.bot_count = bot_count
        self.dealer = Deck()
        self.game_started = False
        self.table = Deck()
        self.special = Deck()
        self.special.set(values=['2', '10'])
        self.special.new_deck()
        self.dealer.set(points=points)
       
    def create_player(self, nick):
        id_ = len(self.players)
        self.players[id_] = Player(nick, False)
        
    def game_status(self):
        return {'turn_id': self.turn_id,
        			 'phase': self.phase,
        			 'game_started': self.game_started
        			 }
        
    def next_player(self):
    	if not self.game_started:
    		return
    	...
    	
    	if self.__check_win():
    		self.__end_game()

    def start(self):
        self.turn_id = random.choice(self.players.keys())
        self.__reset_players()
        self.dealer = Deck()
        self.dealer.new_deck().shuffle()
        random.shuffle(self.players)
        self.__split_cards()
        self.game_started = True
        self.phase = 'start'
        
    def take_cards(self, player_id):
    	id_ = player_id
    	while self.players[id_].hand_deck.count > 3 and self.dealer.count > 0:
    		self.players[id_].hand_deck.add(self.dealer.get())
    	return True
    	
    def __can_deal_card(self, card):
    	if card >= self.table.last or card.special:
    		return True
    	return False
    	
    def __can_deal_deck(self, deck):
    	for card in deck:
    		if self.__can_deal_card(card):
    			return True
    		return False

    def __check_win(self):
        for player in self.players:
            empty = [player.hand_deck.count == 0,
                     player.up_deck.count == 0,
                     player.down_deck == 0]
            if all(empty):
                return player
        return False

    def __create_bots(self, bots_count=4):
        for i in range(bots_count):
            id_ = len(self.players)
            bot = Player(nick=f'Bot_{i + 1}', computer=True)
            self.players[id_] = bot

    def __end_game(self):
        self.game_started = False

    def __last_four(self):
        if self.table.count < 4:
            return False
        last_cards = self.table[-4:]
        last_one = self.table.last
        for card in last_cards:
            same = Deck().is_same_dict(card, last_one)['value']
            if not same:
                return False
            self.table.clear()
        return True
        
    def __reset_players(self):
    	for player in self.players:
    		player.reset()

    def __split_cards(self):
        for player in self.players:
            stacks = [player.hand_deck, player.up_deck, player.down_deck]
            for player_deck in stacks:
                for _ in range(3):
                    player_deck.add(self.dealer.get())
