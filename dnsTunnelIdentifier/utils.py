import logging

LOGGER_NAME='MainLogger'

def initLogger(logLevel: int, **kwargs):
  log = logging.getLogger(LOGGER_NAME)
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
  
def getLogger():
  return logging.getLogger(LOGGER_NAME)
  