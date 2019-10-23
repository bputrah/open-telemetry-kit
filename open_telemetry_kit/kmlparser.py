from .parser import Parser
from .telemetry import Telemetry
from .packet import Packet
from .element import LatitudeElement, LongitudeElement, AltitudeElement
from .element import TimestampElement, DatetimeElement

import io
import xml.etree.ElementTree as ET
import logging
from typing import List

class KMLParser(Parser):
  tel_type = 'kml'

  def __init__(self, source: str, require_timestamp: bool = False):
    super().__init__(source)
    self.ns = dict()
    self.logger = logging.getLogger("OTK.KMLParser")

  def read(self):
    tel = Telemetry()
    tree = ET.parse(self.source)
    self._traverse_tree(tree.getroot(), tel)
    if len(tel) == 0:
      self.logger.warn("No telemetry was found. Returning empty Telemetry()")
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

      if self.require_timestamp and TimestampElement.name not in packet \
          and DatetimeElement.name not in packet:

        self.logger.error("Could not find any time elements when require_timestamp was set")
        raise Exception("No timestamp or datetime found with 'require_timestamp' set to true.")

      if len(packet) > 0:
        self.logger.info("Adding new packet.")
        tel.append(packet)
      else:
        self.logger.warn("No telemetry was found in node. Packet is empty, skipping.")

  def _read_track(self, node: ET.Element, tel: Telemetry):
    packets = []
    for child in node:
      tag = child.tag[child.tag.find('}')+1:]
      if tag == "when":
        packet = Packet()
        packet[DatetimeElement.name] = DatetimeElement(child.text)
        packets.append(packet)
      elif tag == "coord":
        packet = packets.pop(0)
        coords = child.text.split()
        self._process_coords(coords, packet)

        if self.require_timestamp and TimestampElement.name not in packet \
            and DatetimeElement.name not in packet:

          self.logger.error("Could not find any time elements when require_timestamp was set")
          raise Exception("No timestamp or datetime found with 'require_timestamp' set to true.")

        if len(packet) > 0:
          self.logger.info("Adding new packet.")
          tel.append(packet)
        else:
          self.logger.warn("No telemetry was found in node. Packet is empty, skipping.")

  def _process_coords(self, coords: List[str], packet: Packet):
      packet[LatitudeElement.name] = LatitudeElement(coords[0]) 
      packet[LongitudeElement.name] = LongitudeElement(coords[1])
      if len(coords) == 3:
        packet[AltitudeElement.name] = AltitudeElement(coords[2])
