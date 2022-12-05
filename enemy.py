from constants import *
import utility
import card
import random

class Enemy:
    def __init__(self):
        self.name = None
        self.hp = None
        self.max_hp = None
        self.defense = None
        self.hand = None
        self.action = None

    def stat_str(self):
        return f"<{self.name}> HP: {self.hp}/{self.max_hp} | DEF: {self.defense}"

    def is_alive(self):
        assert self.hp is not None
        return self.hp > 0

    def change_hp(self, amt):
        assert self.hp is not None
        assert self.max_hp is not None
        self.hp += amt
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        elif self.hp < 0:
            self.hp = 0

    def change_defense(self, amt):
        self.defense += amt
        if self.defense < 0:
            self.defense = 0

    def pick_action(self):
        assert self.hand is not None
        assert len(self.hand) > 0
        self.action = random.choice(self.hand)

class RookieBrawler(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "Brawler"
        hp = utility.generate_fuzzed_value(42, HP_FUZZ_MULTIPLIER)
        self.hp = hp
        self.max_hp = hp
        self.defense = 0
        self.hand = [card.BasicAttack(), card.BasicAttack(), card.BasicAttack(), card.BasicDefend(), card.Hesitation()]

def generate_enemies(stage): # TODO: Vary enemies by stage
    num_enemies = random.randrange(1, 4)
    enemy_list = []
    for e in range(num_enemies):
        enemy_list.append(RookieBrawler())
    return enemy_list

