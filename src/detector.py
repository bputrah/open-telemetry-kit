import os
import json
from parser import Parser
from typing import Dict, Tuple, Union, List
JSONType = Dict[str, Union[List[Dict[str, Union[str, int]]], Dict[str,Union[str, int]]]]

def split_path(src: str) -> Tuple[str, str, str]:
  path, name = os.path.split(src.lower())
  ext = os.path.splitext(name)[-1]
  return (path, name, ext)

def get_video_metadata(src: str) -> JSONType:
  data_raw = os.popen("ffprobe -v quiet -print_format json -show_format -show_streams " + src).read()
  return json.loads(data_raw)

def write_video_metadata(metadata: JSONType, dest: str):
  with open(dest + "metadata.json", 'w') as file:
    json.dump(metadata, file, indent=3)

def get_embedded_telemetry_type(metadata: JSONType) -> str:
  if "streams" in metadata:
    for stream in metadata["streams"]:
      if stream["codec_type"] == "subtitle" and stream["codec_tag_string"] == "text":
        return "srt"
      elif stream["codec_type"] == "data" and stream["codec_tag_string"] == "KLVA":
        return "klv"
      else:
        return None

def get_telemetry_type(src: str) -> str:
  _, _, ext = split_path(src)
  supported = [cls.ext for cls in Parser.__subclasses__()]
  if ext.strip('.') in supported:
    return ext.strip('.')
  
  metadata = get_video_metadata(src)
  tel_type = get_embedded_telemetry_type(metadata)
  if tel_type and tel_type in supported:
    return tel_type
  
  return None
    
def create_telemetry_parser(src: str) -> Parser:
  tel_type = get_telemetry_type(src)
  for cls in Parser.__subclasses__():
    if tel_type == cls.ext:
      return cls(src)

def extract_embedded_subtitles(src: str) -> str:
  path, src_file, _ = split_path(src)
  out = path + src_file + ".srt"
  cmd = "ffmpeg -y -i " + src + " " + out
  os.system(cmd)
  return out