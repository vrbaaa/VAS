class Player:
    def __init__(self, name, password, score, cards, taken_cards, strategy):
        self.name = name
        self.password = password
        self.score = score
        self.cards = cards
        self.taken_cards = taken_cards
        self.strategy = strategy

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
    
        