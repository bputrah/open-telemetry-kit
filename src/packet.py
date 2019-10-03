#!/usr/bin/env python3

from collections import UserDict
from element import Element
from typing import Dict

class Packet(UserDict):
  def __init__(self, elements: Dict[str, Element] = {}):
    UserDict.__init__(self, elements)

  def toJson(self) -> Dict[str, Element]:
    return self.data