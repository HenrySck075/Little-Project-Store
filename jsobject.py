class Object(object):
    length = 1
    def __init__(self, d: dict | list):
        super().__init__()
        if type(d) == list:
            for i in range(len(d)):
                try: d[i] = Object(d[i])
                except TypeError: pass

        elif type(d) == dict:
            for k in d.keys():
                v = d[k] 
                if type(d[k]) == dict or type(d[k]) == list: v=Object(d[k])
                setattr(self, k, v)
        else: raise TypeError("ok")
        self.__data__ = d
        self.length = len(d)
        self.__setattr__ = self.__setattr2__

    def __repr__(self):
        hi = []
        wrap = "[ ]"
        if type(self.__data__) == dict:
            wrap = "{ }"
            for i in [n for x, n in enumerate(self.__dict__.keys()) if n in self.__data__.keys() and x < 5]: hi.append(i+": "+repr(self.__dict__[i]))
        else:
            hi = [repr(i) for i in self.__data__[0:5]]
        return f"{'Object' if type(self.__data__) == dict else 'Array'} {wrap.split(' ')[0]}{', '.join(hi)}{', ...' if len(self.__data__) > 5 else ''}{wrap.split(' ')[1]}"
    
    def __str__(self):
        return self.__repr__()
    def __getitem__(self,i):
        return self.__data__[i]
    def __setattr2__(self,name,value):
        if name in self.__dict__ and name not in self.__data__: raise KeyError("no you don't")
        else: super().__setattr__(self, name, value)
