import player
import enemy
import constants
import curses

class CardBattle:
    def __init__(self, player, enemies, stdscr): 
        self.player = player
        self.enemies = enemies
        self.turn = 1
        self.stdscr = stdscr
       
    def battle_won(self):
        for enemy in self.enemies:
            if enemy.is_alive():
                return False
        return True 

    def game_over(self):
        if not self.player.is_alive():
            return True
        return False

    def get_hand_str_list(self):
        hand_str_list = []
        count = 1
        for c in self.player.hand:
            hand_str_list.append(f"[{count}] {c.stat_str()}")
            count += 1
        return hand_str_list

    def get_enemy_str_list(self):
        enemy_str_list = []
        count = 1
        for e in self.enemies:
            action_str = "None"
            if e.action is not None:
                action_str = e.action.name
                if e.action.attack is not None:
                    action_str += f" ({e.action.attack})"
            enemy_str_list.append(f"[{count}] {e.stat_str()} [{action_str}]")
            count += 1
        return enemy_str_list

    def clear_prompt_lines(self):
        maxyx = self.stdscr.getmaxyx()
        line = constants.PROMPT_LINE
        while line < maxyx[0]:
            blank = ""
            for x in range(maxyx[1] - 1):
                blank += " "
            self.stdscr.addstr(line, 0, blank)
            line += 1

    # Returns False if the player ended their turn
    def handle_input(self):
        while True:
            maxyx = self.stdscr.getmaxyx()
            y = 13
            prompt = "# of card to play or (e)nd turn"
            x = maxyx[1] // 2 - len(prompt) // 2
            self.stdscr.addstr(y, x, prompt)
            which_card = self.stdscr.getch()
            if which_card == ord('e'):
                return False
            if not which_card in range(48, 58):
                continue
            index = int(chr(which_card)) - 1
            if index >= len(self.player.hand) or index < 0:
                continue
            card_to_play = self.player.hand[index]
            if not card_to_play.playable:
                continue
            if card_to_play.cost > self.player.energy:
                continue
            if card_to_play.attack is not None:
                if card_to_play.aoe is None:
                    self.clear_prompt_lines()
                    prompt = "enter # of enemy to attack"
                    x = maxyx[1] // 2 - len(prompt) // 2
                    self.stdscr.addstr(y, x, prompt)
                    which_enemy = self.stdscr.getch()
                    index = int(chr(which_enemy)) - 1
                    if index >= len(self.enemies) or index < 0:
                        continue
                    target = self.enemies[index]
                    if not target.is_alive():
                        continue
                    raw_dmg = card_to_play.attack
                    dmg = raw_dmg - target.defense
                    if dmg < 0:
                        dmg = 0
                    target.change_hp(-dmg)
                    target.change_defense(-raw_dmg)
                else:
                    dmgs = []
                    for target in self.enemies:
                        if target.is_alive():
                            raw_dmg = card_to_play.attack
                            dmg = raw_dmg - target.defense
                            dmgs.append(dmg)
                            if dmg < 0:
                                dmg = 0
                            target.change_hp(-dmg)
                            target.change_defense(-raw_dmg)
            if card_to_play.defense is not None:
                self.player.change_defense(card_to_play.defense)
            break
        self.player.change_energy(-card_to_play.cost)
        self.player.hand.remove(card_to_play)
        self.player.discard.append(card_to_play)
        return True

    # Returns a list of strings with the damage alerts:
    def enemy_actions(self):
        dmg_alerts = []
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
                    dmg_alerts.append(f"{self.player.name} was struck for {dmg} dmg!")
                if card_to_play.defense is not None:
                    e.change_defense(card_to_play.defense)
                    dmg_alerts.append(f"{e.name} prepares {card_to_play.defense} defense!")
        return dmg_alerts

    def display_battle(self, dmg_alerts):
        self.stdscr.clear()
        maxyx = self.stdscr.getmaxyx()
        
        y = 0
        turn_str = f"Turn {self.turn}:"
        x = maxyx[1] // 2 - len(turn_str) // 2
        self.stdscr.addstr(y, x, turn_str)

        y += 1
        player_str = self.player.stat_str()
        x = maxyx[1] // 2 - len(player_str) // 2
        self.stdscr.addstr(y, x, player_str)

        y += 1
        deck_str = self.player.deck_str()
        x = maxyx[1] // 2 - len(deck_str) // 2
        self.stdscr.addstr(y, x, deck_str)

        hand_str_list = self.get_hand_str_list()
        for entry in hand_str_list:
            x = maxyx[1] // 2 - len(entry) // 2
            y += 1
            self.stdscr.addstr(y, x, entry)

        y += 1
       
        enemy_str_list = self.get_enemy_str_list() 
        for entry in enemy_str_list:
            x = maxyx[1] // 2 - len(entry) // 2
            y += 1
            self.stdscr.addstr(y, x, entry)

        y = constants.PROMPT_LINE + 2
        for entry in dmg_alerts:
            x = maxyx[1] // 2 - len(entry) // 2
            y += 1
            self.stdscr.addstr(y, x, entry)

        self.stdscr.refresh()

    def battle(self): 
        self.player.reset_deck()
        # Player always goes first
        dmg_alerts = []
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
                self.display_battle(dmg_alerts)
                if not self.handle_input():
                    break
            self.player.discard_hand()
            dmg_alerts = self.enemy_actions()
            self.turn += 1
        self.player.reset_deck()

