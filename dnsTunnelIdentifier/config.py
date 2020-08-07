from dnsTunnelIdentifier.utils import getLogger

import ruamel.yaml
import sys
import os

CONFIG_NAME          = "config.yaml"
DEFAULT_CONF_PATH    = f"{CONFIG_NAME}"

class Global:
  ALLOWED_NAME_LEN     = int()
  MIN_TTL              = int()
  RESTRICTED_SYMS      = ""
  MAX_BODY_SIZE        = int()
  NTH                  = int()
  PACKETS_PER_ANALYSIS = int()
  RDD_SLICES           = int()
  DEFAULT_FRQ          = int()
  D1                   = int()
  D2                   = int()
                        
  TRUSTED_DNS          = []

gYaml = ruamel.yaml.YAML()
conf = None

TRUSTED_DNS_FILE="trustedDNS.txt"
TRUSTED_DNS_PATH=fR'.\{TRUSTED_DNS_FILE}'

def getTrustedDNS() -> list:
  # bcs file is small there is no need to use spark
  try:
    with open(TRUSTED_DNS_PATH, 'r', encoding='utf8') as file:
      Global.TRUSTED_DNS = list(map(lambda line: line.rstrip(), file.readlines()))
      getLogger().debug(f"Trusted DNS:{Global.TRUSTED_DNS}")
  except FileNotFoundError:
    print(f"{TRUSTED_DNS_FILE} not found")
    print('Returning empty trustedDNS list')


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
  Global.ALLOWED_NAME_LEN = conf['allowed-name-len']
  Global.MIN_TTL = conf['min-ttl']
  Global.RESTRICTED_SYMS = conf['restricted-syms']
  Global.MAX_BODY_SIZE = conf['max-body-size']
  Global.PACKETS_PER_ANALYSIS = conf['packets-per-analysis']
  Global.RDD_SLICES = conf['rdd-slice-cnt']
  Global.DEFAULT_FRQ = conf['default-frq']
  Global.NTH = conf['nth']
  Global.D1 = conf['d1']
  Global.D2 = conf['d2']
  
  getTrustedDNS()
  
  print("\nConfig:")
  gYaml.dump(conf, sys.stdout)