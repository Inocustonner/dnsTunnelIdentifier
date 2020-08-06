from sys import argv
import os
import argparse
from dnsTunnelIdentifier.config import load_config, dump_conf, getUndoneFiles
from typing import List, Tuple
from pyspark import SparkContext, SparkConf
from dnsTunnelIdentifier.main import main 

if __name__ == "__main__":
  os.chdir(os.path.dirname(os.path.abspath(__file__)))

  parser = argparse.ArgumentParser()
  parser.add_argument('-s', type=str, 
                      help="path to pcap file or directory with pcap files",
                      required=True)

  parsed = parser.parse_args(argv[1:])
  if not os.path.isdir(parsed.s):
    root_dir = os.path.dirname(parsed.s)
  else:
    root_dir = parsed.s

  load_config(root_dir)

  files = getUndoneFiles()
  
  # configure spark
  # conf = SparkConf().setAppName('test').setMaster('local[*]')
  # conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
  # conf.set("spark.sql.execution.arrow.enabled", "true")
  # sc = SparkContext(conf=conf)
  # sc.setLogLevel("ERROR")  

  # output = []
  # try:
  #   for f in files:
  #     output.append(main(sc, f))
  # except KeyboardInterrupt:
  #   print("Stopping programm...")
  # except Exception as e:
  #   print(e)
  # finally:
  #   dump_conf()