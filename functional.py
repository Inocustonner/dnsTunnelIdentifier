import functools

def compose(*functions):
  def composed(f, g):
    return lambda x: f(g(x))
  return functools.reduce(composed, functions, lambda x: x)

def flip(function):
  def flipped(*args):
    return function(args[::-1])
  return flipped