#!/usr/bin/env python3

import csv
import logging

from .parser import Parser
from .telemetry import Telemetry
from .packet import Packet
import open_telemetry_kit.element as element

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
            packet[element_cls.name] = element_cls.fromCSV(val)
          else:
            packet[key] = element.UnknownElement(val)
        
        tel.append(packet)

    return tel