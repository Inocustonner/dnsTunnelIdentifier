# How to run
Use `python main.py` command and pass `-f` flag with the path to analyzed pcap
# What dpkt is doing here?
It's because in original dpkt package has a problem where he tries to decode DNS TXT Answer in utf8 whatsoever may not be true, it may be not a utf8 sequence, so we changed that behavior a bit(disabled decoding)