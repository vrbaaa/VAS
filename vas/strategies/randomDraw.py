import random
from card import Card
from strategies.baseStategy import BaseStategy
from spade.behaviour import CyclicBehaviour
import spade


class RandomDraw(BaseStategy, CyclicBehaviour):
    def __init__(self, score, cards, taken_cards):
       BaseStategy.__init__(self, score, cards, taken_cards)
       CyclicBehaviour.__init__(self)
    async def on_start(self):
        print('Random draw')
    
    async def run(self):
        message = await self.receive(timeout=10)
        # print('mess', message)
        if message:
            currPlayer = message.metadata.get("currPlayer")
            if currPlayer=="random@localhost":
                if message.body == "prviPotez" :
                    sendTo = message.metadata.get("sendTo")
                    print(f'{currPlayer} Karte  {len(self.cards)}')
                    randic = random.randint(0,len(self.cards)-1)
                    card = self.cards[randic]
                    self.cards.pop(randic)
                    miklos = "imam" if len(self.cards) > 0 else  "nemam"
                    msg = spade.message.Message(
                        to=sendTo,
                        body=miklos,     
                        sender=currPlayer,
                        metadata={"card": card.get_visual(), "cardNum": str(len(self.cards)),"cardNumber": card.get_sign(), 
                                  "cardScore": str(card.get_score()), "cardColor": card.get_color()}
                    )
                    await self.send(msg)
                if message.body == "igraj": 
                    currPlayer = message.metadata.get("currPlayer")
                    sendTo = message.metadata.get("sendTo")
                    # print(f'{currPlayer} Karte  {len(self.cards)}')
                    # for ca in self.cards:
                    #     print(ca.get_visual())
                    if len(self.cards) > 0:
                        randic = random.randint(0,len(self.cards)-1)
                        card = self.cards[randic]
                        self.cards.pop(randic)
                        miklos = "imam" 
                        msg = spade.message.Message(
                            to="avrb3@localhost",
                            body=miklos,     
                            sender=currPlayer,
                            metadata={"card": card.get_visual(),  "cardNum": str(len(self.cards)), "cardNumber": card.get_sign(), "cardScore": str(card.get_score()), "cardColor": card.get_color()}
                        )
                        await self.send(msg)

                    else:
                        print("šaljem da nemam")
                        msg = spade.message.Message(
                            to="avrb3@localhost",
                            body="nemam",     
                            sender=currPlayer,
                        )
                        await self.send(msg)
            
                if message.body == "uzmi":
                    score = int(message.metadata.get("cardScore"))
                    color = message.metadata.get("cardColor")
                    sign = message.metadata.get("cardSign")
                    igrac = message.metadata.get("igrac")
                    card = Card(score, color, sign)
                    self.cards.append(card)
                    msg = spade.message.Message(
                        to="avrb3@localhost",
                        body="uzeo",     
                        metadata={"card": card.get_visual(), "cardNumber": card.get_sign()}
                    )
                    await self.send(msg)

                