#!/usr/bin/env python3

import csv
import logging

from parser import Parser
from flightpath import FlightPath
from packet import Packet
import element

class CSVParser(Parser):
  ext = ".csv"

  def __init__(self, src):
    self.__source = src
    self.element_dict = {}
    for cls in element.Element.__subclasses__():
      for name in cls.names:
        self.element_dict[name] = cls

  def __repr__(self):
    #TODO: figure out what the fuck I'm supposed to do here...
    pass

  @property
  def source(self):
    return self.__source

  @source.setter
  def source(self, src):
    #TODO: some sort of directory validation?
    #logging.info("Creating new CSV Parser with source: %s", src)
    self.__source = src

  def read(self):
    fp = FlightPath()
    with open(self.source, newline='') as csvfile:
      reader =  csv.DictReader(csvfile)
      for row in reader:
        packet = Packet()
        for key, val in row.items():
          if key in self.element_dict:
            #element_dict[key] returns a class
            element_cls = self.element_dict[key]
            packet[element_cls.name] = element_cls.fromCSV(val)
          else:
            packet[key] = element.UnknownElement(val)
        
        fp.append(packet)

    return fp