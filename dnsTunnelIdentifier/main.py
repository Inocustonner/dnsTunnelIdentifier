from dnsTunnelIdentifier.DNSInfo import DNSInfo, pcap_to_packets
from dnsTunnelIdentifier.analyze import analyze
from pyspark import SparkContext, SparkConf
# import logger

# SparkContext.setSystemProperty('spark.executor.memory', '2g')
# fname = R"F:\hackathon\Data\clean.pcap"

TEST_MAX_PACKETS = 1000

def main(args):
  conf = SparkConf().setAppName('test').setMaster('local[*]')
  conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
  conf.set("spark.sql.execution.arrow.enabled", "true")
  sc = SparkContext(conf=conf)
  sc.setLogLevel("ERROR")

  print("Server: http://localhost:4040")

  # produces tuples of the following form (timestamp: float, packet_raw_bytes: bytes)
  rdd = sc.parallelize(pcap_to_packets(args.f)[:TEST_MAX_PACKETS])
  analyze(sc, rdd)