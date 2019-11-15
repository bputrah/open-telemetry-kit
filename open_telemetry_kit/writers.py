#!/usr/bin/env python3

from .telemetry import Telemetry
from .packet import Packet
from .element import Element

def telemetryToJson(tel: Telemetry, file: str, ind: int = 3):
  import json
  with open(file, 'w') as f:
    json.dump(tel, f, default=lambda o: o.toJson(), indent=ind)

def telemetryToJsonStream(tel: Telemetry, ind: int = 3):
  import json
  return json.dumps(tel, default=lambda o: o.toJson(), indent=ind)

def telemetryToCSV(tel: Telemetry, file: str):
  import csv
  with open(file, 'w') as f:
    writer = csv.DictWriter(f, fieldnames=tel[0].keys())
    writer.writeheader()
    for packet in tel:
      writer.writerow(packet)