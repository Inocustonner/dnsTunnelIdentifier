import ruamel.yaml
import sys
import os

CONFIG_NAME       = "config.yaml"
DEFAULT_CONF_PATH = f"{CONFIG_NAME}"

ALLOWED_NAME_LEN  = int()
MIN_TTL           = int()
RESTRICTED_SYMS   = ""
MAX_BODY_SIZE     = int()
NTH               = int()
D1                = int()
D2                = int()

gYaml = ruamel.yaml.YAML()
conf = None

def load_files(root: str):
  return list(filter(lambda node: '.pcap' in node, os.listdir(root)))

def getUndoneFiles() -> list:
  global conf
  return list(filter(lambda fname: fname not in conf['filesDone'], conf['files']))

def setFileDone(fname: str) -> None:
  global conf
  conf['filesDone'].append(fname)

def dump_conf(root: str):
  global conf
  config_path = os.path.join(root, CONFIG_NAME)
  gYaml.dump(conf, open(config_path, 'w'))

def load_config(root: str) -> None:
  global conf
  config_path = os.path.join(root, CONFIG_NAME)
  if not os.path.exists(config_path):
    conf = gYaml.load(open(DEFAULT_CONF_PATH))
    conf['files'] = load_files(root)
    conf['filesDone'] = []
    dump_conf(root)
  else:
    conf = gYaml.load(open(config_path))
  ALLOWED_NAME_LEN = conf['allowed-name-len']
  MIN_TTL = conf['min-ttl']
  RESTRICTED_SYMS = conf['restricted-syms']
  MAX_BODY_SIZE = conf['max-body-size']
  NTH = conf['nth']
  D1 = conf['d1']
  D2 = conf['d2']
  
  print("Config: \n")
  gYaml.dump(conf, sys.stdout)