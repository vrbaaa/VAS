import random
import spade
from spade.behaviour import CyclicBehaviour
from card import Card
from spade.agent import Agent

class LowDraw(Agent):
    def __init__(self):
        self.strategy = self.LowDrawBeh()

    class LowDrawBeh(CyclicBehaviour):

        def __init__(self, name, password, score, cards, taken_cards):
            self.name = name
            self.password = password
            self.score = score
            self.cards = cards
            self.taken_cards = taken_cards

        async def on_start(self):
            print('High draw')
        
        async def run(self):
            message = await self.receive(timeout=5)
            if message:
                if message.body == "prviPotez":
                    currPlayer = message.metadata.get("currPlayer")
                    sendTo = message.metadata.get("sendTo")
                    print(f'{currPlayer} Karte  {len(self.cards)}')
                    for ca in self.cards:
                        ca.get_visual()
                    randic = random.randint(0,len(self.cards)-1)
                    card = self.cards[randic]
                    self.cards.pop(randic)
                    miklos = "imam" if len(self.cards) > 0 else  "nemam"
                    msg = spade.message.Message(
                        to=sendTo,
                        body=miklos,     
                        sender=currPlayer,
                        metadata={"card": card.get_visual(), "cardNumber": card.get_sign()}
                    )
                    await self.send(msg)
                if message.body == "igraj": 
                    currPlayer = message.metadata.get("currPlayer")
                    sendTo = message.metadata.get("sendTo")
                    print(f'{currPlayer} Karte  {len(self.cards)}')
                    randic = random.randint(0,len(self.cards)-1)
                    card = self.cards[randic]
                    self.cards.pop(randic)
                    miklos = "imam" if len(self.cards) > 0 else  "nemam"
                    msg = spade.message.Message(
                        to="avrb3@localhost",
                        body=miklos,     
                        sender=currPlayer,
                        metadata={"card": card.get_visual(), "cardNumber": card.get_sign()}
                    )
                    await self.send(msg)
            
                if message.body == "uzmi":
                    print('--------------------------------------------------------------')
                    print('uzimam')
                    print('karte prije', len(self.cards))
                    score = int(message.metadata.get("cardScore"))
                    color = message.metadata.get("cardColor")
                    sign = message.metadata.get("cardSign")
                    igrac = message.metadata.get("igrac")
                    card = Card(score, color, sign)
                    self.cards.append(card)
                    print('karta',card.get_visual() )
                    print('karte posle', len(self.cards))
                    print(f'{igrac} : imam karte: ')
                    for ca in self.cards:
                        ca.get_visual()
                    msg = spade.message.Message(
                        to="avrb3@localhost",
                        body="uzeo",     
                        metadata={"card": card.get_visual(), "cardNumber": card.get_sign()}
                    )
                    await self.send(msg)

        def get_name(self): 
            return self.name
            
        def get_score(self):
            return self.score
        
        def get_cards(self):
            return self.cards
        
        def get_taken_cards(self): 
            return self.taken_cards
            
        def play_card(self, index=0):
            # generate random number between 0 and 3
            return self.cards.pop(index)
        
        def add_points(self, points):
            self.score += points

    async def setup(self):
        print('dodano ponasanje')
        ponasanje = self.LowDrawBeh()
        self.add_behaviour(ponasanje)
