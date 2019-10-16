#!/usr/bin/env python3

import csv
import logging

from .parser import Parser
from .telemetry import Telemetry
from .packet import Packet
from .element import UnknownElement

class CSVParser(Parser):
  ext = "csv"

  def __init__(self, source: str):
    super().__init__(source)

  def read(self) -> Telemetry:
    tel = Telemetry()
    with open(self.source, newline='') as csvfile:
      reader =  csv.DictReader(csvfile)
      for row in reader:
        packet = Packet()
        for key, val in row.items():
          if key in self.element_dict:
            #element_dict[key] returns a class
            element_cls = self.element_dict[key]
            packet[element_cls.name] = element_cls(val)
          else:
            packet[key] = UnknownElement(val)
        
        tel.append(packet)

    return tel