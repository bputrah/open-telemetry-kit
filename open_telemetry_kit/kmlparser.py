from .parser import Parser
from .telemetry import Telemetry
from .packet import Packet
from .element import LatitudeElement, LongitudeElement, AltitudeElement, DatetimeElement
from typing import List

import io
import xml.etree.ElementTree as ET

class KMLParser(Parser):
  ext = 'kml'

  def __init__(self, source: str):
    super().__init__(source)
    self.ns = dict()

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
      elif tag == "Track":
        self._read_track(child, tel)
      
      self._traverse_tree(child, tel)

  def _read_coords(self, sstream: io.StringIO , tel: Telemetry):
    for line in sstream:
      packet = Packet()
      coords = line.strip().split(',')
      self._process_coords(coords, packet)
      tel.append(packet)

  def _read_track(self, node: ET.Element, tel: Telemetry):
    packets = []
    for child in node:
      tag = child.tag[child.tag.find('}')+1:]
      if tag == "when":
        packet = Packet()
        packet["datetime"] = DatetimeElement(child.text)
        packets.append(packet)
      elif tag == "coord":
        packet = packets.pop(0)
        coords = child.text.split()
        self._process_coords(coords, packet)
        tel.append(packet)

  def _process_coords(self, coords: List[str], packet: Packet):
      packet[LatitudeElement.name] = LatitudeElement(coords[0]) 
      packet[LongitudeElement.name] = LongitudeElement(coords[1])
      if len(coords) == 3:
        packet[AltitudeElement.name] = AltitudeElement(coords[2])
