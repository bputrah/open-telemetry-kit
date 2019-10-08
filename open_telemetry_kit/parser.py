from abc import abstractmethod
from .telemetry import Telemetry

class Parser():
  @property
  @classmethod
  @abstractmethod
  def ext(self) -> str:
    pass

  @abstractmethod
  def read(self) -> Telemetry:
    pass