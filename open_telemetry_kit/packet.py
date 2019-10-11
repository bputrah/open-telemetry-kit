#!/usr/bin/env python3

from collections import UserDict
from typing import Dict

from .element import Element

class Packet(UserDict):
  def __init__(self, elements: Dict[str, Element] = {}):
    UserDict.__init__(self, elements)

  def toJson(self) -> Dict[str, Element]:
    return self.data