#import cupy as xp
import numpy as xp
import random
from datetime import datetime as dt

debug = False

# Constants
if debug:
    HELMET = "helmet"
    TEXT = "text"
    SHIRT = "shirt"
    LOGO = "logo"

    UPPER = "upper"
    LOWER = "lower"
else:
    HELMET = 0
    TEXT = 1
    SHIRT = 2
    LOGO = 3

    UPPER = 1
    LOWER = 0

class Card:
    def __init__(self, id, top, right, bottom, left, dir=1):
        self.id = id
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
        self.dir = dir

    def rotate(self):
        return Card(id=self.id,
                    top=self.left,
                    right=self.top,
                    bottom=self.right,
                    left=self.bottom,
                    dir=self.dir+1)


def solve(grid, cards):
    for x in range(0, 3):
        for y in range(0, 3):
            if grid[x, y] == 0:
                for card in cards:
                    if possible(grid,card,x,y):
                        grid[x,y] = card
                        solve(grid, cards)

                        if xp.count_nonzero(grid) == 9:
                            return

                        # Reset
                        grid[x, y] = 0
                # No item fits here
                return
    # We're done!

def possible(grid, card, i, j):
    # Check if card id is already in grid
    for grid_card in grid.flatten():
        if type(grid_card) == int: #Continue if there is no card assigned to this slot yet
            continue

        if (card.id == grid_card.id):
            #if (debug): print('Not possible, card is already in grid')
            return False

    # Validate neighbours
    for _ in range(0, 4):
        if _ == 0:
            x, y = i, j+1
        elif _ == 1:
            x, y, = i+1, j
        elif _ == 2:
            x, y, = i, j-1
        elif _ == 3:
            x, y = i-1, j

        if x<0 or x>2:  # Continue if out of bounds
            continue

        if y < 0 or y > 2:  # Continue if out of bounds
            continue

        grid_card = grid[x, y]
        if grid_card == 0:
            continue

        # Checking relevant position
        if x==i and y>j: # Bottom
            c_side = card.bottom
            gc_side = grid_card.top
        elif x>i and y==j: # Right
            c_side = card.right
            gc_side = grid_card.left
        elif x==i and y<j: # Top
            c_side = card.top
            gc_side = grid_card.bottom
        elif x<i and y==j: # Left
            c_side = card.left
            gc_side = grid_card.right

        if c_side[0] != gc_side[0]:
            #if (debug): print('Not possible, type of side doesnt match')
            return False
        if c_side[1] == gc_side[1]:
            #if (debug): print('Not possible, orientation of side doesnt match')
            return False

    #if (debug): print('possible')
    return True

def instantiate_cards():
    cards = []
    cards.append(Card(0, [LOGO, LOWER], [HELMET, LOWER], [TEXT, UPPER], [HELMET, UPPER]))
    cards.append(Card(1, [TEXT, UPPER], [LOGO, LOWER], [SHIRT, LOWER], [HELMET, UPPER]))
    cards.append(Card(2, [TEXT, UPPER], [HELMET, LOWER], [SHIRT, UPPER], [LOGO, UPPER]))
    cards.append(Card(3, [TEXT, LOWER], [LOGO, LOWER], [SHIRT, UPPER], [SHIRT, UPPER]))
    cards.append(Card(4, [SHIRT, UPPER], [HELMET, LOWER], [TEXT, LOWER], [LOGO, UPPER]))
    cards.append(Card(5, [SHIRT, LOWER], [LOGO, LOWER], [TEXT, UPPER], [HELMET, UPPER]))
    cards.append(Card(6, [SHIRT, LOWER], [LOGO, UPPER], [HELMET, UPPER], [TEXT, UPPER]))
    cards.append(Card(7, [TEXT, UPPER], [HELMET, UPPER], [SHIRT, UPPER], [LOGO, LOWER]))
    cards.append(Card(8, [TEXT, LOWER], [SHIRT, LOWER], [LOGO, LOWER], [HELMET, LOWER]))

    return cards

if __name__ == '__main__':
    cards = instantiate_cards()
    grid = xp.zeros((3, 3), dtype=Card)

    # grid[0, 0] = cards[0]
    # grid[1, 0] = cards[1]
    # grid[2, 0] = cards[2]
    # grid[1, 1] = cards[4]

    # # Check card is already in grid
    # possible(grid, cards[0], 0, 0)
    # possible(grid, cards[0], 1, 0)
    # possible(grid, cards[2], 2, 2)
    #
    # # Check attaching to existing cards
    # possible(grid, cards[3], 0, 1)
    # possible(grid, cards[3], 1, 1)
    # possible(grid, cards[5], 0, 1)

    # Rotate and add all cards
    originals = cards.copy()
    for card in originals:
        for i in range(1, 4):
            cards.append(card.rotate())

    random.seed(131)
    random.shuffle(cards)

    # Solving
    print("Start")
    t1 = dt.now()
    solve(grid, cards)
    time = (dt.now() - t1).total_seconds()
    print("End")
    print("Time (s): " + str(time))

    # Show solution
    for i in range(0, 3):
        for j in range(0, 3):
            print("position: " + str(i) + ", " + str(j))
            print("card id: " + str(grid[i, j].id) + ", dir: " + str(grid[i, j].dir))

