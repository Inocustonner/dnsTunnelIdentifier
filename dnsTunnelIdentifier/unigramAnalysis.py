from dnsTunnelIdentifier.config import Global

import numpy as np

from typing import List, Tuple
import multiprocessing as mp
import functools, enum

DEFAULT_FRQ = 0.1
RANK = 10
d1 = 0.05
d2 = 0.05
 
class Result(enum.Enum):
  Tunnel = 2
  Warning = 1
  
def distribution_test(distr: list) -> Result:
  if len(distr) <= Global.NTH:
    return Result.Warning

  fst = distr[0]
  nth = distr[Global.NTH]
  if (Global.DEFAULT_FRQ - Global.D1) <= fst - nth:
    return Result.Warning
  else:
    return Result.Tunnel

def gatherUnigram(domain: str) -> dict:
  unigrams = dict()
  for ch in set(domain):
    unigrams[ch] = domain.count(ch)
  return unigrams
  
def mergeDicts(d1: dict, d2: dict) -> dict:
  d = {}
  chain = list(d1.items())
  chain.extend(d2.items())
  for k, v in chain:
    if k not in d:
      d[k] = 0
    d[k] += v

  return d

def unigramAnalysis(domains: np.array) -> None:
  with mp.Pool(mp.cpu_count()) as pool:
    res = sorted(functools.reduce(mergeDicts, pool.map(gatherUnigram, domains)).items(), key=lambda tup: tup[1], reverse=True)
  doms_len = functools.reduce(lambda acc, x: len(x) + acc, domains, 0)
  distr = list(map(lambda tup: tup[1] / doms_len, res))
  return distribution_test(distr)