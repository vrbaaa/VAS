from spade.agent import Agent
from strategies.baseStategy import BaseStategy
from player import Player
from strategies.randomDraw import RandomDraw
from spade.behaviour import CyclicBehaviour

class GameAgentt(Agent):
    def __init__(self, player, order):
        super().__init__(player.name, player.password)
        self.player = player
        self.order = order
        print(f'Bok, ja sam igrač {self.player.get_name()}, krećem { "prvi" if order == 1 else "drugi"}' )
        print( 'Ovo su moje karte: ')
        for card in self.player.get_cards():
            print(card.get_visual())
        
    async def setup(self):
        print('dodano ponasanje')
        self.add_behaviour(self.player.strategy)
