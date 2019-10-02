#!/usr/bin/env python3

from collections import UserDict

class Packet(UserDict):
  def __init__(self, elements = {}):
    UserDict.__init__(self, elements)
    # self.__elements = elements

  def toJson(self):
    return self.data