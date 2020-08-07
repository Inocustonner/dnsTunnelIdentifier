from dnsTunnelIdentifier.DNSInfo import DNSInfo, pcap_to_packets
from dnsTunnelIdentifier.analyze import analyze, Result
from dnsTunnelIdentifier.utils import getLogger, Timer
from dnsTunnelIdentifier.config import Global
from dnsTunnelIdentifier.spark import getSC

from pyspark import RDD

from typing import List, Tuple
from multiprocessing import Pool, cpu_count
# SparkContext.setSystemProperty('spark.executor.memory', '2g')
# fname = R"F:\hackathon\Data\clean.pcap"

def main(filepath: str) -> List[Tuple[str, Result]]:
  log = getLogger()
  sc = getSC()
  log.info('http://localhost:4040')
  log.info(f'Processing {filepath}')
  # produces tuples of the following form (timestamp: float, packet_raw_bytes: bytes)
  timer = Timer()
  pcap_packets = pcap_to_packets(filepath)
  log.info(f'Time spent on reading .pcap file = {timer.elapsed()}')

  # TODO: store amout of packets to temp, and load when needed

  lb = (len(pcap_packets) - 1) // Global.PACKETS_PER_ANALYSIS + 1

  def parseDNSInfo(pcap_packets: RDD) -> RDD:
    timer = Timer()

    rddDns = pcap_packets.map(lambda bytes_packet: DNSInfo(bytes_packet[0], bytes_packet[1])).filter(
      lambda dns: not dns.notDns and dns.sip not in Global.TRUSTED_DNS and dns.dip not in Global.TRUSTED_DNS)

    log.info(f'Time spent on parsing chunk = {timer.elapsed()}')
    return rddDns

  def genBundles():
    nonlocal pcap_packets
    nonlocal sc
    for n in range(1, lb):
      yield (n,
             parseDNSInfo(
              sc.parallelize(pcap_packets[:Global.PACKETS_PER_ANALYSIS], Global.RDD_SLICES)))
      pcap_packets = pcap_packets[Global.PACKETS_PER_ANALYSIS:]  

  ret = {}
  for n, rddBundle in genBundles():
    timer = Timer()
    # rdd = sc.parallelize(bundle, Global.RDD_SLICES)
    # filter out ips that we've already remembered 
    # rdd = rddBundle.filter(lambda dns: str(dns.sip) not in ret and str(dns.dip) not in ret)
    if rdd.count():
      ret.update(analyze(rdd))
    log.info(f'Time spent analysing chunk = {timer.elapsed()}')
    log.debug(f'ret: {ret}')

    print(f'{n}/{lb} Iterations')
  return list(ret.items())