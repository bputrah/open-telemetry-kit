from .parser import Parser
from .telemetry import Telemetry
from .packet import Packet
from .element import LatitudeElement, LongitudeElement, AltitudeElement
from .element import TimestampElement, DatetimeElement
from .misb_0601 import MISB_0601

import io
import xml.etree.ElementTree as ET
from dateutil import parser as dup
import logging
from typing import List

class KLVParser(Parser):
  def __init__(self, source: str):
    self.source = source
    self.element_dict = {}
    
    for cls in MISB_0601.__subclasses__():
      self.element_dict[cls.tag] = cls

  def read(self):
    pass