#! /usr/bin/python

import player
import random
import utility
import enemy

if __name__ == "__main__":
    p = player.Player()
    p.print_deck()
    b = enemy.Brawler()
    print(b.stat_str())

