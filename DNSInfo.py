import dpkt
import enum

from functional import compose

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
    self.ts = ts if ts else None

    ip = dpkt.ethernet.Ethernet(raw).data
    self.sip = ip.src
    self.dip = ip.dst
    self.dns = dpkt.dns.DNS(ip.data.data)
    # Assume that dns have only 1 query
    queryIndex = 0
    self.qType = DnsType(self.dns.qd[queryIndex].type)

  def __repr__(self):
    return f"{self.__class__.__name__}({', '.join([f'{k}={repr(v)}' for k,v in vars(self).items()])})"
  
""" 
  Takes a file path to a pcap file and returns array of tuples of the following form
  (timestamp, raw packet)
"""  
def pcap_to_packets(file_path: str) -> list:
  return dpkt.pcap.Reader(open(file_path, 'rb')).readpkts()

""" 
  Takes a file path to a pcap file and returns generator of 
  array of tuples of the following form (timestamp, raw packet)
"""  
def pcap_to_packets_lazy(file_path: str) -> list:
  return dpkt.pcap.Reader(open(file_path, 'rb'))