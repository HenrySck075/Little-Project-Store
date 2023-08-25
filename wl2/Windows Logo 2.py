import math
from tkinter import Button, Label, Menu, messagebox, Entry, Text, Canvas,Toplevel,Tk

root = Tk()

canvas = Canvas(root, width=1286, height=745)
#Format: cv2.line(blank_image, start, end, (0,0,0), 2)
pos=(1286/2,745/2)
cmd=Toplevel(root)
cmd.title("Commands")

#config
rotation=0

def typing(*types):
    def func(*args, **kwargs):
        ...

class cmds:
    def __init__(self) -> None:
        self.forward = self.fd
        self.back = self.bk
        self.right = self.rt
        self.left = self.lt

        self.__penup = False

    def __move(self, length):
        global rotation
        x,y=(0,0)
        match rotation:
            case 0: y = -length
            case 90: x = length
            case 180: y = length
            case 270: x = -length
            case _:
                if False: "hi"
                #0 to 90 degrees
                elif 0<rotation and rotation<=45:
                    y = -(length*math.cos(rotation))
                    x = length*math.sin(rotation)
                elif 45<=rotation and rotation<90:
                    y = -(length*math.sin(rotation))
                    x = length*math.cos(rotation)
                #90 to 180 degrees
                elif 90<rotation and rotation<=135:
                    y = length*math.sin(rotation)
                    x = length*math.cos(rotation)
                elif 135<=rotation and rotation<180:
                    y = length*math.cos(rotation)
                    x = length*math.sin(rotation)
                #180 to 270 degrees
                elif 180<rotation and rotation<=225:
                    y = length*math.sin(rotation)
                    x = -(length*math.cos(rotation))
                elif 225<=rotation and rotation<270:
                    y = length*math.cos(rotation)
                    x = -(length*math.sin(rotation))
                #270 to 360 degrees
                elif 270<rotation and rotation<=315:
                    y = -(length*math.sin(rotation))
                    x = -(length*math.cos(rotation))
                elif 315<=rotation and rotation<360:
                    y = -(length*math.cos(rotation))
                    x = -(length*math.sin(rotation))
        if not self.__penup: canvas.create_line(pos[0],pos[1],pos[0]+x,pos[1]+y,tags="line")

    def fd(self, len):
        self.__move(len)

    def bk(self, len):
        self.__move(-len)
    
    def rt(self, rot):
        global rotation
        rotation+=rot

    def lt(self, rot):
        global rotation
        rotation-=rot
        
    def home(self):
        global pos
        pos=(1286/2,745/2)

    def clean(self):
        canvas.delete("line")

    def cs(self):
        self.ct()
        self.home()

    def ht(self):...
    def st(self):...

    def pu(self):
        self.__penup = True
    
    def pd(self):
        self.__penup = False

processor = cmds()

def process_cmd():
    #Visualize the command sent
    content=command.get()
    history.config(state='normal')
    history.insert("insert", f"{content}\n")
    history.config(state='disabled')
    command.delete(0, "end")
    params = content.split(" ")
    if "__" in params[0] or params[0] not in cmds.__dict__:
        history.config(state='normal')
        history.insert("insert", f"I don't know how to {content}\n")
        history.config(state='disabled')
    (getattr(processor, params[0]))( *params[1:])
    # else:

history=Text(cmd, font=("Consolas", 8))
history.pack(fill='both'); history.config(state='disabled')
command=Entry(cmd, font=("Consolas", 8))
command.pack(fill='x'); command.bind("<Return>", lambda x=None: process_cmd())

root.title("Microsoft Windows Logo 2")
root.mainloop()
