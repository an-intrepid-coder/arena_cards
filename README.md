# Arena Cards

**Version:** 0.0.1

**Description:** I'm a pretty big fan of deck-building games, pool-building games, and deck-building roguelikes. So I decided to make a simple prototype for one, with *Slay the Spire* being the biggest inspiration.

**Installation and Use:** For now, just run arena_cards.py with a python interpreter in whatever way is most convenient (for example by running `python arena_cards.py`). The next version will probably include a GUI and have different installation instructions.

### **Design Notes:** 
* The pathway through the game's stages are linear, for now. I will include branching paths in a future update.
* After every battle, 2 possible reward types (out of the entire set of possible reward types, which will grow with the game) are randomly selected for the player to choose from.
* Currently, if a card can be upgraded, it can be upgraded infinitely. It's a trade-off between that and the other options for rewards in any case.
* The current interface is put together with Python's built-in `print()` and `input()` functions. This was just for the initial prototype, and I will implement a GUI soon. 
* No persistence of any kind just yet, although I will probably implement at least high-score keeping soon (and save states not long afterwards).
* There is a very limited number of cards for now, and there's a decent chance of the `Basic Area Attack` dropping when the player chooses to `GAIN CARD` after a battle. Many more cards soon to come.
* The enemies let you know what the name of the card they are going to use is, so you can prepare a little. If they are attacking then they will also indicate for how much damage, so the player can prepare their defense cards with decent foreknowledge. 
* Energy refreshes every turn. There will be more mechanics around energy later.
* This is a prototype! It needs many more varieties of enemies, cards, and other features before it is even close. But the core of a good game is here.
