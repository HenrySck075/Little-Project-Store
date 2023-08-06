import random, sys, os
from colorama import Fore, Cursor
#TODO: change all "col" to "row" and vice versa
diff = {
    3: "Easy",
    5: "Normal",
    7: "Hard",
    9:  "Easy Demon",
    12: "Extreme Demon"
}
diffStr = ""

rowRes=[]
rowToggle=[]
colRes=[]
colToggle=[]

ten = range(1,10)
size = 3

def sprint(arg,endl='\n'):
    sys.stdout.write(arg)
    if endl != "": sys.stdout.write(endl)

def initRepetive(v, times=2):
    a=[]
    for i in range(size):
        if times > 1: a.append(initRepetive(v, times-1))
        else: a.append(v)
    return a

def tdprint(arr):
    print("[")
    for i in arr:
        print("    ", i)
    print("]")

def colConcat(c):
    res = 0 
    for idx,i in enumerate(board[c]):
        if toggler[c][idx]: res+=i
    return res

def rowConcat(r):
    res = 0
    for idx,i in enumerate(board90[r]):
        if toggler[idx][r]: res+=i
    return res

size = int(input("board size (max 12, min 3): "))
highestSize=size
a = range(size)
board = []
board90 = []
toggler = []

def init():
    global size, board90, board, toggler, a, ten, rowRes, rowToggle, colRes, colToggle, diff, diffStr
    for i in diff:
        if size >= i: diffStr = diff[i]
    board = initRepetive(0)
    board90 = initRepetive(0)
    toggler = initRepetive(True)
    rowRes=[]
    rowToggle=[]
    colRes=[]
    colToggle=[]

    a = range(size)
    if size > 12: size = 12
    if size < 3: size = 3

    for c in a:
        for r in a:
            v = random.choice(ten)
            board[c][r] = v
            board90[r][c] = v
        
        thing = list(a)
        for _ in range(random.choice(range(1,size-1))):
            res = random.choice(thing)
            toggler[c][res] = False
            del thing[thing.index(res)]


    for c in a:
        colRes.append(colConcat(c))
        colToggle.append(c)

    for r in a:
        rowRes.append(rowConcat(r))
        rowToggle.append(r)

    toggler = initRepetive(True)

    #tdprint(board)
    #tdprint(board90)
    print("Difficulty: "+diffStr)

init()
enum = enumerate
def draw(h):

    [sprint(Cursor.UP(),'') for _ in range(h)]
    for idx,i in enum(board):
        print("----"*size+"-")
        col = [f"| {Fore.CYAN if toggler[idx][idx2] else Fore.RED}{b}{Fore.RESET} " for idx2,b in enum(i)]
        color = Fore.RESET
        if colConcat(idx) != colRes[idx]:
            color = Fore.LIGHTBLACK_EX
            colToggle[idx] = False
        else:
            colToggle[idx] = True
        col.append(f"| {color}{colRes[idx]}{Fore.RESET}")
        sprint("".join(col))
    print("----"*size+"-")
    row = []
    for idx,i in enum(rowRes):
        color = Fore.RESET
        if rowConcat(idx) != rowRes[idx]: 
            color = Fore.LIGHTBLACK_EX
            rowToggle[idx] = False
        else:
            rowToggle[idx] = True
        row.append(f"  {color}{i}{Fore.RESET}{' ' if len(str(i)) == 1 else ''}")
    sprint("".join(row))
    print("            ")
    sprint(Cursor.UP(),'')

draw(0)
while True:
    if all(rowToggle) and all(colToggle):
        sprint(f"{Fore.GREEN}You win!")
        break
    d = input(">>> ").split()
    if len(d) == 1: d.append("")
    c,r = d

    que = 0
    match c:
        case "reset":
            toggler = initRepetive(True)
        case "new":
            [sprint(Cursor.UP(),'') for _ in range(size*2+4)]
            [print(" "*(os.get_terminal_size().columns)) for _ in range(size*2+4)]
            [sprint(Cursor.UP(),'') for _ in range(size*2+4)]
            if r != "":
                size = int(r)
            init()
            if size > highestSize:
                que = 2
                highestSize = size
            [sprint(Cursor.DOWN(),'') for _ in range(size*2+3)] # wacky cursor manip
        case _:
            try:c,r = int(c),int(r)
            except: continue

            toggler[c-1][r-1] = not toggler[c-1][r-1]

    draw(size*2+3-que)
