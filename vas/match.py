import random
import time
from card import Card
from deck import Deck
from player import Player
import datetime
from operator import index, indexOf
import spade
from agent import  GameAgentt
from spade.behaviour import TimeoutBehaviour, CyclicBehaviour, PeriodicBehaviour
import random
from spade.agent import Agent
from strategies.optimalDraw import OptimalDraw

from strategies.randomDraw import RandomDraw
# from globals import player1_cards, player2_cards
import asyncio

# def play_game():
#     while True:

deck = Deck()

# Dijeljenje karata
player1_cards, player2_cards = deck.deal_cards()

strategy1=RandomDraw(0, player1_cards, [])
strategy2=OptimalDraw(0, player2_cards, [])


player1 = Player("random@localhost", "tajna", 0, player1_cards, [], strategy1)
player2 = Player("optimal@localhost", "tajna", 0, player2_cards, [], strategy2)

prvi_igrac_index = random.randint(1, 2)

# 1
# leading_player = player1 if prvi_igrac_index == 1 else player2
# following_player = player1 if prvi_igrac_index != 1 else player2

leading_player = player1 
following_player =  player2
print('Pokrećem igru, igru će započeti igrač ' + leading_player.get_name())

class Tournament(Agent):

    class Message(PeriodicBehaviour):

        async def on_start(self):
            self.counter = 0
            self.kartaA = {}
            self.kartaB = {}
            self.baceneKarte = []

        async def run(self):
            global leading_player
            global following_player
            global deck
            if self.counter==0:
                print("----------------KRECEMO-------")
        
                msg = spade.message.Message(
                to=leading_player.get_name(),
                body="igraj", metadata= 
                {
                    "currPlayer" : leading_player.get_name(),
                    "sendTo" : "avrb3@localhost",
                    "oppositePlayer" : following_player.get_name(),
                })

                await self.send(msg)
         
                self.counter+=1
            else: 
                msg = await self.receive(timeout=5)      
                if msg:
                    # print('porukaa', msg.body)
                    if msg.body == "nemam":
                            print("nemam")
                            print(str(msg.sender))
                            leading_player.score+=10
                            for card in player1.taken_cards:
                                player1.add_points(int(card.get_score()))
                            for card in player2.taken_cards:
                                player2.add_points(int(card.get_score()))
                            print(f'Bodovi {player1.get_name()}: {player1.get_score()}')
                            print(f'Bodovi {player2.get_name()}: {player2.get_score()}')
                            print(f'Pobjednik je {player1.get_name()}') if player1.get_score() > player2.get_score() else print(f'Pobjednik je {player2.get_name()}')
                            self.kill(exit_code=10)
                            return
                    
                    elif msg.body == "imam":
                        card = msg.metadata.get("card")
                        cardNumber = msg.metadata.get("cardNumber")
                        cardScore = msg.metadata.get("cardScore")
                        cardColor = msg.metadata.get("cardColor")
                        cardNum = msg.metadata.get("cardNum")
                        carta = Card(int(cardScore), cardColor, cardNumber)
                        print(f'{msg.sender} baca kartu, ima jos {cardNum} karti')
                        print(card)
                        if str(msg.sender)==leading_player.get_name() and msg.body != "nemam":
                            self.kartaA = carta
                            self.baceneKarte.append(self.kartaA)
                            msg = spade.message.Message(
                                to=following_player.get_name(),
                                metadata= 
                                {"currPlayer" : following_player.get_name(),
                                "sendTo" : "avrb3@localhost",
                                "oppositePlayer" : leading_player.get_name(),
                                "cardScore": str(self.kartaA.get_score()),
                                "cardColor": self.kartaA.get_color(),
                                "cardSign": self.kartaA.get_sign(),
                                },
                                body="igraj"
                            )
                            await self.send(msg)

                        if  str(msg.sender)==following_player.get_name() and msg.body != "nemam":
                            self.kartaB = carta
                            self.baceneKarte.append(self.kartaB)

                        #Promjeni == 2 u % 2 == 0
                        if len(self.baceneKarte) == 2:
                            self.baceneKarte = []
                            if self.kartaB.get_sign() == self.kartaA.get_sign() or self.kartaB.get_sign() == '7':
                                #implementiraj logiku za ponavljanje 
                                print(f'Štih uzima {following_player.get_name()}')
                                dummy = leading_player
                                leading_player = following_player
                                following_player = dummy

                            else:
                                print(f'Štih uzima {leading_player.get_name()}')

                            leading_player.taken_cards.append(self.kartaA)
                            leading_player.taken_cards.append(self.kartaB)

                            if len(deck.cards) >= 2:
                                leadCard = deck.draw_card()
                                followCard = deck.draw_card()

                                msg = spade.message.Message (
                                    to=leading_player.get_name(),
                                    body="uzmi",
                                    metadata= 
                                    {  "currPlayer" : leading_player.get_name(),
                                        "sendTo" : "avrb3@localhost",
                                        "oppositePlayer" : following_player.get_name(),
                                        "cardScore": str(leadCard.get_score()),
                                        "cardColor": leadCard.get_color(),
                                        "cardSign": leadCard.get_sign(),
                                        "igrac": leading_player.get_name() 
                                    }
                                )
                                await self.send(msg)


                                msg = spade.message.Message (
                                    to=following_player.get_name(),
                                    body="uzmi",
                                    metadata= 
                                    {  "currPlayer" : following_player.get_name(),
                                        "sendTo" : "avrb3@localhost",
                                        "oppositePlayer" : leading_player.get_name(),
                                        "cardScore": str(followCard.get_score()),
                                        "cardColor": followCard.get_color(),
                                        "cardSign": followCard.get_sign(),  
                                        "igrac": following_player.get_name() 
                                    }
                                )

                                await self.send(msg)

                            msg = spade.message.Message(
                                            to=leading_player.get_name(),
                                            body="igraj",
                                              metadata= 
                                            {
                                                "currPlayer" : leading_player.get_name(),
                                                "sendTo" : "avrb3@localhost",
                                                "oppositePlayer" : following_player.get_name(),
                                            })
                            await self.send(msg)
                                


    async def setup(self):
        print("Tournamenlt: Pokrećem se!")
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=1)
        ponasanje = self.Message(period=0.5, start_at=start_at)
        self.add_behaviour(ponasanje)   


if __name__ == "__main__":



    gameAgent1 = GameAgentt(leading_player, 1)
    gameAgent1.start()
    time.sleep(1)

    gameAgent2 = GameAgentt(following_player, 2)
    gameAgent2.start()
    time.sleep(1)

    tournamentAgent = Tournament("avrb3@localhost", "tajna")
    tournamentAgent.start()
    time.sleep(1)
    input("Press ENTER to exit.\n")
    
    gameAgent1.stop()
    gameAgent2.stop()
    tournamentAgent.stop()
