#!/usr/bin/env python3

# https://docs.python.org/3/reference/datamodel.html#emulating-container-types

from collections import UserList
from typing import List
from .packet import Packet

class Telemetry(UserList):
  def __init__(self, packets: List[Packet] = []):
    UserList.__init__(self, packets)

  def toJson(self) -> List[Packet]:
    return self.data