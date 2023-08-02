#code = print("brainfuck code here (Ctrl-D to continue):\n")
import random, re, time
from prompt_toolkit import PromptSession
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.styles import style_from_pygments_cls, Style
from pygments.styles.colorful import ColorfulStyle
from pygments.lexers.esoteric import BrainfuckLexer
from prompt_toolkit.lexers import PygmentsLexer
from string import ascii_lowercase
from typing import Tuple, Dict

session = PromptSession()
def bfexec(c:str,challengeMode=False,returnType="int") -> Tuple[Dict[str,int], str | int | None]:
    cells = [0]*(8 if challengeMode else 30_000)
    idx=0
    pointer=0
    ignore = -1
    loops = []
    digitout = 0
    stringout = ""
    inputs={}
    while True:
        if idx==len(c): break
        match c[idx]:
            case "+": cells[pointer]+=1
            case "-": cells[pointer]-=1
            case "<": pointer = (pointer-1)%(len(cells)+1)
            case ">": pointer = (pointer+1)%(len(cells)+1)
            case ".": 
                char = chr(cells[pointer]+(32 if challengeMode else 0))
                print(char,end="")
                stringout+=char
                digitout+=cells[pointer]
            case ",": 
                if challengeMode: 
                    cells[pointer] = random.choice(range(96))
                    for i in ascii_lowercase:
                        if i not in inputs.keys():
                            inputs[i] = int(cells[pointer])
                            break
                else: cells[pointer] = int(input("Input cell: "))
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
        if challengeMode:
            time.sleep(.1)
    ret = None
    if returnType == "int": ret = digitout
    if returnType == "str": ret = stringout
    if challengeMode: ret = (inputs, ret)
    return ret


#bfexec("++++[->++++++++>++++++++<<]>>[->+++<]>++++++++.+.<<.>>++++.++.--.")

section = 2

challenges = [
    ("Run any program", None),
    ("Create and run a program that outputs 10", 10),
    ("Create and run a program that outputs 40", 40),
    ("Create and run a program that takes a number as input and outputs that number doubled", "2*a"),
    ("Create and run a program that takes two numbers as input and outputs their sum", "a+b"),
    ("Create and run a program that takes two inputs, and outputs the largest input minus the smallest input", "c=a-b if a>b else b-a", "c") #if the length is 3, then condition uses exec() to check and the 3rd item is the return variable
]
class BfInputValidator(Validator):
    def validate(self, doc):
        text=doc.text
        if len(re.findall("[^+-><.,\[\]]",text)) != 0: raise ValidationError(len(text),"Invalid brainfuck syntax")

if section==2:
    runComplete = None
    idx=0
    last=""
    while True:
        if idx == len(challenges): break
        i = challenges[idx]
        style = style_from_pygments_cls(ColorfulStyle).style_rules
        style.append(('bottom-toolbar', f'#{"000000" if runComplete else "ffffff"} bg:#{"00FF26" if runComplete else "FF002A"}'))
        meow = "Run completed" if runComplete else "Run failed"
        if runComplete == None: meow = None
        command = session.prompt(i[0]+"\n",validator=BfInputValidator(),lexer=PygmentsLexer(BrainfuckLexer),style=Style.from_dict({n[0]:n[1] for n in style}),bottom_toolbar=meow,default=last)
        inputs,res = bfexec(command, True)
        if i[1] == None: runComplete = True
        else:
            if type(i[1]) == int: runComplete = (i[1] == res)
            if type(i[1]) == str: 
                if len(i) == 3: 
                    exec(i[1],{},inputs)
                    runComplete = (inputs[i[2]] == res)
                else: runComplete = (eval(i[1],{},inputs) == res)
        
        if runComplete: idx+=1
        last = command

