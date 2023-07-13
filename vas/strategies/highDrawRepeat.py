from strategies.baseStategy import BaseStategy


class HighDrawRepeat(BaseStategy):
    async def run(self):
        print('')

    async def run(self):
        message = await self.receive(timeout=10)
        if message:
            print(f"{self.agent.name}: Received message: {message}")
        else:
            print(f"{self.agent.name}: No message received.")