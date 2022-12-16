from typing import TypeVar, Generic

# def f(x:int):
#     return x + 1

T = TypeVar("T")
U = TypeVar("U")

class Roled1(Generic[T]):
    pass

class Roled2(Generic[T,U]):
    pass

class rstr(str, Roled1[T]):
    pass

class channel(Roled2[T,U]):
    pass

class Role:
    pass

class A(Role):
    def __matmul__(self, x): # @ を使えるようにする
        pass
    pass

def at(x:T, role:Role) -> T:
    return x

def g(x:str):
    # A() @ ""
    # x @ A()
    # A() @ 123
    return x

# x = 1
# if x:
#     f()
# else:
#     g()

