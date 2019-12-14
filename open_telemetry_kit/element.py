#!/usr/bin/env python3

from abc import ABCMeta
from abc import abstractmethod
from typing import Any, Set

class Element(metaclass=ABCMeta):
  def __init__(self, value: Any):
    self.value = value

  def __str__(self):
    # return '{}'.format(self.value)
    return str(self.value)

  def __repr__(self) -> str:
    return "{}('{}')".format(self.__class__.__name__, self.value)

  @property
  @classmethod
  @abstractmethod
  def name(cls) -> str:
    pass

  @property
  @classmethod
  @abstractmethod
  def names(cls) -> Set[str]:
    pass

  def toJson(self) -> Any:
    return self.value

class UnknownElement(Element):
  name = "unknown"
  names = {}

  def __init__(self, value: str):
    self.value = str(value)
