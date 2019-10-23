from .telemetry import Telemetry
from .element import Element
from abc import ABCMeta
from abc import abstractmethod

class Parser(metaclass=ABCMeta):
  def __init__(self, source, require_timestamp: bool = False):
    self.source = source
    self.require_timestamp = require_timestamp
    self.element_dict = {}
    for cls in Element.__subclasses__():
      for name in cls.names:
        self.element_dict[name] = cls

  def __str__(self) -> str:
    return "{}('{}')".format(self.__class__.__name__, self.source)

  def __repr__(self) -> str:
    return "{}('{}')".format(self.__class__.__name__, self.source)

  @property
  @classmethod
  @abstractmethod
  def tel_type(self) -> str:
    pass

  @abstractmethod
  def read(self) -> Telemetry:
    pass