import os
import threading
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from typing import Literal, Tuple
from PIL import Image

filetypes={
    '*.*'   : "All files",
    '*.png' : "Portable Network Graphics (.png)", 
    '*.jpg' : "Joint Photographic Experts Group (.jpg)", 
    '*.jgeg': "Joint Photographic Experts Group (.jpeg)", 
    '*.tiff': "Tagged Image File Format (.tiff)",
    '*.webp': "WebP Image Format (.webp)", 
    '*.svg' : "Scalable Vector Graphics (.svg)", 
    '*.apng': "Animated PNG (.apng)", 
    '*.gif' : "Graphics Interchange Format (.gif)", 
    '*.bmp' : "Bitmap Image (.bmp)", 
    '*.heif': "High Efficiency Image File (.heif)", 
    '*.jpe' : "Joint Photographic Experts Group (.jpe)", 
    '*.jfif': "Joint Photographic Experts Group (.jfif)", 
    '*.jfi' : "Joint Photographic Experts Group (.jfi)"
}
r=Tk()
r.title("Light Image Conversion")
Canvas(r, width=200, height=5).pack()
Label(r, text="Choose an image or folder").pack()
h=Frame(r, borderwidth=0)
Button(h, text="Images", command=lambda x=None: o(type='Files')).pack(side=LEFT)
Button(h, text="Folder", command=lambda x=None: o(type='Folder')).pack()
Label(r, text="Convert from").pack()
extfrom=StringVar()
OptionMenu(r, extfrom, *[g.replace("*.", "") for g in filetypes]).pack()
def o(type: Literal['Files', 'Folder']):
    filelist=()
    match type:
        case "Files":
            files=filedialog.askopenfilenames(title="Open multiple files...", parent=r, filetypes=[(filetypes[a], a) for a in filetypes.keys()])
            if files == '' or files == (): return
            filelist=tuple([i for i in os.listdir(files) if os.path.isfile(os.path.join(files, i)) and i.split(".")[-1] == extfrom])
        case "Folder":
            folder=filedialog.askdirectory(title="Open folder..", mustexist=True, parent=r)
            if folder == '': return
            filelist=tuple([i for i in os.listdir(folder) if os.path.isfile(os.path.join(folder, i)) and i.split(".")[-1] == extfrom])
            os.chdir(folder)
    Label(r, text="Files:").pack()
    listbox=Listbox(r); listbox.pack(expand=True,fill="both")
    scroll=Scrollbar(listbox); scroll.pack(side = RIGHT, fill = BOTH)
    listbox.config(yscrollcommand=scroll.set)
    scroll.config(command = listbox.yview)
    for f in filelist:
        listbox.insert(END, f)
    Label(r, text="Convert to").pack()
    extto=StringVar()
    OptionMenu(r, extto, *[g.replace("*.", "") for g in filetypes]).pack()
    Button(r, text="Convert", command=lambda x=None, y=None: convert(extfrom.get(), extto.get(), filelist)).pack()

def convert(_from, _to, files): 
    r.title("Processing... Please do not close this window")
    iables=locals()
    for c in r.winfo_children():
        try:
            c.configure(state="disabled")
        except:pass
    match=[]
    for f in files:
        exten = f.split(".")
        bef=''.join([".", exten[-1]])
        aft=f".{_to}"
        if bef != aft and bef == f".{_from}":
            match.append(f)
    for shards in range(6): iables[f"list{shards+1}"]=[files[m] for m in range(len(files)) if m%6==shards]
    for shards in range(6): threading.Thread(target=actualconvertfr, args=(_from, _to, iables[f"list{shards+1}"])).start()
    while True:
        if threading.active_count() == 0: 
            for c in r.winfo_children():
                try:
                    c.configure(state="normal")
                except:pass
            r.title("Light Image Conversion")
            break

def actualconvertfr(_from, _to, files: Tuple[str]):
    for f in files:
        img=Image.open(f)
        exten = f.split(".")
        bef=''.join([".", exten[-1]])
        aft=f".{_to}"
        if bef != aft and bef == f".{_from}":
            if _to in ["jpg", "jpeg", "jfif", "jfi"]:
                im = img.convert('RGB')
            else: im=img
            temp=f.replace(bef, aft)
            im.save(temp)
            os.remove(f)
h.pack()
r.mainloop()
