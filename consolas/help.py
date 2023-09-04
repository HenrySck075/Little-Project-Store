import json
from typing import TypeVar
def sliceEvery(iter, nthElem:int):
    try: nthElem = int(nthElem)
    except: return iter # gotcha, you dont listen to me

    return [iter[i:i+nthElem] for i in range(0,len(iter),nthElem)]

def loadJson(filename) -> dict | list: 
    return json.load(open(filename, "r"))

def addattr(o,**h):
    for i in h.keys():
        setattr(o,i,h[i])
    return o

def runmethod(iter:list, methods:list):
    for i in iter:
        h = {"i":i}
        [exec(f"i.{m}",h) for m in methods]

h = TypeVar("h", covariant=True, bound=dict)

def modifyValue(dic:h, key, stuff) -> h:
    if key != "":
        dic[key] = stuff(dic[key])
    return dic


