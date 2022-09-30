import tkinter
import cv2
from tkinter import Button, Label, Menu, messagebox, Entry, Text
import numpy as np
blank_image = np.zeros((745,1286,3), np.uint8)
blank_image[:,0:1286] = (255,255,255)
#Format: cv2.line(blank_image, start, end, (0,0,0), 2)
start=(1286/2,745/2)
cmd=tkinter.Tk()
cmd.title("Commands")

#config
rotation=0

def process_cmd():
    #Visualize the command sent
    content=command.get()
    history.config(state='normal')
    history.insert(tkinter.INSERT, f"{content}\n")
    history.config(state='disabled')
    command.delete(0, "end")
    if "fd " in content:
        pass
    else:
        history.config(state='normal')
        history.insert(tkinter.INSERT, f"I don't know how to {content}\n")
        history.config(state='disabled')

history=Text(cmd, font=("Consolas", 8))
history.pack(fill='both'); history.config(state='disabled')
command=Entry(cmd, font=("Consolas", 8))
command.pack(fill='x'); command.bind("<Return>", lambda x=None: process_cmd())

cv2.imshow("Microsoft Windows Logo 2", blank_image)
cmd.mainloop()
