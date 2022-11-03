#+-<>[].,e
import sys
import time

from termcolor import colored
cells = ["0", "0", "0", "0", "0", "0", "0", "0"]
#         1    2    3    4    5    6    7    8
txtcells = []
abc = " !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
alphabetidx = list(abc)
for i in range(32):
    alphabetidx.insert(0, "")
print("brainfuck code here (Ctrl-D to continue):\n")
n = []
while True:
    try:
        line = input()
    except EOFError:
        break
    n.append(line)
cod = n
out = "0"
loop = 0
moarlist = []
cellid = 0
bracketidx = 0
loopcheck = 0
theCellIsTheFirstCellSoDontMoveLeftPls = 0
selcell = cells[0]
delay = float(input("delay between code execution (0 to ignore): "))
def exec(code, inLoop=0):
    #global declaration, why
    global cellid, selcell, out, delay, loop, moarlist, bracketidx, afloop, loopcheck, eoloop
    codeinput = list(code)
    outtxt = ''.join(txtcells)
    #execute   
    for i in codeinput:
        if i == "+":
            selcell = str(int(cells[cellid])+1)
            cells[cellid] = selcell
        if i == "-":
            if selcell != "0":
                selcell = str(int(cells[cellid])-1)
                cells[cellid] = selcell
            if selcell == "0":
                continue
        if i == "<":
            if cellid == 0:
                continue
            if cellid != 0:
                cellid = cellid-1
        if i == ">":
            if cellid == 7:
                continue
            if cellid != 7:
                cellid = cellid+1
        if i == "[":
            # inLoop = re.search('{ob}(.*){cb}'.format(ob=openbrackets[anotherint], cb=closedbrackets[anotherint]), ''.join(variable2))
            moarlist = []
            loop = cellid
            loopcheck = 0
            if inLoop == 0:
                afloop = [u for u, y in enumerate(codeinput) if y == '['][bracketidx]
            # print(inLoop.group(1))
        if i == "]":
            if inLoop == 0:
                eoloop = [u for u, y in enumerate(codeinput) if y == ']'][bracketidx]
                for j in range(afloop+1, eoloop+1):
                    moarlist.append(codeinput[j])
            if int(cells[loop]) != 0:
                exec(moarlist, 1)
            if int(cells[loop]) == 0:
                if loopcheck == 0:
                    loopcheck = 1
                    bracketidx = bracketidx+1
                if loopcheck == 1:
                    pass
        if i == ",":
            cells[cellid] = input("input params detected, gimme input: ")
        if i == ".":
            out = cells[cellid]
            seltxt = alphabetidx[int(cells[cellid])]
            txtcells.append(seltxt)
            outtxt = ''.join(txtcells)
        if i == "e":
            break
        else:
            pass
        cellsValueReport = "Cells value: ", ' '.join(cells)
        numberOutputReport = "Number output: ", out
        textOutputReport = "\nText output: ", outtxt
        currentCellReport = "Current cell: ", str(cellid+1)
        for i in range(2):
            sys.stdout.write("\x1b[1A\x1b[2K")
        line = colored(''.join(cellsValueReport), "magenta"), " | ", colored(''.join(currentCellReport), "cyan" ), " | ", colored(''.join(numberOutputReport), "green"), " | ", colored(''.join(textOutputReport), "red")#, " | Current idx: ", str(bracketidx), " | Code: ", ''.join(codeinput), "            " 
        print(''.join(line))
        if delay == 0:
            pass
        else:
            time.sleep(delay)
exec(cod)
print("\n")