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

# def play_game():
#     while True:

deck = Deck()

# Dijeljenje karata
player1_cards, player2_cards = deck.deal_cards()

strategy1=RandomDraw(0, player1_cards, [])
strategy2=RandomDraw(0, player2_cards, [])


player1 = Player("avrb1w@localhost", "tajna", 0, player1_cards, [], strategy1)
player2 = Player("avrb2@localhost", "tajna", 0, player2_cards, [], strategy2)

prvi_igrac_index = random.randint(1, 2)

# 1
leading_player = player1 if prvi_igrac_index == 1 else player2
following_player = player1 if prvi_igrac_index != 1 else player2
print('Pokrećem igru, igru će započeti igrač ' + leading_player.get_name())

# print('---------------------------------------------------------------')
# # Ispis karata za svakog igrača
# print("Karte za igrača 1:")
# for card in player1_cards:
#     print(card.get_visual())

# print("Karte za igrača 2:")
# for card in player2_cards:
#     print(card.get_visual())

# while len(player1.cards) > 1:
#     random_broj = random.randint(0, len(player1.cards) - 1)

#     bacena_karta1 = leading_player.play_card(random_broj)
#     print(f'{leading_player.get_name()} baca kartu:')
#     print(f'{bacena_karta1.get_visual()}')

#     # time.sleep(0.5)

#     random_broj = random.randint(0, len(player2.cards) - 1)
#     bacena_karta2 = following_player.play_card(random_broj)
#     print(f'{following_player.get_name()} baca kartu:')
#     print(f'{bacena_karta2.get_visual()}')

#     time.sleep(0.5)

#     # print('Karte na stolu: ')
#     # # karte_na_stolu = [bacena_karta1, bacena_karta2]
#     # print(f'{bacena_karta1.get_visual()}')
#     # print(f'{bacena_karta2.get_visual()}')

#     # time.sleep(0.5)


#     if bacena_karta2.get_sign() == bacena_karta1.get_sign():
#         print(f'Štih uzima {following_player.get_name()}')
#         dummy = leading_player
#         leading_player = following_player
#         following_player = dummy

#     elif bacena_karta2.get_sign() == '7':
#         print(f'Štih uzima {following_player.get_name()}')
#         dummy = leading_player
#         leading_player = following_player
#         following_player = dummy

#     else:
#         print(f'Štih uzima {leading_player.get_name()}')


#     leading_player.taken_cards.append(bacena_karta1)
#     leading_player.taken_cards.append(bacena_karta2)
#     if len(deck.cards) >= 2:
#         leading_player.cards.append(deck.draw_card())
#         following_player.cards.append(deck.draw_card())

#     if len(player1.cards) == 0:
#         leading_player.add_points(10)
        
#     print(f'{leading_player.get_name()} ima {len(leading_player.cards)} karata')
#     print(f'{following_player.get_name()} ima {len(following_player.cards)} karata')
#     print(f'U špilu ima {len(deck.cards)} karata')
#     print('---------------------------------------------------------------')
#     time.sleep(0.5)

# for card in player1.taken_cards:
#     player1.add_points(card.get_score())

# for card in player2.taken_cards:
    # player2.add_points(card.get_score())

# agent1 = Agent("vrba1@yax.im", "tajna")
# agent2 = Agent("vrba2@yax.im", "tajna")

class Tournament(Agent):

    class Message(PeriodicBehaviour):

        async def on_start(self):
            self.counter = 0
            self.kartaA = ''
            self.kartaB = ''

        async def run(self):
            global leading_player
            global following_player
            global deck
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
        
            msg = await self.receive(timeout=5)      
            if msg:
                card = msg.metadata.get("card")
                cardNumber = msg.metadata.get("card")
                print(f'{msg.sender} baca kartu')
                print(card)
                if str(msg.sender)==leading_player.get_name():
                    print('kokolo')
                    self.kartaA = cardNumber
                    msg = spade.message.Message(
                        to=following_player.get_name(),
                        metadata= 
                        {"currPlayer" : following_player.get_name(),
                        "sendTo" : "avrb3@localhost",
                        "oppositePlayer" : leading_player.get_name(),
                        },
                        body="igraj"
                    )
                    await self.send(msg)

                if  str(msg.sender)==following_player.get_name():
                    self.kartaB = cardNumber
                    print('mokolo')
                    if self.kartaB == self.kartaA:
                        print(f'Štih uzima {following_player.get_name()}')
                        dummy = leading_player
                        leading_player = following_player
                        following_player = dummy

                    elif self.kartaB == '7':
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
                            {  
                                "cardScore": str(leadCard.get_score()),
                                "cardColor": leadCard.get_color(),
                                "cardSign": leadCard.get_sign(),  
                            }
                        )
                        await self.send(msg)

                        msg = spade.message.Message (
                            to=following_player.get_name(),
                            body="uzmi",
                            metadata= 
                            {  
                                "cardScore": str(followCard.get_score()),
                                "cardColor": followCard.get_color(),
                                "cardSign": followCard.get_sign(),  
                            }
                        )
                        await self.send(msg)

                        if msg.body == "nemam":
                            leading_player.score+=10
                            for card in player1.taken_cards:
                                player1.add_points(card.get_score())

                            for card in player2.taken_cards:
                                player2.add_points(card.get_score())
                            return


    async def setup(self):
        print("Tournamenlt: Pokrećem se!")
        start_at = datetime.datetime.now() + datetime.timedelta(seconds=1)
        ponasanje = self.Message(period=1, start_at=start_at)
        self.add_behaviour(ponasanje)   



if __name__ == "__main__":

    tournamentAgent = Tournament("avrb3@localhost", "tajna")
    tournamentAgent.start()

    gameAgent1 = GameAgentt(leading_player, 1)
    gameAgent1.start()

    # gameAgent2 = GameAgentt(following_player, 2)
    gameAgent2 = GameAgentt(following_player, 2)
    gameAgent2.start()

    input("Press ENTER to exit.\n")
    
    gameAgent1.stop()
    print('aaaaaa')
    gameAgent2.stop()
    tournamentAgent.stop()
# print(f'Bodovi igrača 1: {player1.get_score()}')
# print(f'Bodovi igrača 2: {player2.get_score()}')
# print(f'Pobjednik je {player1.get_name()}') if player1.get_score() > player2.get_score() else print(f'Pobjednik je {player2.get_name()}')