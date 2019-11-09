def bytes_to_int(bytes):
  return int().from_bytes(bytes, byteorder="bigendian", signed=False)

def lerp(x, x0, x1, y0, y1):
  t = (x - x0) / (x1 - x0)
  return (1-t) * y0 + t * y1

def bytes_to_float(bytes, src_min, src_max, dest_min, dest_max):
  i = int.from_bytes(bytes, byteorder="bigendian", signed=src_min < 0)
  return lerp(i, src_min, src_max, dest_min, dest_max)

#TODO: This function
def bytes_to_str(bytes):
  pass