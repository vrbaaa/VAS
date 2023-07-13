from strategies.baseStategy import BaseStategy
from spade.behaviour import CyclicBehaviour


class OptimalDraw(CyclicBehaviour):
    async def on_start(self):
        print('Optimal Draw')
    
    async def run(self):
        message = await self.receive(timeout=1)
        if message:
            print(f"{self.agent.name}: Received message: {message}")
        else:
            print(f"{self.agent.name}: No message received.")