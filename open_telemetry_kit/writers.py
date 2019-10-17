#!/usr/bin/env python3

import json
from .telemetry import Telemetry
from .packet import Packet
from .element import Element

def telemetryToJson(tel: Telemetry, file: str, ind: int = 3):
  with open(file, 'w') as f:
    json.dump(tel, f, default=lambda o: o.toJson(), indent=ind)

def telemetryToJsonStream(tel: Telemetry, ind: int = 3):
  return json.dumps(tel, default=lambda o: o.toJson(), indent=ind)