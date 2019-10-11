from abc import ABCMeta
from abc import abstractmethod
from .telemetry import Telemetry
from .element import Element

class Parser(metaclass=ABCMeta):
  def __init__(self, source):
    self.source = source
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
  def ext(self) -> str:
    pass

  @abstractmethod
  def read(self) -> Telemetry:
    pass