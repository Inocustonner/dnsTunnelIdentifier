from dnsTunnelIdentifier.config import load_config, dump_conf, getUndoneFiles, setFileDone
from dnsTunnelIdentifier.main import main 
from dnsTunnelIdentifier.utils import initLogger, getLogger, write_results, Timer
from dnsTunnelIdentifier.spark import initSpark
import os, argparse, traceback
import logging, multiprocessing as mp
from sys import argv
from typing import List, Tuple
# def job(path: str):
#   try:
#     res = main(path)
#     # setFileDone(f)
#   except:
#     return None
#   return res

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

  initLogger(logging.DEBUG, file=Rf'{root_dir}\log.txt')
  initSpark()
  load_config(root_dir)
  log = getLogger()
  
  # files = map(lambda f: Rf'{root_dir}\{f}', getUndoneFiles())
  files = getUndoneFiles()

  # output = []
  try:
    # with mp.Pool(mp.cpu_count()) as pool:
    #   result = pool.map(job, files)

    for f in files:
      
      timer = Timer()
      res = main(Rf'{root_dir}\{f}')
      log.info(f'Time spent on {f} = {timer.elapsed()}')
      
      write_results(root_dir, res)
      setFileDone(f)
      
  except KeyboardInterrupt:
    print("Stopping programm...")
  except Exception:
    error = traceback.format_exc()
    log.fatal(f'!!-----------!!\n{error}')
  finally:
    dump_conf(root_dir)