import player
import enemy
import constants

# TEST CASE: (but will be basis for stage template)
class CardBattle:
    def __init__(self, player, enemies): 
        self.player = player
        self.enemies = enemies
        self.turn = 1
       
    def battle_won(self):
        for enemy in self.enemies:
            if enemy.is_alive():
                return False
        print("You won the battle!")
        return True 

    def game_over(self):
        if not self.player.is_alive():
            print("You won the battle!")
            return True
        return False

    def print_hand(self):
        count = 1
        for c in self.player.hand:
            print(f"[{count}] {c.stat_str()})")
            count += 1

    def print_enemies(self):
        count = 1
        for e in self.enemies:
            action_str = "None"
            if e.action is not None:
                action_str = e.action.name
                if e.action.attack is not None:
                    action_str += f" ({e.action.attack})"
            print(f"[{count}] {e.stat_str()} [{action_str}])")
            count += 1

    # Returns False if the player ended their turn
    def handle_input(self):
        while True:
            which_card = input("Enter # of card to play or (e)nd turn: ")
            if which_card == "e":
                return False
            if not which_card.isdecimal(): 
                print("Invalid selection!")
                continue
            index = int(which_card) - 1
            if index >= len(self.player.hand) or index < 0:
                print("Invalid selection!")
                continue
            card_to_play = self.player.hand[index]
            if not card_to_play.playable:
                print("That card is not playable!")
                continue
            if card_to_play.cost > self.player.energy:
                print("Not enough energy to play this card this turn!")
                continue
            if card_to_play.attack is not None:
                if card_to_play.aoe is None:
                    which_enemy = input("Enter # of enemy to attack: ")
                    index = int(which_enemy) - 1
                    if index >= len(self.enemies) or index < 0:
                        print("Invalid selection!")
                        continue
                    target = self.enemies[index]
                    if not target.is_alive():
                        print("Target is already dead!")
                        continue
                    raw_dmg = card_to_play.attack
                    dmg = raw_dmg - target.defense
                    if dmg < 0:
                        dmg = 0
                    target.change_hp(-dmg)
                    target.change_defense(-raw_dmg)
                    print(f"{target.name} is struck for {dmg} dmg!")
                else:
                    for target in self.enemies:
                        if target.is_alive():
                            raw_dmg = card_to_play.attack
                            dmg = raw_dmg - target.defense
                            if dmg < 0:
                                dmg = 0
                            target.change_hp(-dmg)
                            target.change_defense(-raw_dmg)
                            print(f"{target.name} is struck for {dmg} dmg!")
            if card_to_play.defense is not None:
                self.player.change_defense(card_to_play.defense)
                print(f"{self.player.name} prepares {card_to_play.defense} defense!")
            break
        self.player.change_energy(-card_to_play.cost)
        self.player.hand.remove(card_to_play)
        self.player.discard.append(card_to_play)
        return True

    def enemy_actions(self):
        for e in self.enemies:
            if e.is_alive():
                e.defense = 0
                card_to_play = e.action
                if card_to_play.attack is not None:
                    raw_dmg = card_to_play.attack
                    dmg = raw_dmg - self.player.defense
                    if dmg < 0:
                        dmg = 0
                    self.player.change_hp(-dmg)
                    self.player.change_defense(-raw_dmg)
                    print(f"{self.player.name} is struck for {dmg} dmg!")
                if card_to_play.defense is not None:
                    e.change_defense(card_to_play.defense)
                    print(f"{e.name} prepares {card_to_play.defense} defense!")
                else:
                    print(f"{e.name} uses {card_to_play.name}")

    def battle(self): 
        self.player.reset_deck()
        # Player always goes first
        while not (self.battle_won() or self.game_over()): 
            for entry in self.enemies: 
                if entry.is_alive():
                    entry.pick_action()
                else:
                    entry.action = None
            self.player.defense = 0
            self.player.energy = self.player.max_energy
            self.player.draw_hand()
            while True:
                print(f"Turn {self.turn}:")
                print(self.player.stat_str())
                self.print_hand()
                print("------")
                self.print_enemies()
                if not self.handle_input():
                    break
            self.player.discard_hand()
            self.enemy_actions()
            self.turn += 1
        self.player.reset_deck()

class StageGraphNode:
    def __init__(self, contents, prev_node, next_node):
        self.contents = contents
        self.prev_node = prev_node
        self.next_node = next_node

def generate_stage_graph(player):
    root = StageGraphNode(CardBattle(player, enemy.generate_enemies(stage=1)), None, None)
    graph = [root]
    for i in range(constants.NUM_STAGES):
        stage_level = i + 1
        next_stage = CardBattle(player, enemy.generate_enemies(stage_level))
        next_node = StageGraphNode(next_stage, graph[i], None)
        graph[i].next_node = next_node
        graph.append(next_node)
    return graph

