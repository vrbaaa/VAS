
import random
import time
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
import asyncio

class Tournament(Agent):
    class Message(PeriodicBehaviour):
        async def on_start(self):
            self.counter = 0
            self.kartaA = {}
            self.kartaB = {}

        async def run(self):
            msg = spade.message.Message(
            to=self.leading_player.get_name(),
            body="igraj",
            metadata= 
                {"currPlayer" : self.leading_player.get_name(),
                    "sendTo" : "avrb3@localhost",
                    "oppositePlayer" : self.following_player.get_name(),

                    })
            await self.send(msg)
        
            msg = await self.receive(timeout=100)      
            if msg:
                card = msg.metadata.get("card")
                print(f'{msg.sender} baca kartu')
                print(card.get_visual())
                if msg.sender == self.leading_player.get_name():
                    self.kartaA = card
                    msg = spade.message.Message(
                        to=self.following_player.get_name(),
                        metadata= 
                        {"currPlayer" : self.following_player.get_name(),
                        "sendTo" : "avrb3@localhost",
                        "oppositePlayer" : self.leading_player.get_name(),
                        "playedCard": card
                        },
                        body="igraj"
                    )
                    await self.send(msg)

                if msg.sender == self.following_player.get_name():
                    self.kartaB = card

                    if self.kartaB.get_sign() == self.kartaA.get_sign():
                        print(f'Štih uzima {self.following_player.get_name()}')
                        dummy = self.leading_player
                        self.leading_player = self.following_player
                        self.following_player = dummy

                    elif self.kartaB.get_sign() == '7':
                        print(f'Štih uzima {self.following_player.get_name()}')
                        dummy = self.leading_player
                        self.leading_player = self.following_player
                        self.following_player = dummy

                    else:
                        print(f'Štih uzima {self.leading_player.get_name()}')

                    self.leading_player.taken_cards.append(self.kartaA)
                    self.leading_player.taken_cards.append(self.kartaB)
                    if len(self.deck.cards) >= 2:
                        leadCard = self.deck.draw_card()
                        followCard = self.deck.draw_card()

                        msg = spade.message.Message (
                            to=self.leading_player.get_name(),
                            body="uzmi",
                            metadata= 
                            {  "takenCard": leadCard,
                            }
                        )
                        await self.send(msg)

                        msg = spade.message.Message (
                            to=self.following_player.get_name(),
                            body="uzmi",
                            metadata= 
                            {  "takenCard": followCard,
                            }
                        )
                        await self.send(msg)

                    if len(self.leading_player.cards) == 0:
                        self.leading_player.add_points(10)

            self.counter = self.counter+1

    async def setup(self, leading_player, following_player, deck ):
        print("Tournamenlt: Pokrećem se!")
        self.leading_player = leading_player
        self.following_player = following_player
        self.deck = deck
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=2)
        ponasanje = self.Message(period=1, start_at=start_at)
        self.add_behaviour(ponasanje)   
