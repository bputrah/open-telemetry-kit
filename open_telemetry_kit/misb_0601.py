
#!/usr/bin/env python3

import logging
from abc import ABCMeta
from abc import abstractmethod
from datetime import datetime
from dateutil import parser as dup
from typing import Any, Set

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

