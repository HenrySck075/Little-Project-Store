import os, sys, time
size = os.get_terminal_size()

print("\n"*size.lines)

sys.stdout.write(f"\033[{size.lines}A")
x,y=(0,0)
dx,dy=(True,True)

move = lambda x,y: sys.stdout.write(f"\033[{x+1};{y+1}H")
a=0
while True:
    if a%600!=0: continue
    x+=(1 if dx else -1)
    y+=(1 if dy else -1)
    if x>size.columns-1: 
        x-=2
        dx=False
    elif x<0: 
        x+=2
        dx=True

    if y>size.lines-1: 
        y-=2
        dy=False
    elif y<0: 
        y+=2
        dy=True
    
    move(x,y)
    sys.stdout.write("o")

    a+=1


