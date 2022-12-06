#! /usr/bin/python

import card_battle
import player
import constants
from enum import Enum
import random
import card
import utility

class RewardType(Enum):
    REMOVE_CARD = 0
    UPGRADE_CARD = 1
    GAIN_CARD = 2
    HEAL = 3

class ArenaCards: # I suppose in the Kivy version this will subclass App!
    def __init__(self):
        self.player = player.Player()
        self.stages_cleared = 0
        self.stage_graph = card_battle.generate_stage_graph(self.player)
        self.current_stage = None

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
        while True:
            count = 1
            for entry in upgradeable:
                print(f"({count}) {entry.stat_str()}")
                count += 1
            user_choice = input("# of card to upgrade or (e)nd: ")
            if user_choice == "e":
                break
            if not user_choice.isdecimal():
                print("Invalid input!")
                continue
            index = int(user_choice) - 1
            upgradeable[index].upgrade()
            print(f"UPGRADED: {upgradeable[index].stat_str()}")
            break

    def remove_card_loop(self):
        count = 1
        for entry in self.player.draw:
            print(f"({count}) {entry.stat_str()}")
            count += 1
        while True:
            user_choice = input("# of card to remove or (e)nd: ")
            if user_choice == "e":
                break
            if not user_choice.isdecimal():
                print("Invalid input!")
                continue
            index = int(user_choice) - 1
            target = self.player.draw[index]
            self.player.draw.remove(target)
            print(f"REMOVED: {target.stat_str()}")
            break

    def gain_card_loop(self):
        count = 1
        choices = [card.BasicAttack(), card.BasicDefend()] # more to come
        if random.random() <= constants.BASIC_AOE_DROP_CHANCE:
            choices.append(card.BasicAreaAttack())
        for entry in choices:
            print(f"({count}) {entry.stat_str()}")
            count += 1
        while True:
            user_choice = input("# of card to gain or (e)nd: ")
            if user_choice == "e":
                break
            if not user_choice.isdecimal():
                print("Invalid input!")
                continue
            index = int(user_choice) - 1
            self.player.draw.append(choices[index])
            print(f"GAINED: {choices[index].stat_str()}")
            break

    def rewards_loop(self):
        rewards = self.generate_rewards()
        while True:
            reward_choice = input(f"(1) {rewards[0].name} (2) {rewards[1].name} or (e)nd: ")
            if reward_choice == "e":
                break
            elif not (reward_choice == "1" or reward_choice == "2"):
                print("Invalid input!")
                continue
            pick = rewards[int(reward_choice) - 1]
            if pick == RewardType.UPGRADE_CARD:
                self.upgrade_card_loop()
            elif pick == RewardType.REMOVE_CARD:
                self.remove_card_loop()
            elif pick == RewardType.GAIN_CARD:
                self.gain_card_loop()
            elif pick == RewardType.HEAL:
                heal_amt = utility.generate_fuzzed_value(BASE_HEAL_AMOUNT, HEAL_FUZZ_MULTIPLIER)
                self.player.change_hp(heal_amt)
                print(f"{self.player.name} heals for {heal_amt} HP!")
            break

    def play(self):
        self.current_stage = self.stage_graph[0]
        while not self.player_wins():
            input(f"ENTER to begin stage #{self.stages_cleared + 1}")
            self.current_stage.contents.battle()
            self.stages_cleared += 1
            self.rewards_loop()
            self.current_stage = self.self.current_stage.next_node
        print("You beat every stage!")

if __name__ == "__main__":
    game = ArenaCards()
    game.play()

