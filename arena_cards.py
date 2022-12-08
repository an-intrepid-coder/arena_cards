#! /usr/bin/python

import card_battle
import player
import constants
from enum import Enum
import random
import card
import utility
import curses

class RewardType(Enum):
    REMOVE_CARD = 0
    UPGRADE_CARD = 1
    GAIN_CARD = 2
    HEAL = 3

class ArenaCards(): 
    def __init__(self):
        self.init_curses()
        self.player = player.Player()
        self.stages_cleared = 0
        self.stage_graph = card_battle.generate_stage_graph(self.player, self.stdscr)
        self.current_stage = None
        self.version = "0.0.2"

    def init_curses(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.curs_set(0)
        # TODO: colors!

    def uninit_curses(self):
        curses.echo()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.endwin()

    def player_wins(self):
        return self.stages_cleared >= constants.NUM_STAGES

    # Returns two reward types in a tuple out of all possible reward types:
    def generate_rewards(self):
        rewards = [RewardType.REMOVE_CARD, RewardType.UPGRADE_CARD, RewardType.GAIN_CARD, RewardType.HEAL]
        random.shuffle(rewards)
        first_pick = rewards.pop()
        second_pick = rewards.pop()
        return (first_pick, second_pick)

    def upgrade_card_loop(self):
        upgradeable = self.player.get_upgradeable_cards()
        page = 0
        draw_divmod = divmod(len(upgradeable), constants.PAGE_SIZE)
        num_pages = draw_divmod[0]
        if draw_divmod[1] > 0:
            num_pages += 1
        while True:
            count = 0
            self.stdscr.clear()
            maxyx = self.stdscr.getmaxyx()
            for i in range(constants.PAGE_SIZE):
                entry_index = i + constants.PAGE_SIZE * page
                if len(upgradeable) > entry_index:
                    entry = upgradeable[entry_index]
                    line = f"({count + 1}) {entry.stat_str()}"
                    x = int(maxyx[1] / 2 - len(line) / 2)
                    self.stdscr.addstr(count, x, line)
                    count += 1
            y = constants.PROMPT_LINE
            prompt = f"(page {page + 1}/{num_pages}) # of card to remove, (e)nd"
            if page > 0:
                prompt += ", (b)ack"
            if page < num_pages - 1:
                prompt += ", (n)ext"
            x = int(maxyx[1] / 2 - len(prompt) / 2)
            self.stdscr.addstr(y, x, prompt)
            user_choice = self.stdscr.getch()
            if user_choice == ord("e"):
                break
            if user_choice == ord("b"): 
                if page > 0:
                    page -= 1
                continue
            if user_choice == ord("n"):
                if page < num_pages - 1:
                    page += 1
                continue
            if not user_choice in range(48, 58):
                continue
            index = int(chr(user_choice)) - 1 + constants.PAGE_SIZE * page
            if len(upgradeable) > entry_index:
                upgradeable[index].upgrade()
            #print(f"REMOVED: {target.stat_str()}") # TODO: Console log?
            break

    #def paged_menu_loop(self): # TODO

    def remove_card_loop(self):
        page = 0
        draw_divmod = divmod(len(self.player.draw), constants.PAGE_SIZE)
        num_pages = draw_divmod[0]
        if draw_divmod[1] > 0:
            num_pages += 1
        while True:
            count = 0
            self.stdscr.clear()
            maxyx = self.stdscr.getmaxyx()
            for i in range(constants.PAGE_SIZE):
                entry_index = i + constants.PAGE_SIZE * page
                if len(self.player.draw) > entry_index:
                    entry = self.player.draw[entry_index]
                    line = f"({count + 1}) {entry.stat_str()}"
                    x = int(maxyx[1] / 2 - len(line) / 2)
                    self.stdscr.addstr(count, x, line)
                    count += 1
            y = constants.PROMPT_LINE
            prompt = f"(page {page + 1}/{num_pages}) # of card to remove, (e)nd"
            if page > 0:
                prompt += ", (b)ack"
            if page < num_pages - 1:
                prompt += ", (n)ext"
            x = int(maxyx[1] / 2 - len(prompt) / 2)
            self.stdscr.addstr(y, x, prompt)
            user_choice = self.stdscr.getch()
            if user_choice == ord("e"):
                break
            if user_choice == ord("b"): 
                if page > 0:
                    page -= 1
                continue
            if user_choice == ord("n"):
                if page < num_pages - 1:
                    page += 1
                continue
            if not user_choice in range(48, 58):
                continue
            index = int(chr(user_choice)) - 1 + constants.PAGE_SIZE * page
            if len(self.player.draw) > index:
                target = self.player.draw[index]
                self.player.draw.remove(target)
                #print(f"REMOVED: {target.stat_str()}") # TODO: Console log?
            break

    def gain_card_loop(self):
        self.stdscr.clear()
        maxyx = self.stdscr.getmaxyx()
        count = 0
        choices = [card.BasicAttack(), card.BasicDefend()] # for now
        if random.random() <= constants.BASIC_AOE_DROP_CHANCE:
            choices.append(card.BasicAreaAttack())
        for entry in choices:
            line = f"({count + 1}) {entry.stat_str()}"
            x = int(maxyx[1] / 2 - len(line) / 2)
            self.stdscr.addstr(count, x, line)
            count += 1
        while True:
            prompt = "# of card to gain or (e)nd"
            x = int(maxyx[1] / 2 - len(prompt) / 2)
            self.stdscr.addstr(count, x, prompt)
            user_choice = self.stdscr.getch()
            if user_choice == ord("e"):
                break
            if not user_choice in range(48, 58):
                continue
            index = int(chr(user_choice)) - 1
            self.player.draw.append(choices[index])
            # print(f"GAINED: {choices[index].stat_str()}") # TODO: Console log?
            break

    def rewards_loop(self):
        self.stdscr.clear()
        maxyx = self.stdscr.getmaxyx()
        rewards = self.generate_rewards()
        while True:
            reward_choice_prompt = f"(1) {rewards[0].name} (2) {rewards[1].name} or (e)nd: "
            y = int(maxyx[0] / 2)
            x = int(maxyx[1] / 2 - len(reward_choice_prompt) / 2)
            self.stdscr.addstr(y, x, reward_choice_prompt)
            reward_choice = self.stdscr.getch()
            if reward_choice == ord("e"):
                break
            elif not (reward_choice == ord("1") or reward_choice == ord("2")):
                #print("Invalid input!") # TODO: Console log?
                continue
            pick = rewards[int(chr(reward_choice)) - 1]
            if pick == RewardType.UPGRADE_CARD:
                self.upgrade_card_loop()
            elif pick == RewardType.REMOVE_CARD:
                self.remove_card_loop()
            elif pick == RewardType.GAIN_CARD:
                self.gain_card_loop() 
            elif pick == RewardType.HEAL:
                heal_amt = utility.generate_fuzzed_value(constants.BASE_HEAL_AMOUNT, constants.HEAL_FUZZ_MULTIPLIER)
                self.player.change_hp(heal_amt)
                # print(f"{self.player.name} heals for {heal_amt} HP!") # TODO: Console log?
            break

    def display_title(self):
        self.stdscr.clear()
        title = f"Arena Cards ({self.version})"
        maxyx = self.stdscr.getmaxyx()
        y = int(maxyx[0] / 2)
        x = int(maxyx[1] / 2 - len(title) / 2)
        self.stdscr.addstr(y, x, title)
        prompt = "< any key to continue >"
        y += 1
        x = int(maxyx[1] / 2 - len(prompt) / 2)
        self.stdscr.addstr(y, x, prompt)
        self.stdscr.refresh()
        self.stdscr.getch()

    def display_stage_graph(self):
        maxyx = self.stdscr.getmaxyx()
        self.stdscr.clear()
        
        y = 1
        prompt = f"SPACE KEY to begin stage #{self.stages_cleared + 1}"
        x = int(maxyx[1] / 2 - len(prompt) / 2)
        self.stdscr.addstr(y, x, prompt)

        # This will be very different when branching paths are implemented
        stage_graph_str = ""
        for i in range(constants.NUM_STAGES):
            if self.stages_cleared > i:
                stage_graph_str += "[+]"
            else:
                stage_graph_str += "[ ]"
            if i < constants.NUM_STAGES - 1:
                stage_graph_str += "--"
        y = int(maxyx[0] / 2)
        x = int(maxyx[1] / 2 - len(stage_graph_str) / 2)
        self.stdscr.addstr(y, x, stage_graph_str)

        self.stdscr.refresh()

        while True:
            user_input = self.stdscr.getch()
            if user_input == constants.ASCII_SPACE:
                break

    def display_victory(self):
        maxyx = self.stdscr.getmaxyx()
        self.stdscr.clear()
        prompt = "You win! Any key to exit game. (placeholder)"
        y = int(maxyx[0] / 2)
        x = int(maxyx[1] / 2 - len(prompt) / 2)
        self.stdscr.addstr(y, x, prompt)
        self.stdscr.refresh()
        self.stdscr.getch()

    def play(self):
        self.display_title()
        self.current_stage = self.stage_graph[0]
        while not self.player_wins():
            self.display_stage_graph()
            check = self.player.total_cards_amt()
            self.current_stage.contents.battle()
            assert check == self.player.total_cards_amt()
            self.stages_cleared += 1
            self.rewards_loop()
            self.current_stage = self.current_stage.next_node
        self.display_victory()

if __name__ == "__main__":
    try:
        game = ArenaCards()
        game.play()
    finally:
        game.uninit_curses()

