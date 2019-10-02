#!/usr/bin/env python3

# https://docs.python.org/3/reference/datamodel.html#emulating-container-types

from collections import UserList

class FlightPath(UserList):
  def __init__(self, packets=[]):
    ##list of elements
    ##should elements be a @property?
    UserList.__init__(self, packets)

  def toJson(self):
    return self.data