#! /usr/bin/python

import card_battle
import player
import constants

class ArenaCards: # I suppose in the Kivy version this will subclass App!
    def __init__(self):
        self.player = player.Player()
        self.stages_cleared = 0
        self.stage_graph = card_battle.generate_stage_graph(self.player)
        self.current_stage = None

    def player_wins(self):
        return self.stages_cleared >= constants.NUM_STAGES

    def play(self):
        self.current_stage = self.stage_graph[0]
        while not self.player_wins():
            input(f"ENTER to begin stage #{self.stages_cleared + 1}")
            self.current_stage.contents.battle()
        print("You beat every stage!")

if __name__ == "__main__":
    game = ArenaCards()
    game.play()

