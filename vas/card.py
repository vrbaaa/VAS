class Card:
    def __init__(self, score, color, sign):
        self.score = score
        self.color = color
        self.sign = sign
        self.visual = self.create_visual()  
    def get_score(self):
        return self.score

    def get_color(self):
        return self.color

    def get_sign(self):
        return self.sign
    
    def get_visual(self):
        return self.visual

    def get_combo(self):
        return self.sign + self.color
    def create_visual(self):
        suit_symbols = {
            'T': '♦',
            'K': '♠',
            'P': '♥',
            'H': '♣'
        }

        value_mapping = {
            '7': '7',
            '8': '8',
            '9': '9',
            '10': '10',
            'J': 'J',
            'Q': 'Q',
            'K': 'K',
            'A': 'A'
        }

        suit_symbol = suit_symbols.get(self.color, '')
        value = value_mapping.get(self.sign, '')

        visual = f"┌─────────┐\n" \
                 f"│ {value:<2}      │\n" \
                 f"│         │\n" \
                 f"│    {suit_symbol}    │\n" \
                 f"│         │\n" \
                 f"│      {value:>2} │\n" \
                 f"└─────────┘"

        return visual