from io import BytesIO
from typing import Tuple

def lerp(x: int, x0: int, x1: int, y0: float, y1: float):
  t = (x - x0) / (x1 - x0)
  return (1-t) * y0 + t * y1

def bytes_to_int(byte, issigned=False):
  return int.from_bytes(byte, byteorder="big", signed=issigned)

def bytes_to_float(byte, src: Tuple[int, int], dest: Tuple[float, float]):
  i = int.from_bytes(byte, byteorder="big", signed=(src[0] < 0))
  return lerp(i, src[0], src[1], dest[0], dest[1])

def bytes_to_str(byte):
  return byte.decode("utf-8")

def read_len(klv_stream: BytesIO):
  length = bytes_to_int(klv_stream.read(1))

  if length >= 128:
    length = bytes_to_int(klv_stream.read(length - 128))

  return length

def read_ber_oid(klv_stream: BytesIO):
  byte = bytes_to_int(klv_stream.read(1))

  if byte < 128:
    return byte

  val = 0
  while byte >= 128:
    val = (val << 7) + (byte - 128)
    byte = bytes_to_int(klv_stream.read(1))

  val = (val << 7) + (byte)
  return val
