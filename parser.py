from abc import abstractmethod

class Parser():
  @property
  @classmethod
  @abstractmethod
  def ext(self):
    pass

  @abstractmethod
  def read(self):
    pass