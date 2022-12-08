#! /usr/bin/python

import card_battle
import player
import constants
from enum import Enum
import random
import card
import utility
import curses
import stage_graph
import enemy

class RewardType(Enum):
    REMOVE_CARD = 0
    UPGRADE_CARD = 1
    GAIN_CARD = 2
    HEAL = 3
    MAX_HP = 4

class ArenaCards(): 
    def __init__(self):
        self.init_curses()
        self.player = player.Player()
        self.stages_cleared = 0
        self.stage_graph = self.generate_stage_graph()
        self.current_stage = None
        self.version = "0.0.3"
        self.enemies_defeated = 0

    def generate_stage_graph(self):
        root = stage_graph.StageGraphNode(card_battle.CardBattle(self.player, enemy.generate_enemies(stage=1), self), None, None)
        graph = [root]
        for i in range(constants.NUM_STAGES):
            stage_level = i + 1
            next_stage = card_battle.CardBattle(self.player, enemy.generate_enemies(stage_level), self)
            next_node = stage_graph.StageGraphNode(next_stage, graph[i], None)
            graph[i].next_node = next_node
            graph.append(next_node)
        return graph

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

    def check_game_over(self):
        if not self.player.is_alive():
            maxyx = self.stdscr.getmaxyx()
            self.stdscr.clear()
            prompt = "GAME OVER (any key to exit)"
            y = maxyx[0] // 2
            x = maxyx[1] // 2 - len(prompt) // 2
            self.stdscr.addstr(y, x, prompt)
            self.stdscr.refresh()
            self.stdscr.getch()
            exit()

    def player_wins(self):
        return self.stages_cleared >= constants.NUM_STAGES

    # Returns two reward types in a tuple out of all possible reward types:
    def generate_rewards(self):
        rewards = [
            RewardType.REMOVE_CARD, RewardType.UPGRADE_CARD, RewardType.GAIN_CARD, RewardType.HEAL,
            RewardType.MAX_HP,
        ]
        random.shuffle(rewards)
        first_pick = rewards.pop()
        second_pick = rewards.pop()
        return (first_pick, second_pick)

    def paged_menu_loop(self, menu_items, context_str, action):
        # menu_items is a list of card references
        # action is a function that takes a card and does something to it
        page = 0
        draw_divmod = divmod(len(menu_items), constants.PAGE_SIZE)
        num_pages = draw_divmod[0]
        if draw_divmod[1] > 0:
            num_pages += 1
        while True:
            count = 0
            self.stdscr.clear()
            maxyx = self.stdscr.getmaxyx()
            for i in range(constants.PAGE_SIZE):
                entry_index = i + constants.PAGE_SIZE * page
                if len(menu_items) > entry_index:
                    entry = menu_items[entry_index]
                    line = f"({count + 1}) {entry.stat_str()}"
                    x = maxyx[1] // 2 - len(line) // 2
                    self.stdscr.addstr(count, x, line)
                    count += 1
            y = constants.PROMPT_LINE
            prompt = f"(page {page + 1}/{num_pages}) # of card to {context_str}, (e)nd"
            if page > 0:
                prompt += ", (b)ack"
            if page < num_pages - 1:
                prompt += ", (n)ext"
            x = maxyx[1] // 2 - len(prompt) // 2
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
            if len(menu_items) > entry_index:
                action(menu_items[index])
            break

    def rewards_loop(self):
        self.stdscr.clear()
        maxyx = self.stdscr.getmaxyx()
        rewards = self.generate_rewards()
        while True:
            reward_choice_prompt = f"(1) {rewards[0].name} (2) {rewards[1].name} or (e)nd: "
            y = maxyx[0] // 2
            x = maxyx[1] // 2 - len(reward_choice_prompt) // 2
            self.stdscr.addstr(y, x, reward_choice_prompt)
            reward_choice = self.stdscr.getch()
            if reward_choice == ord("e"):
                break
            elif not (reward_choice == ord("1") or reward_choice == ord("2")):
                continue
            pick = rewards[int(chr(reward_choice)) - 1]
            if pick == RewardType.UPGRADE_CARD:
                self.paged_menu_loop(self.player.get_upgradeable_cards(), "upgrade", lambda x: x.upgrade())
            elif pick == RewardType.REMOVE_CARD:
                self.paged_menu_loop(self.player.draw, "remove", lambda x: self.player.draw.remove(x))
            elif pick == RewardType.GAIN_CARD:
                self.paged_menu_loop(card.generate_gain_card_choices(), "gain", lambda x: self.player.draw.append(x))
            elif pick == RewardType.HEAL:
                heal_amt = utility.generate_fuzzed_value(constants.BASE_HEAL_AMOUNT, constants.HEAL_FUZZ_MULTIPLIER)
                self.player.change_hp(heal_amt)
            elif pick == RewardType.MAX_HP:
                hp_amt = utility.generate_fuzzed_value(constants.BASE_HEAL_AMOUNT, constants.HEAL_FUZZ_MULTIPLIER)
                self.player.max_hp += hp_amt
                self.player.change_hp(hp_amt)
            break

    def display_title(self):
        self.stdscr.clear()
        title = f"Arena Cards ({self.version})"
        maxyx = self.stdscr.getmaxyx()
        y = maxyx[0] // 2
        x = maxyx[1] // 2 - len(title) // 2
        self.stdscr.addstr(y, x, title)
        prompt = "< any key to continue >"
        y += 1
        x = maxyx[1] // 2 - len(prompt) // 2
        self.stdscr.addstr(y, x, prompt)
        self.stdscr.refresh()
        self.stdscr.getch()

    def display_stage_graph(self):
        maxyx = self.stdscr.getmaxyx()
        self.stdscr.clear()
        
        y = 1
        prompt = f"SPACE KEY to begin stage #{self.stages_cleared + 1} or view (d)eck"
        x = maxyx[1] // 2 - len(prompt) // 2
        self.stdscr.addstr(y, x, prompt)

        stage_graph_str_list = ["" for x in range(constants.NUM_STAGES // 10)]
        index = 0
        count = 0
        while count < constants.NUM_STAGES:
            if count > 0 and count % 10 == 0:
                index += 1
            if self.stages_cleared > count:
                stage_graph_str_list[index] += "[+]"
            else:
                stage_graph_str_list[index] += "[ ]"
            if count < constants.NUM_STAGES - 1:
                stage_graph_str_list[index] += "--"
            count += 1
        y = maxyx[0] // 2 - 1
        for stage_graph_str in stage_graph_str_list:
            x = maxyx[1] // 2 - len(stage_graph_str) // 2
            self.stdscr.addstr(y, x, stage_graph_str)
            y += 1
            
        self.stdscr.refresh()

        while True:
            user_input = self.stdscr.getch()
            if user_input == constants.ASCII_SPACE:
                break
            elif user_input == ord("d"):
                self.paged_menu_loop(self.player.draw, "", lambda x: None)
                break

    def display_victory(self):
        maxyx = self.stdscr.getmaxyx()
        self.stdscr.clear()
        prompt = "You win! Any key to exit game. (placeholder)"
        y = maxyx[0] // 2
        x = maxyx[1] // 2 - len(prompt) // 2
        self.stdscr.addstr(y, x, prompt)
        self.stdscr.refresh()
        self.stdscr.getch()

    def play(self):
        self.display_title()
        self.current_stage = self.stage_graph[0]
        while not self.player_wins():
            self.display_stage_graph()
            self.current_stage.contents.battle()
            self.check_game_over()
            self.stages_cleared += 1
            self.rewards_loop()
            self.current_stage = self.current_stage.next_node
        self.display_victory()

if __name__ == "__main__":
    game = ArenaCards()
    try:
        game.play()
    finally:
        game.uninit_curses()

