from __future__ import annotations
from typing import Callable, Any
from copy import deepcopy

class Array(object):
    length = 0
    def __init__(self, a: list):
        super().__init__()
        for i in range(len(a)):
            a[i] = Object(a[i]) if type(a[i]) == dict else Array(a[i]) if type(a[i]) == list else a[i]
        
        self.__data__ = a
        self.length = len(a)
        self.__setattr__ = self.__setattr2__
    def __repr__(self):
        hi = [repr(i) for i in self.__data__[0:5]]
        wrap = "[ ]"
        return f"Array {wrap.split(' ')[0]}{', '.join(hi)}{', ...' if len(self.__data__) > 5 else ''}{wrap.split(' ')[1]}"

    def __setattr2__(self,name,value):
        if name in self.__dict__ and name not in self.__data__: raise KeyError("no you don't")
        else: super().__setattr__(self, name, value)
    
    def __str__(self):
        return "[object Array]"
    
    def __getitem__(self,i):
        return self.__data__[i]
    
    def forEach(thisself, callbackFn:Callable[[Any], None], self=None):
        if self == None: self = thisself
        for i in [a for a in self.__dict__ if a in self.__data__]: callbackFn(i)

    def at(self,i): return self.__getitem__(i)

    def concat(self, *arrays:Array):
        a = deepcopy(self.__data__)
        [a.extend(ar) for ar in list(arrays)]
        return a
    
    def copyWithin(self, to, start, end=None):
        part = self.__data__[start:end]
        (self.__data__[.pop(to)] for _ in range(to))
        (self.__data__[to] for _ in range(to))

        
class Object(object):
    length = 0
    def __init__(self, d: dict):
        super().__init__()
        for k in d.keys():
            v = d[k] 
            if type(d[k]) == dict or type(d[k]) == list: v=Object(d[k])
            setattr(self, k, v)
        self.__data__ = d
        self.length = len(d)
        self.__setattr__ = self.__setattr2__

    
    def __repr__(self):
        hi = []
        wrap = "{ }"
        for i in [n for x, n in enumerate(self.__dict__.keys()) if n in self.__data__.keys() and x < 5]: hi.append(i+": "+repr(self.__dict__[i]))
        return f"Object {wrap.split(' ')[0]}{', '.join(hi)}{', ...' if len(self.__data__) > 5 else ''}{wrap.split(' ')[1]}"
    
    def __str__(self):
        return "[object Object]"
    
    def __getitem__(self,i):
        return self.__data__[i]
    
    def __setattr2__(self,name,value):
        if name in self.__dict__ and name not in self.__data__: raise KeyError("no you don't")
        else: super().__setattr__(self, name, value)