import random

# Builds a starter deck of 5 Basic Attack, 5 Basic Defend, and 3 Hesitation
def build_starter_deck():
    deck = []
    for i in range(5):
        deck.append(BasicAttack())
        deck.append(BasicDefend())
        if i < 3:
            deck.append(Hesitation())
    random.shuffle(deck)
    return deck

class Card:
    def __init__(self):
        self.name = None
        self.cost = None
        self.attack = None
        self.defense = None
        # TODO: More

    def stat_str(self, cost=True, attack=True, defense=True):
        stat_str = f"<{self.name}> "
        if self.playable:
            stat_str += "[*] "
        else:
            stat_str += "[X] "
        if cost:
            stat_str += f"COST: {self.cost} | "
        if attack:
            stat_str += f"ATK: {self.attack} | "
        if defense:
            stat_str += f"DEF: {self.defense} | "
        return stat_str

class BasicAttack(Card):
    def __init__(self):
        super().__init__()
        self.name = "Basic Attack"
        self.attack = 6
        self.cost = 1
        self.playable = True

class BasicDefend(Card):
    def __init__(self):
        super().__init__()
        self.name = "Basic Defend"
        self.defense = 5
        self.cost = 1
        self.playable = True

class Hesitation(Card):
    def __init__(self):
        super().__init__()
        self.name = "Hesitation"
        self.playable = False

