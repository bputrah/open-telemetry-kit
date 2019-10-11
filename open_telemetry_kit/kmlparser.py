from .parser import Parser
from .telemetry import Telemetry
from .packet import Packet
from .element import LatitudeElement, LongitudeElement, AltitudeElement

import io
import xml.etree.ElementTree as ET

class KMLParser(Parser):
  ext = 'kml'

  def __init__(self, source: str):
    super().__init__(source)

  def read(self):
    tel = Telemetry()
    tree = ET.parse(self.source)
    self._traverse_tree(tree.getroot(), tel)
    return tel

  def _traverse_tree(self, node: ET.Element, tel: Telemetry):
    for child in node:
      tag = child.tag[child.tag.find('}')+1:]
      if tag == "coordinates" and child.text:
        self._read_coords(io.StringIO(child.text.strip()), tel)
      
      self._traverse_tree(child, tel)

  def _read_coords(self, sstream: io.StringIO , tel: Telemetry):
    for line in sstream:
      packet = Packet()
      coords = line.strip().split(',')
      packet[LatitudeElement.name] = LatitudeElement.fromKML(coords[0]) 
      packet[LongitudeElement.name] = LongitudeElement.fromKML(coords[1])
      if len(coords) == 3:
        packet[AltitudeElement.name] = AltitudeElement.fromKML(coords[2])
      tel.append(packet)
