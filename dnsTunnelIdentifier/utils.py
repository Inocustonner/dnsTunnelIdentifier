import logging
import os
import pandas as pd
from typing import List, Tuple
import time

LOGGER_NAME='MainLogger'

class Logger:
  logger = None

def write_results(root:str, results:List[Tuple[str,str]]):
  path = os.path.join(root, 'results.csv')
  df = pd.DataFrame(results)
  df.to_csv(path, mode='a', header=False, index=False)

def initLogger(logLevel: int = logging.DEBUG, **kwargs):
  if not (lgname := kwargs.get('loggerName')):
    lgname = LOGGER_NAME

  log = logging.getLogger(lgname)
  
  formatter = logging.Formatter(
    "[%(levelname)s]: %(message)s"
  )

  hcon = logging.StreamHandler()
  if kwargs.get('file'):
    hfile = logging.FileHandler(kwargs.get('file'))
    hfile.setFormatter(formatter)
    log.addHandler(hfile)
  
  hcon.setFormatter(formatter)
  log.addHandler(hcon)

  log.setLevel(logLevel)

  log.info(f'Logger `{LOGGER_NAME}` set to "{logging.getLevelName(log.getEffectiveLevel())}"')
  Logger.logger = log

def getLogger():
  return Logger.logger
  
class Timer():
  def __init__(self, msg: str = 'Time elapsed '):
    self.t = time.time_ns()
    self.msg = msg

  def elapsed(self):
    return (time.time_ns() - self.t) / 1e9

  def __enter__(self):
    self.t = time.time_ns()

  def __exit__(self):
    getLogger().info(self.msg + repr(self.elapsed()))