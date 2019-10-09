from .parser import Parser
from .telemetry import Telemetry
from .packet import Packet
from .element import Element

import xml.etree.ElementTree as ET

class KMLParser(Parser):
  ext = 'kml'

  def __init__(self, source):
    super().__init__(source)