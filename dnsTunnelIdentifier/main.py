from dnsTunnelIdentifier.DNSInfo import DNSInfo, pcap_to_packets
from dnsTunnelIdentifier.analyze import analyze
import logging
import dnsTunnelIdentifier.utils
from pyspark import SparkContext, SparkConf

# SparkContext.setSystemProperty('spark.executor.memory', '2g')
# fname = R"F:\hackathon\Data\clean.pcap"

TEST_MAX_PACKETS = 1000

def main(sc: SparkContext, *args):
  

  utils.initLogger(logging.DEBUG)

  print("Server: http://localhost:4040")

  # produces tuples of the following form (timestamp: float, packet_raw_bytes: bytes)
  rdd = sc.parallelize(pcap_to_packets(args.f, TEST_MAX_PACKETS))
  analyze(sc, rdd)