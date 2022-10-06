import json, os, re, traceback
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

os.chdir(os.path.dirname(os.path.realpath(__file__)))
def BaseTkInstance():
    r = tk.Tk()
    r.title("0-budget Text Editor. untitled")
    return r


class LineCounter:
    class CustomText(tk.Text):
        def __init__(self, *args, **kwargs):
            tk.Text.__init__(self, *args, **kwargs)

            # create a proxy for the underlying widget
            self._orig = self._w + "_origi"
            self.tk.call("rename", self._w, self._orig)
            self.tk.createcommand(self._w, self._proxy)

        def _proxy(self, *args):
            # avoid error when copying
            if args[0] == 'get' and (args[1] == 'sel.first' and args[2] == 'sel.last') and not self.tag_ranges('sel'): return

            # avoid error when deleting
            if args[0] == 'delete' and (args[1] == 'sel.first' and args[2] == 'sel.last') and not self.tag_ranges('sel'): return
            
            cmd = (self._orig,) + args
            result = self.tk.call(cmd)
            
            if (args[0] in ("insert", "replace", "delete") or
                args[0:3] == ("mark", "set", "insert") or
                args[0:2] == ("xview", "moveto") or
                args[0:2] == ("xview", "scroll") or
                args[0:2] == ("yview", "moveto") or
                args[0:2] == ("yview", "scroll")
            ):
                self.event_generate("<<Change>>", when="now")
            if args[0] in ("insert", "replace", "delete"):
                self.event_generate('<<TextModified>>')


            return result

    class TextLineNumbers(tk.Canvas):
        def __init__(self, *args, **kwargs):
            self.variables=vars()
            self.index="0"
            tk.Canvas.__init__(self, *args, **kwargs)
            self.variables[f"textwidget{self.index}"] = None

        def attach(self, text_widget):
            self.variables[f"textwidget{self.index}"] = text_widget
        
        def sync_index(self, index):
            self.index = index
        
        def redraw(self, *args):
            '''redraw line numbers'''
            self.delete("all")

            i = self.variables[f"textwidget{self.index}"].index("@0,0")
            while True :
                dline= self.variables[f"textwidget{self.index}"].dlineinfo(i)
                if dline is None: break
                y = dline[1]
                linenum = str(i).split(".")[0]
                self.create_text(2,y,anchor="nw", text=linenum)
                i = self.variables[f"textwidget{self.index}"].index("%s+1line" % i)


