from pyspark import SparkContext, SparkConf, RDD
from socket import inet_aton, inet_ntoa
from dnsTunnelIdentifier.functional import compose
from dnsTunnelIdentifier.DNSInfo import DNSInfo
import functools
import os

TRUSTED_DNS_FILE="trustedDNS.txt"
TRUSTED_DNS_PATH=fR'.\{TRUSTED_DNS_FILE}'

def getTrustedDNS() -> list:
  # bcs file is small there is no need to use spark
  try:
    with open(TRUSTED_DNS_PATH, 'r', encoding='utf8') as file:
      return file.readlines()
  except FileNotFoundError:
    print(f"{TRUSTED_DNS_FILE} not found")
    print('Returning empty trustedDNS list')
    return []

def printIPDirections(rddDns: RDD, cnt = 10) -> None:
  print('\n'.join(map(lambda dnsinfo: f'{dnsinfo.sip}->{dnsinfo.dip}', rddDns.take(10))))

def printDns(rddDns: RDD, cnt = 10) -> None:
  print('\n'.join(map(repr, rddDns.take(cnt))))

def analyze(sc: SparkContext, rdd_raw_packets: RDD) -> None:
  # filter out trustedDNS
  trustedDNS = getTrustedDNS()
  
  rddDns = rdd_raw_packets.map(lambda bytes_packet: DNSInfo(bytes_packet[0], bytes_packet[1]))
  # cache bcs only this rdd will be used in the application
  rddDns = rddDns.filter(lambda dnsinfo: all(map(lambda ip: ip not in trustedDNS, [dnsinfo.sip, dnsinfo.dip]))).cache()
  printIPDirections(rddDns, 20)
  printDns(rddDns, 20)