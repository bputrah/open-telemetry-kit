from .parser import Parser
from .telemetry import Telemetry
from .packet import Packet
from .element import Element, UnknownElement

import xml.etree.ElementTree as ET

class GPXParser(Parser):
  ext = 'gpx'

  def __init__(self, source):
    super().__init__(source)

  def read(self):
    tree = ET.parse(self.source)
    tel = Telemetry()
    self._traverse_tree(tree.getroot(), tel)
    return tel

  def _traverse_tree(self, node, tel):
    for child in node:
      # Ignore namespace if it exists
      tag = child.tag[child.tag.find('}')+1:]
      if tag in {"trkpt", "metadata"}:
        packet = Packet()
        self._extract_node(child, packet)
        tel.append(packet)

      self._traverse_tree(child, tel)
  
  def _extract_node(self, node, packet):
    for key, val in node.items():
      self._add_element(packet, key, val)

    if not node.text.isspace():
      tag = node.tag[node.tag.find('}')+1:]
      self._add_element(packet, tag, node.text.strip())

    for child in node:
      self._extract_node(child, packet)

  def _add_element(self, packet, key, val):
      if key in self.element_dict:
        element_cls = self.element_dict[key]
        packet[element_cls.name] = element_cls(val)
      else: 
        packet[key] = UnknownElement(val)
