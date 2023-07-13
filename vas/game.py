import random
import time
from deck import Deck
from player import Player
import datetime
from operator import index, indexOf
import spade
from agent import GameAgent
from spade.behaviour import TimeoutBehaviour, CyclicBehaviour, PeriodicBehaviour
import random
from spade import quit_spade
from spade.agent import Agent

# def play_game():
#     while True:


deck = Deck()

# Dijeljenje karata
player1_cards, player2_cards = deck.deal_cards()

player1 = Player("Prvi igrac", 0, player1_cards, [], "random")
player2 = Player("Drugi igrac", 0, player2_cards, [], "random")

prvi_igrac_index = random.randint(1, 2)

# 1
leading_player = player1 if prvi_igrac_index == 1 else player2
following_player = player1 if prvi_igrac_index != 1 else player2
print('Pokrećem igru, igru će započeti igrač ' + leading_player.get_name())
print('---------------------------------------------------------------')
# Ispis karata za svakog igrača
print("Karte za igrača 1:")
for card in player1_cards:
    print(card.get_visual())

print("Karte za igrača 2:")
for card in player2_cards:
    print(card.get_visual())

while len(player1.cards) > 1:
    random_broj = random.randint(0, len(player1.cards) - 1)

    bacena_karta1 = leading_player.play_card(random_broj)
    print(f'{leading_player.get_name()} baca kartu:')
    print(f'{bacena_karta1.get_visual()}')

    # time.sleep(0.5)

    random_broj = random.randint(0, len(player2.cards) - 1)
    bacena_karta2 = following_player.play_card(random_broj)
    print(f'{following_player.get_name()} baca kartu:')
    print(f'{bacena_karta2.get_visual()}')

    time.sleep(0.5)

    # print('Karte na stolu: ')
    # # karte_na_stolu = [bacena_karta1, bacena_karta2]
    # print(f'{bacena_karta1.get_visual()}')
    # print(f'{bacena_karta2.get_visual()}')

    # time.sleep(0.5)


    if bacena_karta2.get_sign() == bacena_karta1.get_sign():
        print(f'Štih uzima {following_player.get_name()}')
        dummy = leading_player
        leading_player = following_player
        following_player = dummy

    elif bacena_karta2.get_sign() == '7':
        print(f'Štih uzima {following_player.get_name()}')
        dummy = leading_player
        leading_player = following_player
        following_player = dummy

    else:
        print(f'Štih uzima {leading_player.get_name()}')


    leading_player.taken_cards.append(bacena_karta1)
    leading_player.taken_cards.append(bacena_karta2)
    if len(deck.cards) >= 2:
        leading_player.cards.append(deck.draw_card())
        following_player.cards.append(deck.draw_card())

    if len(player1.cards) == 0:
        leading_player.add_points(10)
        
    print(f'{leading_player.get_name()} ima {len(leading_player.cards)} karata')
    print(f'{following_player.get_name()} ima {len(following_player.cards)} karata')
    print(f'U špilu ima {len(deck.cards)} karata')
    print('---------------------------------------------------------------')
    time.sleep(0.5)

for card in player1.taken_cards:
    player1.add_points(card.get_score())

for card in player2.taken_cards:
    player2.add_points(card.get_score())


agent1 = Agent("vrba1@yax.im", "tajna")
agent2 = Agent("vrba2@yax.im", "tajna")

gameAgent1 = GameAgent.setup(agent1, player1)
gameAgent2 = GameAgent.setup(agent2, player2)

print(f'Bodovi igrača 1: {player1.get_score()}')
print(f'Bodovi igrača 2: {player2.get_score()}')
print(f'Pobjednik je {player1.get_name()}') if player1.get_score() > player2.get_score() else print(f'Pobjednik je {player2.get_name()}')