class Object(object):
    length = 1
    def __init__(self, d: dict | list):
        super().__init__()
        if type(d) == list:
            for i in range(len(d)):
                try: d[i] = JSONObject(d[i])
                except TypeError: pass

        elif type(d) == dict:
            for k in d.keys():
                v = d[k] 
                if type(d[k]) == dict or type(d[k]) == list: v=JSONObject(d[k])
                setattr(self, k, v)
        else: raise TypeError("ok")
        self.__data__ = d
        self.length = len(d)
        self.__setattr__ = self.__setattr2__

    def __repr__(self):
        return "Object {im lazy to do this sorry}"
    def __str__(self):
        return self.__repr__()
    def __getitem__(self,i):
        return self.__data__[i]
    def __setattr2__(self,name,value):
        if name in self.__dict__ and name not in self.__data__: raise KeyError("no you don't")
        else: super().__setattr__(self, name, value)
