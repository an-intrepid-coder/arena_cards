from constants import *
import utility

class Enemy:
    def __init__(self):
        self.name = None
        self.hp = None
        self.max_hp = None
        self.defend = None
        self.actions = [] # List of Actions

    def stat_str(self):
        return f"<{self.name}> HP: {self.hp}/{self.max_hp} | DEF: {self.defend}"

class Brawler(Enemy):
    def __init__(self):
        super().__init__()
        hp = utility.generate_fuzzed_value(42, HP_FUZZ_MULTIPLIER)
        self.hp = hp
        self.max_hp = hp
        self.defend = 0
        self.actions = [] # TODO