tab=ttk.Notebook
class Window:
    def __init__(self):
        self.r = BaseTkInstance()
        self.r.protocol("WM_DELETE_WINDOW", self.on_window_close)
        self.index="-1"
        self.tabindex="-1"
        self.variables={}
        self.filename = "untitled-1"
        self.dirname = ""
        self.fileobj = {}
        self.presave_content={}
        self.saves: dict = json.load(open("cursorpos.json", "r", encoding="utf-8"))
        self.last_closed=[]
        self.r.bind("<Control-Shift-N>", lambda x=None: Window().main())
        self.text=None

    def menubar(self):
        """Initialize the menubar"""
        for widgets in self.r.winfo_children():
            widgets.destroy()
        menu = tk.Menu(self.r)
        self.tablore=tab(self.r)
        self.tablore.pack(fill='both')
        self.r.config(menu=menu)

        #goofy action menu
        filemenu = tk.Menu(menu, tearoff=False)
        filemenu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        filemenu.add_command(label="New", accelerator="Ctrl+N", command=self.newtab)
        filemenu.add_command(label="Save", accelerator="Ctrl+S", command=self.savechoice)
        filemenu.add_command(label="Save as", accelerator="Ctrl+Alt+S", command=self.saveas)
        filemenu.add_separator()
        filemenu.add_command(label="Run test script", command=self.test)
        filemenu.add_command(label="Run program (if it was code file)", accelerator="Ctrl+F5", command=None)
        menu.add_cascade(label='Action', menu=filemenu)
    
    def test(self): pass

    def main(self):
        self.menubar()
        self.newtab()
        for b in [self.r]:
            b.bind("<Control-o>", lambda x=None: self.open_file())
            b.bind("<Control-n>", lambda x=None: self.newtab())
            b.bind("<Control-w>", lambda x=None: self.closetab)
            b.bind("<Control-f>", lambda x=None: self.find_dialog())
            b.bind("<Control-Shift-T>", self.reopen_last_close); b.bind("<Control-Shift-t>", self.reopen_last_close)
            b.bind("<Control-s>", lambda x=None: self.savechoice())
            b.bind("<Control-S>", self.savechoice)
            b.bind("<Key>", lambda x=None: self.check())
            b.bind("<Control-Alt-s>", self.saveas)
            b.bind("<Control-F5>", None)#le run
        self.tablore.bind("<<NotebookTabChanged>>", self.tabchange)
        self.r.mainloop()

    def _on_change(self, event):
        self.variables[f"linenumbers{self.tabindex}"].redraw()

    def multi(self, text):
        self._on_change

    def open_file(self):
        self.fileobj[self.tabindex]=filedialog.askopenfilename(
            title="Open text file",
            filetypes=[
                ("All files", "*.*"),
                ("Text Document", "*.txt"),
                ("Python files", "*.py"),
                ("Python files (no console)", "*.pyw"),
                (".js files", "*.js"),
                ("HTML Document", "*.html"),
                ("Markdown files", "*.md"),
                ("JSON files", "*.json"),
            ],
            defaultextension="Text Document")
        if self.fileobj[self.tabindex] != "":
            self.filename = os.path.basename(self.fileobj[self.tabindex])
            self.dirname = os.path.dirname(self.fileobj[self.tabindex])
            file = open(self.fileobj[self.tabindex], encoding="utf-8")
            self.variables[f"text{self.tabindex}"].delete('1.0', "end-1c")
            self.variables[f"text{self.tabindex}"].insert(tk.INSERT, file.read())
            self.r.title(f'0-budget Text Editor: {self.filename}')
            self.presave_content[str(self.index)]={
                "content": self.variables[f"text{self.index}"].get("1.0", "end-1c"),
                "name": self.filename,
                "directory": self.fileobj[self.tabindex]
            }
            self.tablore.add(self.variables[f"tab{self.tabindex}"],text=self.filename)
            if self.fileobj[self.tabindex] in list(set(self.saves.keys())):
                self.variables[f"text{self.tabindex}"].see(self.saves[self.fileobj[self.tabindex]])

    
    def savechoice(self):
        if self.presave_content[self.tabindex]["directory"] == "":
            self.saveas()
        else:
            self.save()
    
    def save(self):
        with open(self.fileobj[self.tabindex], "w", encoding="utf-8") as f:
            f.write(self.variables[f"text{self.index}"].get("1.0", "end-1c"))
        self.presave_content[str(self.tabindex)]={
            "content": self.variables[f"text{self.index}"].get("1.0", "end-1c"),
            "name": self.filename,
            "directory": self.fileobj[self.tabindex]
        }
        self.saves[self.fileobj[self.tabindex]] = self.variables[f"text{self.tabindex}"].index(tk.INSERT)
    
    def saveas(self):
        self.fileobj[self.tabindex] = filedialog.asksaveasfilename(
            title="Save file", 
            filetypes=[
                ("All files", "*.*"),
                ("Text Document", "*.txt"),
                ("Python files", "*.py"),
                (".js files", "*.js"),
                ("HTML Document", "*.html"),
                ("Markdown files", "*.md"),
                ("JSON files", "*.json")
            ],
            defaultextension="*.txt")
        if self.fileobj[self.tabindex] != "":
            self.filename = os.path.basename(self.fileobj[self.tabindex])
            self.dirname = os.path.dirname(self.fileobj[self.tabindex])
            with open(self.fileobj[self.tabindex], "w", encoding="utf-8") as f:
                f.write(self.variables[f"text{self.index}"].get("1.0", "end-1c"))
            self.r.title(f'0-budget Text Editor: {self.filename}')
        self.presave_content[str(self.tabindex)]={
            "content": self.variables[f"text{self.index}"].get("1.0", "end-1c"),
            "name": self.filename,
            "directory": self.fileobj[self.tabindex]
        }
        self.tablore.add(self.variables[f"tab{self.index}"],text=self.filename)
        self.saves[self.fileobj[self.tabindex]] = self.variables[f"text{self.tabindex}"].index(tk.INSERT)
    
    def check(self):
        if self.variables[f"text{self.tabindex}"].get("1.0", "end-1c") != self.presave_content[self.tabindex]["content"]:
            self.r.title(f"0-budget Text Editor: *{self.presave_content[self.tabindex]['name']}")
            self.tablore.add(self.variables[f"tab{self.tabindex}"],text=f"*{self.presave_content[self.tabindex]['name']}")
        else:
            self.r.title(f"0-budget Text Editor: {self.presave_content[self.tabindex]['name']}")
            self.tablore.add(self.variables[f"tab{self.tabindex}"],text=f"{self.presave_content[self.tabindex]['name']}")
    
    def tabchange(self, event: tk.Event):
        self.tabindex = str(event.widget.index("current"))
        self.text=self.variables[f"text{self.tabindex}"]
        self.check()

    def newtab(self):
        self.index = str(int(self.index) + 1)
        self.tabindex = str(int(self.tabindex) + 1)
        self.variables[f"tab{self.index}"] = tk.Frame(self.tablore)
        textobj=tk.Text(self.variables[f"tab{self.index}"], font=("Arial", 8))
        self.variables[f"text{self.index}"] = LineCounter.CustomText(textobj)
        self.variables[f"vsb{self.index}"] = tk.Scrollbar(textobj, orient="vertical", command=self.variables[f"text{self.index}"].yview)
        self.variables[f"text{self.index}"].configure(yscrollcommand=self.variables[f"vsb{self.index}"].set)
        self.variables[f"linenumbers{self.index}"] = LineCounter.TextLineNumbers(self.variables[f"tab{self.index}"], width=30)
        self.variables[f"linenumbers{self.index}"].sync_index(self.index)
        self.variables[f"linenumbers{self.index}"].attach(self.variables[f"text{self.index}"])

        self.variables[f"vsb{self.index}"].pack(side="right", fill="y")
        self.variables[f"linenumbers{self.index}"].pack(side="left", fill="both")
        #self.variables[f"text{self.index}"].pack(side="right", fill="both", expand=True)

        self.variables[f"text{self.index}"].bind("<<Change>>", self._on_change)
        self.variables[f"text{self.index}"].bind("<Configure>", self._on_change)
        
        textobj.pack(fill='both')
        self.variables[f"text{self.index}"].pack(expand=True, fill='both')

        self.tablore.add(self.variables[f"tab{self.index}"],text=f"untitled-{int(self.index)+1}")
        self.tablore.select(self.variables[f"tab{self.index}"])
        self.presave_content[self.index]={
            "content": "",
            "name": f"untitled-{int(self.index)+1}",
            "directory": ""
        }

    def closetab(self) -> int | None:
        if self.variables[f"text{self.tabindex}"].get("1.0", "end-1c") != self.presave_content[self.tabindex]["content"]:
            confirm: bool | None=messagebox.askyesnocancel("Unsaved changes", f"Do you want to save changes to {self.presave_content[self.tabindex]['name']}?")
            if confirm: #yes
                self.saveas()
            elif not confirm: #no
                self.last_closed.append(self.variables[f"tab{self.tabindex}"])
                self.tablore.hide(self.variables[f"tab{self.tabindex}"])
            else: return 0 #cancel
        else:
            self.last_closed.append(self.variables[f"tab{self.tabindex}"])
            self.tablore.hide(self.variables[f"tab{self.tabindex}"])
        if len(self.tablore.tabs()) == 0: self.r.destroy()
            

    def reopen_last_close(self, nonexist):
        try:
            self.tablore.add(self.last_closed[-1])
            self.tablore.select(self.last_closed[-1])
            del self.last_closed[-1]
        except: pass

    def on_window_close(self):
        for i in self.tablore.tabs():
            self.tabindex=str(self.tablore.index(i))
            cancel=self.closetab()
            if cancel == 0: return
        self.r.destroy()
    
    def find_replace_window(self) -> tk.Toplevel:
        """Create a Find and Replace window"""
        subwidget=tk.Toplevel(self.r)
        subwidget.title("Find or Replace")
        subwidget.protocol("WM_DELETE_WINDOW", lambda x=None: self.on_fnr_dialog_delete(subwidget))
        subwidget.bind("Control-F"); subwidget.bind("Control-f")
        subwidget.bind("Control-R"); subwidget.bind("Control-r")
        return subwidget

    def on_fnr_dialog_delete(self, wid):
        """On Find and Replace dialog close"""
        self.variables[f"text{self.index}"].tag_remove('found', '1.0', 'end')
        self.variables[f"text{self.index}"].tag_remove('current', '1.0', 'end')
        wid.destroy()

    def search(self, input):
        self.find_indexes = []
        text: tk.Text=self.variables[f"text{self.index}"]
        # remove tag 'found' from index 1 to END
        text.tag_remove('found', '1.0', 'end')
        
        # returns to widget currently in focus
        s = input.get('1.0', 'end-1c')
        if (s):
            idx = '1.0'
            onetime=0
            while 1:
                # searches for desired string from index 1
                idx = text.search(s, idx, nocase = 1,
                                stopindex = 'end')
                
                if not idx: break
                text.see(idx)
                # last index sum of current index and
                # length of text
                lastidx = '% s+% dc' % (idx, len(s))
                
    
                # overwrite 'Found' at idx
                text.tag_add('found', idx, lastidx)
                if onetime == 0:
                    text.tag_add('current', idx, lastidx)
                    onetime = 1
                self.find_indexes.append((idx, lastidx))
                idx = lastidx

            # mark located string as red
            
            text.tag_config('found', background= 'green')
            text.tag_config('current', background= 'blue')
        input.focus_set()

    def next_search(self, direction: int):
        """1 is up, 2 is down"""
        try:
            self.variables[f"text{self.index}"].tag_remove('current', self.find_indexes[self.find_count][0], self.find_indexes[self.find_count][1])
        except AttributeError: return
        if direction == 2:
            self.find_count+=1
            if self.find_count > len(self.find_indexes)-1:self.find_count=0
                
        elif direction == 1:
            self.find_count-=1
            if self.find_count < 0: self.find_count= len(self.find_indexes)-1
        else: print("ok no bye"); return
        
        b=self.find_indexes[self.find_count]

        print(self.find_count)
        self.variables[f"text{self.index}"].tag_add('current', b[0], b[1])
        self.variables[f"text{self.index}"].see(b[0])

    def find_dialog(self):
        self.find_count=0
        findwindow = self.find_replace_window()
        tk.Button(findwindow, text="Next", command=lambda x=None: self.next_search(2)).pack(anchor="w")
        tk.Button(findwindow, text="Previous", command=lambda x=None: self.next_search(1)).pack(anchor="w")
        input=tk.Text(findwindow)
        input.focus_set()
        input.pack()
        tk.Button(findwindow, text="Next", command=lambda x=None: self.search(input)).pack()
    

re.search
try:
    Window().main()
except:
    messagebox.showerror("haha you cause exit error, now see what it said", traceback.format_exc())
