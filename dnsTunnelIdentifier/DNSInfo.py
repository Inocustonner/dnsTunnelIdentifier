import enum

from dnsTunnelIdentifier.functional import compose

from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, UDP
from scapy.layers.dns import DNS, DNSQR, DNSRR

from typing import Union, List, Tuple


class DnsType(enum.Enum):
  A = 1
  NS = 2
  CNAME = 5
  SOA = 6
  NULL = 10
  PTR = 12
  HINFO = 13
  MX = 15
  TXT = 16
  AAAA = 28
  SRV = 33
  OPT = 41
  
class DNSInfo:
  def __init__(self, raw: bytes, ts: float = 0):
    packet = Ether(raw)

    self.ts = ts
    ip = packet[IP]

    assert ip.haslayer(DNS), 'Packet must have DNS layer'
    self.sip = ip.src
    self.dip = ip.dst
    self.dns = ip[DNS]
    #assume we have only one query
    self.qType = self.dns.qd.qtype
    self.name = self.dns.qd.qname
    # if self.dns.haslayer(DNSRR):
      # self.ans = self.dns

  def isResponse(self) -> bool:
    return self.dns.haslayer(DNSRR)

  def getAns(self) -> Union[DNSRR, None]:
    if self.isResponse():
      return self.dns[DNSRR]
    else:
      return None

  def getTTL(self) -> Union[int, None]:
    if ans := self.getAns():
      return ans.ttl
    else:
      return None
  
  def getName(self) -> bytes:
    return self.name

  def get(self, attr: str, default=None) -> Union[str, None]:
    switch = {
      'name': lambda: self.name,
      'type': lambda: self.qType,
      'answer': self.getAns,
      'ttl': self.getTTL,
    }
    return switch.get(attr, lambda: default)()


  def __repr__(self):
    return f"{self.__class__.__name__}({', '.join([f'{k}={repr(v)}' for k,v in vars(self).items()])})"

"""
  Takes a path to .pcap file and returns packet with `n` index in DnsInfo
"""
def from_pcap(file_path: str, n: int = 0) -> DNSInfo:
  pt = convertPacket(RawPcapReader(file_path).read_all(n + 1)[-1])
  return DNSInfo(pt[0], pt[1])

to_ts = lambda meta: float(meta.sec) + meta.usec / 10**6
convertPacket = lambda pkt: (pkt[0], to_ts(pkt[1]))
""" 
  Takes a file path to a pcap file and returns array of tuples of the following form
  (raw packet, timestamp)
"""  
def pcap_to_packets(file_path: str, cnt: int = -1) -> List[Tuple[bytes, float]]:
  return map(convertPacket, RawPcapReader(file_path).read_all(cnt))

""" 
  Takes a file path to a pcap file and returns generator of 
  array of tuples of the following form (timestamp, raw packet)
"""  
def pcap_to_packets_lazy(file_path: str):
  def lazy():
    reader = RawPcapReader(file_path)
    v = next(reader)
    while v:
      yield convertPacket(v)
      v = next(reader)