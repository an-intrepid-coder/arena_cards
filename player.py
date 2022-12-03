from constants import *
import card

class Player:
    def __init__(self):
        self.deck = card.build_starter_deck()
        self.discard = []
        self.hp = STARTING_HP
        self.max_hp = STARTING_HP
        self.energy = STARTING_ENERGY
        self.max_energy = STARTING_ENERGY
        self.defend = 0

    def print_deck(self, names_only=True):
        for card in self.deck:
            if names_only:
                print(card.stat_str(cost=False, attack=False, defend=False))
            else:
                print(card.stat_str())

