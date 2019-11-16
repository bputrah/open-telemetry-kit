from typing import Tuple

def bytes_to_int(byte):
  return int.from_bytes(byte, byteorder="big", signed=False)

def lerp(x: int, x0: int, x1: int, y0: float, y1: float):
  t = (x - x0) / (x1 - x0)
  return (1-t) * y0 + t * y1

def bytes_to_float(byte, src: Tuple[int, int], dest: Tuple[float, float]):
  i = int.from_bytes(byte, byteorder="big", signed=(src[0] < 0))
  return lerp(i, src[0], src[1], dest[0], dest[1])

def bytes_to_str(byte):
  return byte.decode("utf-8")