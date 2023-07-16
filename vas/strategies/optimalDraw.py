import random
from card import Card
from strategies.baseStategy import BaseStategy
from spade.behaviour import CyclicBehaviour

import spade


class OptimalDraw(BaseStategy, CyclicBehaviour):
    def __init__(self, score, cards, taken_cards):
       BaseStategy.__init__(self, score, cards, taken_cards)
       CyclicBehaviour.__init__(self)
    async def on_start(self):
        print('Optimal draw')

    def handlePlaySmallCard(self):
        filtered_cards = list(filter(lambda x: x.get_score() == 0 and x.get_sign() != '7', self.cards))
        if len(filtered_cards) > 0:
            randic = random.randint(0,len(filtered_cards)-1)
            duplicate = filtered_cards[randic]
            index = next((i for i, x in enumerate(self.cards) if x.get_combo() == duplicate.get_combo()), -1)
            if index != -1:
                print('combo' , duplicate.get_combo())
            else:
                print('reazličit')
            card = self.cards[index]
            self.cards.pop(index)
            return card
        else:
            filtered_cards = list(filter(lambda x: x.get_score() != 0, self.cards))
            if len(filtered_cards) > 0:
                randic = random.randint(0,len(filtered_cards)-1)
                duplicate = filtered_cards[randic]
                index = next((i for i, x in enumerate(self.cards) if x.get_combo() == duplicate.get_combo()), -1)
                if index != -1:
                    print('combo' , duplicate.get_combo())
                else:
                    print('reazličit')
                card = self.cards[index]
                self.cards.pop(index)
                return card
            else: 
                randic = random.randint(0,len(self.cards)-1)
                card = self.cards[randic]
                self.cards.pop(randic)
                return card

    def handlePlaySameCard(self, opponent_card):
        filtered_cards = list(filter(lambda x: x.get_sign() == opponent_card.get_sign(), self.cards))
        if len(filtered_cards) > 0:
            randic = random.randint(0,len(filtered_cards)-1)
            duplicate = filtered_cards[randic]
            index = next((i for i, x in enumerate(self.cards) if x.get_combo() == duplicate.get_combo()), -1)
            if index != -1:
                print('combo' , duplicate.get_combo())
            else:
                print('reazličit')
            card = self.cards[index]
            self.cards.pop(index)
            return card
        else:
            filtered_cards = list(filter(lambda x: x.get_sign() == '7', self.cards))
            if len(filtered_cards) > 0:
                randic = random.randint(0,len(filtered_cards)-1)
                duplicate = filtered_cards[randic]
                index = next((i for i, x in enumerate(self.cards) if x.get_combo() == duplicate.get_combo()), -1)
                if index != -1:
                    print('combo' , duplicate.get_combo())
                else:
                    print('reazličit')
                card = self.cards[index]
                self.cards.pop(index)
                return card
            else: 
                randic = random.randint(0,len(self.cards)-1)
                card = self.cards[randic]
                self.cards.pop(randic)
                return card
    
    async def run(self):
        message = await self.receive(timeout=10)
        # print('mess', message)

        if message:
            currPlayer = message.metadata.get("currPlayer")
            # print('currPlayer', currPlayer)

            if currPlayer=="optimal@localhost":
                if message.body == "prviPotez":
                    sendTo = message.metadata.get("sendTo")
                    # print(f'{currPlayer} Karte  {len(self.cards)}')
                    randic = random.randint(0,len(self.cards)-1)
                    card = self.cards[randic]
                    self.cards.pop(randic)
                    msg = spade.message.Message(
                        to=sendTo,
                        body="imam",     
                        sender=currPlayer,
                        metadata={"card": card.get_visual(),  "cardNum": str(len(self.cards)),"cardNumber": card.get_sign(), "cardScore": str(card.get_score()), "cardColor": card.get_color()}
                    )
                    await self.send(msg)
                if message.body == "igraj": 
                    currPlayer = message.metadata.get("currPlayer")
                    sendTo = message.metadata.get("sendTo")
                    # print(f'{currPlayer} Karte  {len(self.cards)}')
                    # for ca in self.cards:
                    #     print(ca.get_visual())

                    if len(self.cards) > 0:
                        sign = message.metadata.get("cardSign")
                        if sign:
                            score = int(message.metadata.get("cardScore"))
                            color = message.metadata.get("cardColor")
                            sign = message.metadata.get("cardSign")
                            opponent_card = Card(score, color, sign)
                            if opponent_card.get_score() == 0:
                                card = self.handlePlaySmallCard()
                                # print('karta', card.get_visual())
                                msg = spade.message.Message(
                                        to="avrb3@localhost",
                                        body="imam",     
                                        sender=currPlayer,
                                        metadata={"card": card.get_visual(),  "cardNum": str(len(self.cards)),"cardNumber": card.get_sign(), "cardScore": str(card.get_score()), "cardColor": card.get_color()}
                                    )
                                await self.send(msg)
                            else: 
                                card = self.handlePlaySameCard(opponent_card)
                                msg = spade.message.Message(
                                        to="avrb3@localhost",
                                        body="imam",     
                                        sender=currPlayer,
                                        metadata={"card": card.get_visual(), "cardNum": str(len(self.cards)), "cardNumber": card.get_sign(), "cardScore": str(card.get_score()), "cardColor": card.get_color()}
                                    )
                                await self.send(msg)
                        else:
                            card = self.handlePlaySmallCard()
                            msg = spade.message.Message(
                                        to="avrb3@localhost",
                                        body="imam",     
                                        sender=currPlayer,
                                        metadata={"card": card.get_visual(), "cardNum": str(len(self.cards)), "cardNumber": card.get_sign(), "cardScore": str(card.get_score()), "cardColor": card.get_color()}
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
                    card = Card(score, color, sign)
                    self.cards.append(card)
                    msg = spade.message.Message(
                        to="avrb3@localhost",
                        body="uzeo",     
                        metadata={"card": card.get_visual(), "cardNumber": card.get_sign()}
                    )
                    await self.send(msg)

                