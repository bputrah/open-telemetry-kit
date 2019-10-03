#!/usr/bin/env python3

# https://docs.python.org/3/reference/datamodel.html#emulating-container-types

from collections import UserList
from packet import Packet
from typing import List

class Telemetry(UserList):
  def __init__(self, packets: List[Packet] = []):
    ##list of elements
    ##should elements be a @property?
    UserList.__init__(self, packets)

  def toJson(self) -> List[Packet]:
    return self.data