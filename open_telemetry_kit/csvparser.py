from .parser import Parser
from .telemetry import Telemetry
from .packet import Packet
from .element import UnknownElement
from .element import TimestampElement, DatetimeElement

import csv
import logging

class CSVParser(Parser):
  tel_type = "csv"

  def __init__(self, source: str, require_timestamp: bool = False):
    super().__init__(source, require_timestamp)
    self.logger = logging.getLogger("OTK.CSVParser")

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
            self.logger.warn("Adding unknown element ({} : {})".format(key, val))
            packet[key] = UnknownElement(val)
        
        if self.require_timestamp and TimestampElement.name not in packet \
           and DatetimeElement.name not in packet:

          self.logger.error("Could not find any time elements when require_timestamp was set")
          raise Exception("No timestamp or datetime found with 'require_timestamp' set to true.")

        if len(packet) > 0:
          self.logger.info("Adding new packet.")
          tel.append(packet)
        else:
          self.logger.warn("No telemetry was found in block. Packet is empty, skipping.")

    if len(tel) == 0:
      self.logger.warn("No telemetry was found. Returning empty Telemetry()")
    return tel