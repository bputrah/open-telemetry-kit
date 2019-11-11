def bytes_to_int(byte):
  return int.from_bytes(byte, byteorder="big", signed=False)

def lerp(x: int, x0: int, x1: int, y0: float, y1: float):
  t = (x - x0) / (x1 - x0)
  return (1-t) * y0 + t * y1

def bytes_to_float(byte, src_min: int, src_max: int, dest_min: float, dest_max: float):
  i = int.from_bytes(byte, byteorder="big", signed=src_min < 0)
  return lerp(i, src_min, src_max, dest_min, dest_max)

#TODO: This function
def bytes_to_str(byte):
  return byte.decode("utf-8")