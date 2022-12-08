import card
import random
import constants

class Player:
    def __init__(self):
        self.name = "Player"
        self.hand = []
        self.draw = card.build_starter_deck()
        self.discard = []
        self.hp = constants.STARTING_HP
        self.max_hp = constants.STARTING_HP
        self.energy = constants.STARTING_ENERGY
        self.max_energy = constants.STARTING_ENERGY
        self.defense = 0

    def total_cards_amt(self):
        return len(self.hand) + len(self.draw) + len(self.discard)

    def stat_str(self):
        return f"<{self.name}> HP: {self.hp}/{self.max_hp} DEF: {self.defense} ENERGY: {self.energy}/{self.max_energy}"

    def reshuffle(self):
        assert len(self.draw) == 0
        while len(self.discard) > 0:
            c = self.discard.pop()
            self.draw.append(c)
        random.shuffle(self.draw)

    def change_hp(self, amt):
        self.hp += amt
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        elif self.hp < 0:
            self.hp = 0
    
    def change_defense(self, amt):
        self.defense += amt
        if self.defense < 0:
            self.defense = 0

    def change_energy(self, amt):
        self.energy += amt

    def discard_hand(self):
        while len(self.hand) > 0:
            card_to_discard = self.hand.pop()
            self.discard.append(card_to_discard)

    def draw_hand(self):
        for i in range(constants.BASE_DRAW_AMOUNT):
            if len(self.draw) == 0:
                self.reshuffle()
            drawn = self.draw.pop()
            self.hand.append(drawn)

    def is_alive(self):
        return self.hp > 0

    # Puts everything back in the draw pile and shuffles it:
    def reset_deck(self):
        while len(self.hand) > 0:
            yoink = self.hand.pop()
            self.draw.append(yoink)
        while len(self.discard) > 0:
            yoink = self.discard.pop()
            self.draw.append(yoink)
        random.shuffle(self.draw)

    # Returns a list of the cards which may be upgraded:
    def get_upgradeable_cards(self): 
        upgradeable = []
        for card in self.draw:
            if card.upgradeable:
                upgradeable.append(card) 
        return upgradeable

