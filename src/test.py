from csvparser import CSVParser
from srtparser import SRTParser
from telemetry import Telemetry
from packet import Packet
from element import Element
import writers as write
import detector

import json

def toJson(obj):
  if isinstance(obj, Packet):
    return obj.data
  if isinstance(obj, Element):
    return obj.value
  else:
    raise TypeError()

source = "/home/adam/Documents/telemetry_extraction/DJI/DJI_0001.srt"
dest = "/home/adam/hivemapper/telemetry-extraction-conversion/test.json"

parser = detector.create_telemetry_parser(source)

print(parser)

# parser = SRTParser(source)
# fp = parser.read()
# write.flightPathToJson(fp, dest)

# parser = CSVParser(source)
# fp = parser.read()

# with open("/home/adam/hivemapper/telemetry-extraction-conversion/test.json", 'w') as f:
#   json.dump(fp[:3], f, default = lambda o: o.toJson(), indent=3)
# print (fp)
# for packet in fp:
#   json.dumps(packet)
#   print(packet)