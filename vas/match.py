import copy
import csv
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
from strategies.throwBigAtEndTakeAll import  ThrowBigAtEndTakeAll
from strategies.throwBigAtStartTakeAll import ThrowBigAtStartTakeAll
from strategies.throwBigAtStart import  ThrowBigAtStart
from strategies.throwBigAtEnd import ThrowBigAtEnd

from strategies.randomDraw import RandomDraw
import asyncio

# def play_game():
#     while True:



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
            global bodovaIgrac1
            global bodovaIgrac2
            global new_bodovaIgrac1
            global new_bodovaIgrac2
            global starts_first
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
                            for card in p1.taken_cards:
                                print ()
                                p1.add_points(int(card.get_score()))
                            for card in p2.taken_cards:
                                p2.add_points(int(card.get_score()))
                            print(f'Bodovi {p1.get_name()}: {p1.get_score()}')
                            print(f'Bodovi {p2.get_name()}: {p2.get_score()}')
                            winner = p1  if p1.get_score() > p2.get_score() else p2
                            loser = p1  if p1.get_score() < p2.get_score() else p2
                            print(f'Pobjednik je {p1.get_name()}') if p1.get_score() > p2.get_score() else print(f'Pobjednik je {p2.get_name()}')
                            ideza = 3 if loser.get_score() > 0 and loser.rounds == 0 else  2 if loser.get_score() == 0 else 1
                            print('ide za ', ideza)
                            if winner == p1:
                                new_bodovaIgrac1+=ideza
                            else: 
                                new_bodovaIgrac2+=ideza

                            filename = "data.csv"

                            with open(filename, "a", newline="") as file:
                                writer = csv.writer(file)
                                writer.writerow([p1.get_name(), p2.get_name(), p1.get_score(), p2.get_score(), ideza, starts_first])
                                                        
                            self.kill(exit_code=10)
                            return
                    
                    if msg.body == "imam":
                        await self.handleThrowAction(msg)   

                    if msg.body == "ponavljam":
                        await self.handleThrowAction(msg)   

                    if msg.body=="neponavljam":
                        print("mIJENJAM POČETNOGA IGRAČA")
                        dummy = leading_player
                        leading_player = following_player
                        following_player = dummy
                        await self.handleResultInput(msg)   


        async def handleThrowAction(self, msg):
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

            if len(self.baceneKarte) % 2 == 0 and len(self.baceneKarte) != 0:
                if self.kartaB.get_sign() == self.kartaA.get_sign() or self.kartaB.get_sign() == '7':
                    #implementiraj logiku za ponavljanje 
                    msg = spade.message.Message (
                        to=leading_player.get_name(),
                        body="ponovi",
                        metadata= 
                        {  "currPlayer" : leading_player.get_name(),
                            "sendTo" : "avrb3@localhost",
                            "oppositePlayer" : following_player.get_name(),
                            "cardScore": str(self.kartaB.get_score()),
                            "cardColor": self.kartaB.get_color(),
                            "cardSign": self.kartaB.get_sign(),
                            "igrac": leading_player.get_name() 
                        }
                    )
                    await self.send(msg)
                    # print(f'Štih uzima {following_player.get_name()}')
                    # dummy = leading_player
                    # leading_player = following_player
                    # following_player = dummy

                else:
                    print(f'Štih uzima {leading_player.get_name()}')
                    await self.handleResultInput(msg)

        async def handleResultInput(self, msg):
                print('handling')
                for car in self.baceneKarte: 
                    leading_player.taken_cards.append(car)

                for i in range(int(len(self.baceneKarte) / 2)):
                    leading_player.rounds+=1
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

                self.baceneKarte = []

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
        

    strategy1=RandomDraw(0, [], [])
    strategy2=ThrowBigAtEnd(0, [], [])
    strategy3=ThrowBigAtEndTakeAll(0, [], [])
    strategy4=ThrowBigAtStart(0, [], [])
    strategy5=ThrowBigAtStartTakeAll(0, [], [])




    player1 = Player("randomdraw@localhost", "tajna", 0, [], [], strategy1, 0)
    player2 = Player("throwbigatend@localhost", "tajna", 0, [], [], strategy2, 0)
    player3 = Player("throwbigatendtakeall@localhost", "tajna", 0, [], [], strategy3, 0)
    player4 = Player("throwbigatstart@localhost", "tajna", 0, [], [], strategy4, 0)
    player5 = Player("throwbigatstarttakeall@localhost", "tajna", 0, [], [], strategy5, 0)


    players = [
        player1,
        player2,
        player3,
        player4,
        player5,
    ]

    strategies = [
        strategy1,
        strategy2,
        strategy3,
        strategy4,
        strategy5,
    ]
    

    bodovaIgrac1 = 0
    bodovaIgrac2 = 0
    new_bodovaIgrac1 = 0
    new_bodovaIgrac2 = 0
    deck = Deck()

    pc1, pc2  = deck.deal_cards()

    i =  random.randint(0,len(players)-1)
    #i = 0
    p1 = players[i]
    p1.cards = pc1
    strategies[i].set_cards(pc1)
    p1.strategy = strategies[i]
    j = random.randint(0,len(players)-1)
    while j == i:
        j = random.randint(0,len(players)-1)
    strategies[j].set_cards(pc2)
    p2 = players[j]
    p2.cards = pc2
    p2.strategy = strategies[j]

    
    prvi_igrac_index = random.randint(1, 2)
    leading_player = p1 if prvi_igrac_index == 1 else p2
    following_player = p1 if prvi_igrac_index != 1 else p2
    starts_first = leading_player.get_name()

    print('Pokrećem igru, igru će započeti igrač ' + leading_player.get_name())
    gameAgent1 = GameAgentt(leading_player, 1)
    gameAgent1.start()

    gameAgent2 = GameAgentt(following_player, 2)
    gameAgent2.start()

    tournamentAgent = Tournament("avrb3@localhost", "tajna")
    tournamentAgent.start()

    input("Press ENTER to exit.\n")
    bodovaIgrac1 = new_bodovaIgrac1
    bodovaIgrac2 = new_bodovaIgrac2
    gameAgent1.stop()
    gameAgent2.stop()
    tournamentAgent.stop()

    


