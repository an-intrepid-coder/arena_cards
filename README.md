# Arena Cards

**Version:** 0.0.3

**Description:** I'm a pretty big fan of deck-building games, pool-building games, and deck-building roguelikes. So I decided to make a simple prototype for one, with *Slay the Spire* being the biggest inspiration.

**Installation and Use:** For now, just run `arena_cards.py` with a python interpreter in whatever way is most convenient (for example by running `python arena_cards.py`). If using windows then you will not have the `curses` module installed by default, but you can use [windows-curses](https://pypi.org/project/windows-curses/). **Important:** `arena_cards.py` needs to be an executable file or otherwise have read/write permissions (for example, via `chmod +x arena_cards.py`) for the persistent high-score file to work, although the game can be played either way for the time being.

### **Design Notes:** 
* The pathway through the game's stages is linear, for now. I will include branching paths in a future update. I'm still not sure how long the game will be once it is more fully developed.
* After every battle, 2 possible reward types (out of the entire set of possible reward types, which will grow with the game) are randomly selected for the player to choose from.
* Currently, if a card can be upgraded, it can be upgraded infinitely. It's a trade-off between that and the other options for rewards in any case.
* No save states yet, although there is persistence in the form of a high-score list.
* There is a very limited number of cards for now, and there's a decent chance of the `Basic Area Attack` dropping when the player chooses to `GAIN CARD` after a battle. Many more cards soon to come.
* The enemies let you know what the name of the card they are going to use is, so you can prepare a little. If they are attacking then they will also indicate for how much damage, so the player can prepare their defense cards with decent foreknowledge. 
* Energy refreshes every turn. There will be more mechanics around energy later.
* This is a prototype! It needs many more varieties of enemies, cards, and other features before it is even close. But the core of a good game is here.
* The current interface is put together with the python `curses` module and is a long-term placeholder until I implement a GUI.
