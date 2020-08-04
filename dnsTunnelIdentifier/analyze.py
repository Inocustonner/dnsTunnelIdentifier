from pyspark import SparkContext, SparkConf, RDD
from socket import inet_aton, inet_ntoa
from dnsTunnelIdentifier.functional import compose
from dnsTunnelIdentifier.DNSInfo import DNSInfo
import functools
import os.path

TRUSTED_DNS_FILE=os.path.realpath(R"dnsTunnelIdentifier\trustedDNS.txt")

def getTrustedDNS() -> list:
  # bcs file is small there is no need to use spark
  with open(TRUSTED_DNS_FILE, 'r', encoding='utf8') as file:
    return list(map(inet_aton, file.readlines()))

def printIPDirections(rddDns: RDD, cnt = 10) -> None:
  print('\n'.join(map(lambda dnsinfo: f'{inet_ntoa(dnsinfo.sip)}->{inet_ntoa(dnsinfo.dip)}', rddDns.take(10))))

def printDns(rddDns: RDD, cnt = 10) -> None:
  print('\n'.join(map(repr, rddDns.take(cnt))))

def analyze(sc: SparkContext, rdd_raw_packets: RDD) -> None:
  # filter out trustedDNS
  trustedDNS = getTrustedDNS()
  rddDns = rdd_raw_packets.map(lambda tup: DNSInfo(tup[1], tup[0]))
  # cache bcs only this rdd will be used in the application
  rddDns = rddDns.filter(lambda dnsinfo: all(map(lambda ip: ip not in trustedDNS, [dnsinfo.sip, dnsinfo.dip]))).cache()
  printIPDirections(rddDns, 20)
  printDns(rddDns, 20)