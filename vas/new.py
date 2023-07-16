import random
import time
from deck import Deck
from player import Player
import datetime
from operator import index, indexOf
import spade
from newAgent import GameAgenttt, GameAgentt
from spade.behaviour import TimeoutBehaviour, CyclicBehaviour, PeriodicBehaviour
import random
from spade.agent import Agent
from strategies.throwBigAtEnd import ThrowBigAtEnd

from strategies.randomDraw import RandomDraw

# def play_game():
#     while True:


deck = Deck()

# Dijeljenje karata
player1_cards, player2_cards = deck.deal_cards()

player1 = Player("avrb1@localhost", "tajna", 0, player1_cards, [], RandomDraw)
player2 = Player("avrb2@localhost", "tajna", 0, player2_cards, [], RandomDraw)

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
    class Message(CyclicBehaviour):
        async def on_start(self):
            self.counter = 0

        async def run(self):
            print('aaaa')
            msg = spade.message.Message(
            to=leading_player.get_name(),
            body="prviPotez")

            await self.send(msg)

            msg = spade.message.Message(
            to=following_player.get_name(),
            body="prviPotez")

            await self.send(msg)
        

    async def setup(self):
        print("Tournamenlt: Pokrećem se!")
        start_at = datetime.datetime.now()
        ponasanje = self.Message()
        self.add_behaviour(ponasanje)   

class IgracA(Agent):
    class Randommm(CyclicBehaviour):
        async def on_start(self):
            print('Random draw')
    
        async def run(self):
            print('Pokrećem se')
            message = await self.receive()
            if message:
                print(f"{self.agent.name}: Received message: {message}")
            else:
                print(f"{self.agent.name}: No message received.")

    async def setup(self):
        print("IgracA: Pokrećem se!")
        ponasanjeSve2 = self.Randommm()
        self.add_behaviour(ponasanjeSve2)

class IgracB(Agent):
    class Randomm(CyclicBehaviour):
        async def on_start(self):
            print('Random draw')
    
        async def run(self):
            print('Pokrećem se')
            message = await self.receive()
            if message:
                print(f"{self.agent.name}: Received message: {message}")
            else:
                print(f"{self.agent.name}: No message received.")

    async def setup(self):
        print("IgracB: Pokrećem se!")
        ponasanjeSve2 = self.Randomm()
        self.add_behaviour(ponasanjeSve2)

if __name__ == "__main__":

    tournamentAgent = Tournament("avrb4@localhost", "tajna")
    tournamentAgent.start()

    gameAgent1 = IgracA("avrb5@localhost", "tajna")
    gameAgent1.start()

    # gameAgent2 = GameAgentt(following_player, 2)
    gameAgent2 = IgracB("avrb6@localhost", "tajna")


    gameAgent2.start()

    input("Press ENTER to exit.\n")
    
    gameAgent1.stop()
    print('aaaaaa')
    gameAgent2.stop()
    tournamentAgent.stop()
# print(f'Bodovi igrača 1: {player1.get_score()}')
# print(f'Bodovi igrača 2: {player2.get_score()}')
# print(f'Pobjednik je {player1.get_name()}') if player1.get_score() > player2.get_score() else print(f'Pobjednik je {player2.get_name()}')