#code = print("brainfuck code here (Ctrl-D to continue):\n")

def bfexec(c:str):
    cells = [0]*30_000
    idx=0
    pointer=0
    ignore = -1
    loops = []
    while True:
        if idx==len(c): break
        match c[idx]:
            case "+": cells[pointer]+=1
            case "-": cells[pointer]-=1
            case "<": pointer = (pointer-1)%30001
            case ">": pointer = (pointer+1)%30001
            case ".": 
                print(chr(cells[pointer]),end="")
            case ",": cells[pointer] = int(input("Input cell: "))
            case "[": 
                ignore+=1
                loops.append(idx)
            case "]":
                if cells[pointer]==0:
                    del loops[ignore]
                    ignore-=1
                else:
                    idx = loops[ignore]
        idx+=1
        

bfexec("++++[->++++++++>++++++++<<]>>[->+++<]>++++++++.+.<<.>>++++.++.--.")