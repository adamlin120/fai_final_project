import random

from copy import deepcopy
from game.engine.deck import Deck

def setup_cards():
    return [cid for cid in range(1, 53)]


def build_decks(max_round=20, num_game=5):
    decks = [[] for _ in range(num_game)]
    for game in range(num_game):
        if game % 2 != 0:
            decks[game] = deepcopy(decks[game - 1])
            continue
        for round in range(max_round):
            card_ids = setup_cards()
            random.shuffle(card_ids)
            new_deck = Deck(cheat=True, cheat_card_ids=card_ids) # cheat 要是 True，不然之後可能會被 random shuffle 掉
            decks[game].append(new_deck)
    return decks


if __name__ == '__main__':
    decks = build_decks()
    print(decks)