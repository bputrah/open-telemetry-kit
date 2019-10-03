import os
import json
from parser import Parser

def split_path(src):
  path, src_file = os.path.split(src.lower())
  ext = os.path.splitext(src_file)[-1]
  return path, src_file, ext

def get_video_metadata(src):
  data_raw = os.popen("ffprobe -v quiet -print_format json -show_format -show_streams " + src).read()
  return json.loads(data_raw)

def get_embedded_data_type(metadata):
  if "streams" in metadata:
    for stream in metadata["streams"]:
      if stream["codec_type"] in ("video", "audio"):
        continue
      else:
        return (stream["codec_type"], stream["codec_name"], stream["codec_tag_string"])

def extract_embedded_subtitles(src):
  path, src_file, _ = split_path(src)
  out = path + src_file + ".srt"
  cmd = "ffmpeg -y -i " + src + " " + out
  os.system(cmd)
  return out
