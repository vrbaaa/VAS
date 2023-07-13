from spade.agent import Agent
from strategies.baseStategy import BaseStategy
from strategies.highDrawNoRepeat import HighDrawNoRepeat
from player import Player
from strategies.highDrawRepeat import HighDrawRepeat
from strategies.randomDraw import RandomDraw
from spade.behaviour import CyclicBehaviour

class GameAgentt(Agent):
    class RandomDrawaa(CyclicBehaviour):
        async def on_start(self):
            print('Random draw')
    
        async def run(self):
            print('Pokrećem se')
            message = await self.receive()
            if message:
                print(f"{self.agent.name}: Received message: {message}")
            else:
                print(f"{self.agent.name}: No message received.")

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
        self.add_behaviour(self.RandomDrawaa())

class GameAgenttt(Agent):
    class RandomDrawaa(CyclicBehaviour):
        async def on_start(self):
            print('Random draw')
    
        async def run(self):
            print('Pokrećem se')
            message = await self.receive()
            if message:
                print(f"{self.agent.name}: Received message: {message}")
            else:
                print(f"{self.agent.name}: No message received.")

    def __init__(self, player, order):
        super().__init__(player.name, player.password)
        self.player = player
        self.order = order
        print(f'Bok, ja sam igrač {self.player.get_name()}, krećem { "prvi" if order == 1 else "drugi"}' )
        print( 'Ovo su moje karte: ')
        for card in self.player.get_cards():
            print(card.get_visual())
        
    async def setup(self):
        self.add_behaviour(self.RandomDrawaa())
        print('dodano ponasanje')