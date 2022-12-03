from table import Table
import interface
from ai import AI


table = Table()
table.add_player('Bartek', interface.make_move, computer=False)
table.create_bots(AI.make_move, 2)
table.start()
