from card import Card
import random

class Deck:
    def __init__(self):
        self.cards = self.create_deck()

    def create_deck(self):
        deck = []
        colors = ['T', 'K', 'P', 'H']
        signs = ['7', '8', '9', '10', 'J', 'Q', 'K', 'A']

        for color in colors:
            for sign in signs:
                if sign in ['10', 'A']:
                    score = 10
                else:
                    score = 0
                card = Card(score, color, sign)
                deck.append(card)
        random.shuffle(deck)
        return deck
    
    def deal_cards(self):
        if len(self.cards) < 8:
            print("Nema dovoljno karata za dijeljenje.")
            return

        player1_cards = []
        player2_cards = []

        for _ in range(4):
            player1_cards.append(self.cards.pop(0))
            player2_cards.append(self.cards.pop(0))

        return player1_cards, player2_cards
    
    def draw_card(self):
        if len(self.cards) == 0:
            print("Nema više karata u špilu.")
            return None

        return self.cards.pop(0)