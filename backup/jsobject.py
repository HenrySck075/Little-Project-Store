class JSONObject(object):
    length = 1
    def __init__(self, d: dict | list):
        for k in d:
            v = d[k] if type(d[k]) != dict and type(d[k]) != list else (JSONObject(d[k]))
            setattr(self, k, v)
        self.__data__ = d
        length = len(d)
        self.__setattr__ = self.__setattr2__

    def __repr__(self):
        return f"Object {im lazy to do this sorry}"
    def __str__(self):
        return self.__repr__()
    def __getitem__(self,i):
        return self.__data__[i]
    def __setattr2__(self,name,value):
        if name in self.__dict__ and name not in self.__data__: raise KeyError("no you don't")
        else: super().__setattr__(self, name, value)
