import functools, operator
from typing import List
def compose(*functions):
  def composed(f, g):
    return lambda x: f(g(x))
  return functools.reduce(composed, functions, lambda x: x)

def flip(function):
  def flipped(*args):
    return function(args[::-1])
  return flipped

def mergeList(lst: List[list]) -> list:
  return functools.reduce(operator.add, lst)