from spade import agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour

class BaseStategy: 
    def __init__(self, score, cards, taken_cards):
        self.score = score
        self.cards = cards
        self.taken_cards = taken_cards

    def get_score(self):
        return self.score
    
    def get_cards(self):
        return self.cards
    
    def get_taken_cards(self): 
        return self.taken_cards
        
    def play_card(self, index=0):
        return self.cards.pop(index)
    
    def add_points(self, points):
        self.score += points

    
        
