from dnsTunnelIdentifier.main import main 

from sys import path, argv
from os.path import dirname, realpath
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', type=str, 
                      help="Path to pcap file that should be analyzed",
                      required=True)
  main(parser.parse_args(argv[1:]))