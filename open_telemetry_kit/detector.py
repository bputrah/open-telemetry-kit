import os
import json
from .parser import Parser
from typing import Dict, Tuple, Union, List
JSONType = Dict[str, Union[List[Dict[str, Union[str, int]]], Dict[str,Union[str, int]]]]

def split_path(src: str) -> Tuple[str, str, str]:
  path, filename = os.path.split(src)
  name, ext = os.path.splitext(filename)
  return (path, name, ext.lower())

def get_video_metadata(src: str) -> JSONType:
  data_raw = os.popen("ffprobe -v quiet -print_format json -show_format -show_streams " + src).read()
  return json.loads(data_raw)

def write_video_metadata(metadata: JSONType, dest: str):
  with open(os.path.join(dest, "metadata.json"), 'w') as fl:
    json.dump(metadata, fl, indent=3)

def read_video_metadata(src: str):
  with open(src, 'r') as fl:
    metadata = json.load(fl)
  return metadata

def get_embedded_telemetry_type(metadata: JSONType) -> str:
  if "streams" in metadata:
    for stream in metadata["streams"]:
      if stream["codec_type"] == "subtitle" and stream["codec_tag_string"] == "text":
        return "srt"
      elif stream["codec_type"] == "data" and stream["codec_tag_string"] == "KLVA":
        return "klv"

  return None

# If supported return the extension and bool
#   False: Telemetry is not embedded in video file (in it's own file)
#   True: Telemetry is embedded in video file
def get_telemetry_type(src: str) -> Tuple[str, bool]:
  path, _, ext = split_path(src)
  supported = [cls.ext for cls in Parser.__subclasses__()]
  if ext.strip('.') in supported:
    return (ext.strip('.'), False)
  
  metadata = get_video_metadata(src)
  write_video_metadata(metadata, path)
  tel_type = get_embedded_telemetry_type(metadata)
  if tel_type and tel_type in supported:
    return (tel_type, True)
  
  return (None, False)
    
def create_telemetry_parser(src: str) -> Parser:
  tel_type, embedded = get_telemetry_type(src)
  tel_src = src

  if embedded and tel_type == "srt":
    tel_src = extract_embedded_subtitles(tel_src)

  for cls in Parser.__subclasses__():
    if tel_type == cls.ext:
      return cls(tel_src, embedded)

def extract_embedded_subtitles(src: str) -> str:
  path, src_file, _ = split_path(src)
  out = os.path.join(path, src_file) + ".srt"
  cmd = "ffmpeg -y -i " + src + " " + out
  os.system(cmd)
  return out