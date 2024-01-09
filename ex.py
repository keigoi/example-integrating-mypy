# 色々確認用ファイル
#from typing import TypeVar, Generic
#from enum import Enum
#import mypy
#import builtins
#
#T = TypeVar("T")
#U = TypeVar("U")
#V = TypeVar("V")

#A = TypeVar("A")
#B = TypeVar("B")
#C = TypeVar("C")
#x: At[int, type[A]] = 123 @ A
#class B(Role):
#    def __matmul__(self, x): # @ を使えるようにする
#        pass
#    pass
#
#class C(Role):
#    def __matmul__(self, x): # @ を使えるようにする
#        pass
#    pass
#
#class R2(Generic[U,V]):
#    pass
#
##class Bchannel(Generic[T,V]):
##    builtins.At[object,R2[T,V]]
#
#class Choice(Enum):
#    OK = 1
#    KO = 2
#from mypy import *
from role import *
from builtins import *
#from builtins import *
#x:int
#x = 1 + 1
#import role

class Conv(Ch2[A,B]):
  def __init__(self):
    self.chAB : Channel[int,A,B] = Channel[int,A,B]()

  def f(self,x:At[int,A]):
    x = 123@A()
    y = self.chAB.com(x)
    return y
    #if x > 100@A():
    #  return "a"@A()
    #else:
    #  return "False"@A()

#x = 123@A()
#
#if x > 100@A: # (int@A > int@A)@boolになって欲しい
#  assert 1
#elif x <= 200@A:
#  assert 2
#else:
#  assert 3