#!/usr/bin/env python3

import json
from flightpath import FlightPath
from packet import Packet
from element import Element

def makeSerializable(obj):
  if isinstance(obj, FlightPath):
    return obj.data
  if isinstance(obj, Packet):
    return obj.data
  if isinstance(obj, Element):
    return obj.value
  else:
    type_name = obj.__class__.__name__
    raise TypeError(f"Object of type '{type_name}' is not JSON serializable")

def flightPathToJson(flightpath, file, ind=3):
  with open(file, 'w') as f:
    # import pdb
    # pdb.set_trace()
    json.dump(flightpath, f, default=lambda o: o.toJson(), indent=ind)
    # json.dump(flightpath, f, default=makeSerializable, indent=ind)

def flightPathToJsonStream(flightpath, ind=3):
  return json.dumps(flightpath, default=lambda o: o.toJson, indent=ind)