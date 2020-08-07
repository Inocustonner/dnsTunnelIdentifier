# from dnsTunnelIdentifier.spark import getSC
from dnsTunnelIdentifier.functional import compose
from dnsTunnelIdentifier.DNSInfo import DNSInfo
from dnsTunnelIdentifier.utils import getLogger, Timer
from dnsTunnelIdentifier.config import Global
from dnsTunnelIdentifier.unigramAnalysis import unigramAnalysis, Result
from dnsTunnelIdentifier.spark import getSC

from pyspark import RDD, StorageLevel
import numpy as np
import chardet, tld

from socket import inet_aton, inet_ntoa
from typing import List, Tuple, Dict
import os, functools, operator

def printIPDirections(rddDns: RDD, cnt = 10) -> None:
  print('\n'.join(map(lambda dnsinfo: f'{dnsinfo.sip}->{dnsinfo.dip}', rddDns.take(10))))

def printDns(rddDns: RDD, cnt = 10) -> None:
  print('\n'.join(map(repr, rddDns.take(cnt))))

def is_trusted_encoding(raw: bytes) -> bool:
  trusted_encodings = ['utf-8', 'ascii']
  encoding = chardet.detect(raw)['encoding']
  return encoding in trusted_encodings

""" Returns True if premise is not found """
def premiseCheck(allowed_name_len: str, 
                 restricted_syms: str, 
                 max_body_size: int,
                 min_ttl: int,
                 dns: DNSInfo) -> bool:
  name = dns.getName()

  log_prefix = f'{dns.getServerIP()}-{name} '
  
  prem = is_trusted_encoding(name) 
  if not prem: 
    # print(log_prefix + 'premise failed on encoding check')
    return prem
  
  name = str(name)
  
  # if this name has known TLD ignore it
  if tld.get_tld(name, fix_protocol=True, fail_silently=True) != None:
    return True

  prem = prem and len(name) <= allowed_name_len
  if not prem: 
    # print(log_prefix + 'premise failed on name len check')
    return prem

  prem = prem and all(map(lambda sym: sym not in name, restricted_syms))
  if not prem: 
    # print(log_prefix + 'premise failed on restricted syms check')
    return prem

  # if still satisfy
  if prem == True:
    if dns.qtype == 'TXT' and (ans := dns.getAns()):
      prem = prem and functools.reduce(lambda acc, x: acc+len(x), ans.rdata, 0) <= max_body_size
      if not prem: 
        # print(log_prefix + 'premise failed on body size check')
        return prem

    # TTL should be applied to average TTL value
    # if ttl := dns.getTTL():
    #   prem = prem and ttl <= min_ttl
    #   if not prem: 
    #     print(log_prefix + 'premise failed on ttl check')
    #     return prem

  return prem

def parseDomain(domain: str) -> str:
  return domain.lower()

def analyze(rddDns: RDD) -> Dict[str, Result]:
  # filter out trustedDNS
  log = getLogger()
  premiseCheck_ = functools.partial(premiseCheck, 
                                    Global.ALLOWED_NAME_LEN, 
                                    Global.RESTRICTED_SYMS, 
                                    Global.MAX_BODY_SIZE,
                                    Global.MIN_TTL)
  
  timer = Timer()
  # cache bcs only this rdd will be used in the application
  ipPartGen = rddDns.filter(compose(operator.not_, premiseCheck_)).map(lambda dns: str(dns.sip)).distinct().glom().toLocalIterator()
  log.info(f'Time spent on premis analysis = {timer.elapsed()}')
  # log.debug(ips)

  timer = Timer()
  ipdoms = {}
  # REFACTOR THIS STIH

    
  for ipPart in ipPartGen:
    for ip in set(ipPart):
      if ip not in ipdoms:
        log.debug(ip)
        ipdoms[ip] = np.array(
          rddDns.filter(
            lambda dns: ip in [dns.dip, dns.sip]).map(
              lambda dns: parseDomain(str(dns.getName()))).distinct().collect())
        log.debug(ipdoms.get(ip))
      
  log.info(f'Time spent on searching packets for chosen IPs = {timer.elapsed()}')

  timer = Timer()
  result = []
  for ip, doms in ipdoms.items():
    result.append((str(ip), repr(unigramAnalysis(doms))))
  log.info(f'Time spent on unigram distribution analysis = {timer.elapsed()}')

  rddDns.unpersist()
  
  return dict(result)