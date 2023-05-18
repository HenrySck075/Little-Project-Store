from typing import Generic, TypeVar, Callable, List, Any
from typing_extension import Self
import asyncio
from inspect import iscoroutinefunction as iscoro
from functools import wraps, partial


def to_async(func):
    @wraps(func)  # Makes sure that function is returned for e.g. func.__name__ etc.
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop() # Make event loop of nothing exists
        pfunc = partial(func, *args, **kwargs)  # Return function with variables (event) filled in
        return await loop.run_in_executor(executor, pfunc)
    return run

T = TypeVar("T")
TResult1 = TypeVar("TResult1", contravariant = True)
TResult2 = TypeVar("TResult2", contravariant = True)

class AggregateError(Exception):
    "Class that packs multiple exceptions in one. Used in `Promise`"
    def __init__(*msg, errors:List[Any]):
        super().__init__(*msg)
        self.errors=errors
#TODO: promise isnt synchronous
class Promise(Generic[T]):
    "The worst recreation ever exist (due to Python syntax and me)"
    def __init__(self,status=0,ret:T):
        self.status=status
        if status not in range(2): raise ValueError("Invalid status")
        self.ret=ret

    def then(self, onfulfilled: Callable[[T],TResult1]|None, onrejected: Callable[[Exception],TResult2]|None) -> Self[TResult1|TResult2]:
        def test(func):
            if not iscoro(func):
                func = to_async(func)
            try:
                return 0,asyncio.run(func(self.ret))
            except Exception as e:
                return 1,e
        

        if self.status==0:
            return Promise(*test(onfulfilled))
        else: return Promise(*test(onrejected))

    def catch(self,onrejected: Callable[[Exception],TResult2]|None) -> Self[TResult1|TResult2|None]:
        return self.then(None,onrejected)
    
    @classmethod
    def resolve(cls,ret:Any):
        return cls(0,ret)

    @classmethod
    def reject(cls,ret:Exception|Any):
        return cls(0,ret)

    @classmethod
    def all(cls,promises:List[Promise]):
        a=[]
        async for p in promises:
            pp = await p
            if pp.rejected == False: pp.then(lambda v: a.append(v))
            else: return pp
        return cls(0,a)

    @classmethod
    def allSettled(cls,promises:List[Promise]):
        boom = ["fulfilled","rejected"]
        a=[]
        async for p in promises:
            pp = await p
            h = {"status": boom[pp.status]}
            if pp.status==0: h["value"]=pp.ret
            else:h["reason"]=pp.ret
        return cls(0,a)

    @classmethod
    def any(cls,promises:List[Promise]):
        a=[]
        if promises==[]: return cls(1,ValueError("promises array is empty")
        async for p in promises:
            pp = await p
            if pp.status==1: pp.catch(lambda v: a.append(v))
            else: return pp

        return cls(1,AggregateError("All Promise rejected",errors=a))
