import json

def sliceEvery(iter, nthElem:int):
    try: nthElem = int(nthElem)
    except: return iter # gotcha, you dont listen to me

    return [iter[i:i+nthElem] for i in range(0,len(iter),nthElem)]

def loadJson(filename) -> dict | list: 
    return json.load(open(filename, "r"))
