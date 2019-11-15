#!/usr/bin/env python3

from .klv_common import bytes_to_int, bytes_to_float, bytes_to_str
import logging
from abc import ABCMeta
from abc import abstractmethod
from datetime import datetime
from dateutil import parser as dup
from typing import Tuple

class MISB_0601(metaclass=ABCMeta):
  @classmethod
  @abstractmethod
  def fromMISB(cls, value):
    pass

  @property
  @classmethod
  @abstractmethod
  def misb_key(cls):
    pass

  @property
  @classmethod
  @abstractmethod
  def misb_name(cls) -> str:
    pass

  @property
  @classmethod
  @abstractmethod
  def misb_tag(cls) -> int:
    pass

  @property
  @classmethod
  @abstractmethod
  def misb_units(cls) -> str:
    pass

class MISB_int(MISB_0601):
  @classmethod
  def fromMISB(cls, value):
    return cls(bytes_to_int(value))

class MISB_float(MISB_0601):
  @property
  @classmethod
  @abstractmethod
  def __domain(cls) -> Tuple[int, int]:
    pass


  @property
  @classmethod
  @abstractmethod
  def __range(cls) -> Tuple[int, int]:
    pass

  @property
  @classmethod
  @abstractmethod
  def __invalid(cls) -> bytes:
    pass

  @classmethod
  def fromMISB(cls, value):
    if cls.__invalid and value == cls.__invalid:
      return cls(None)
    else:
      return cls(bytes_to_float(value, cls.__domain, cls.__range))

class MISB_str(MISB_0601):
  @classmethod
  def fromMISB(cls, value):
    return cls(bytes_to_str(value))
