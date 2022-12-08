import constants
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
        self.name = "Rookie Brawler"
        hp = utility.generate_fuzzed_value(16, constants.HP_FUZZ_MULTIPLIER) 
        self.hp = hp
        self.max_hp = hp
        self.defense = 0
        self.hand = [card.BasicAttack(), card.BasicAttack(), card.BasicAttack(), card.BasicDefend(), card.Hesitation()]

class Brawler(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "Brawler"
        hp = utility.generate_fuzzed_value(25, constants.HP_FUZZ_MULTIPLIER) 
        self.hp = hp
        self.max_hp = hp
        self.defense = 0
        self.hand = [card.BasicAttack(), card.BasicAttack(), card.BasicAttack(), card.BasicDefend()]

class CarefulBrawler(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "Careful Brawler"
        hp = utility.generate_fuzzed_value(25, constants.HP_FUZZ_MULTIPLIER) 
        self.hp = hp
        self.max_hp = hp
        self.defense = 0
        self.hand = [card.BasicAttack(), card.BasicAttack(), card.BasicDefend(), card.BasicDefend()]
        for lvl in range(5):
            self.hand[2].upgrade()
            self.hand[3].upgrade()

class AggroBrawler(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "Aggro Brawler"
        hp = utility.generate_fuzzed_value(25, constants.HP_FUZZ_MULTIPLIER) 
        self.hp = hp
        self.max_hp = hp
        self.defense = 0
        self.hand = [card.BasicAttack(), card.BasicAttack(), card.BasicAttack(), card.BasicAttack()]
        for lvl in range(2):
            self.hand[2].upgrade()
            self.hand[3].upgrade()

def generate_enemies(stage):  
    enemy_min = 1
    enemy_max = 3
    if stage > 3:
        enemy_max += 1
    num_enemies = random.randrange(enemy_min, enemy_max)
    enemy_list = []
    for e in range(num_enemies):
        choices = [RookieBrawler(), Brawler(), CarefulBrawler(), AggroBrawler()]
        enemy_list.append(random.choice(choices))
    return enemy_list

