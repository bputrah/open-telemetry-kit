#!/usr/bin/env python3

# https://docs.python.org/3/reference/datamodel.html#emulating-container-types

from collections import UserList
from typing import List
from .packet import Packet

class Telemetry(UserList):
  def __init__(self, packets: List[Packet] = []):
    UserList.__init__(self, packets)

  def __str__(self):
    #TODO: Implement me
    # return str(self.data) 
    pass

  def __repr__(self):
    #TODO: Implement me
    # return UserList.__repr__(self.data)
    pass

  def toJson(self) -> List[Packet]:
    return self.data