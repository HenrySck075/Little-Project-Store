import sys
import time
from collections import deque

spaces = 0
reverse = 0
queue = deque([], 16)
loop = 0
while loop == 0:
    space = []
    for p in range(spaces):
        space.append(" ")
    if spaces == 0:
        reverse = 0
    if spaces == 24:
        reverse = 1
    if reverse == 0:
        spaces = spaces+1
    if reverse == 1:
        spaces = spaces-1
    time.sleep(0.06)
    s = ''.join([''.join(space), "please read the pins"])
    for _ in range(len(queue)):
        sys.stdout.write("\x1b[1A\x1b[2K")
    queue.append(s)
    for i in range(len(queue)):
        sys.stdout.write(queue[i] + "\n")