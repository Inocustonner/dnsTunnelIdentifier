from sys import path, argv
import os
import argparse

# from scapy.utils import RawPcapReader, PcapReader
# from scapy.layers.l2 import Ether
# from scapy.layers.inet import IP, UDP
# from scapy.layers.dns import DNS, DNSQR, DNSRR

# fpath = R"F:\hackathon\Data\iodinet.pcap"
# packet = RawPcapReader(fpath).read_all(2)[1]
# print(repr(Ether(packet[0])))
# udp = packet[UDP]
# print(repr(packet[IP]))
# print(repr(udp))

from dnsTunnelIdentifier.main import main 
if __name__ == "__main__":
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', type=str, 
                      help="path to pcap file that should be analyzed",
                      required=True)
  main(parser.parse_args(argv[1:]))