import random
import sys
from typing import Literal
pattern={
    "vertical": [(0,3,6), (1,4,7), (2,5,8)],
    "horizontal": [(0,1,2), (3,4,5), (6,7,8)],
    "diagonal": [(0,4,8), (3,4,6)]
}
turn=0
board=["" for i in range(9)]
def the_check(text: Literal["x", "o"]):
    v=pattern["vertical"]
    h=pattern["horizontal"]
    d=pattern["diagonal"]
    if ([True, True, True] in [[board[v[o][i]]==text for i in range(3)] for o in range(3)] or
        [True, True, True] in [[board[h[o][i]]==text for i in range(3)] for o in range(3)] or
        [True, True, True] in [[board[d[o][i]]==text for i in range(3)] for o in range(2)]):
        return True
    else: return False

while True:
    if turn==0:
        cell=int(input("Item: "))
        board[cell-1]="x"
        if the_check("x"): print("usr won"); break
        turn+=1
    if turn==1:
        while True:
            opt=random.randrange(0,8)
            if board[opt] != "x" or board[opt] != "o": board[opt]="o"; break
        if the_check("o"): print("com won"); break
        turn-=1
    if not '' in board:print("draw"); break
    sys.stdout.write("\x1b[1A\x1b[2K")
    sys.stdout.write("\x1b[1A\x1b[2K")
    sys.stdout.write("\x1b[1A\x1b[2K")
    sys.stdout.write("\x1b[1A\x1b[2K")
    print(board)


