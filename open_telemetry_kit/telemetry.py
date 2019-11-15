#!/usr/bin/env python3

# https://docs.python.org/3/reference/datamodel.html#emulating-container-types

import open_telemetry_kit as otk
from collections import UserList
from typing import List
from .packet import Packet
from datetime import timedelta
from dateutil import parser as dup

class Telemetry(UserList):
  def __init__(self, packets: List[Packet] = []):
    UserList.__init__(self, packets)

  def toJson(self) -> List[Packet]:
    return self.data

  def split_telemetry(self, videos: List[str], video_offset: int = 0) -> List['Telemetry']:
    # Split a single telemetry object into multiple objects
    # Use case: Multiple video files but only a single telemetry file
    # Expects list of videos in form of their directory location
    # Get creation time and duration of each video
    # Extract the corresponding subset of the telemetry
    # Assumes telemetry is sorted
    # Video offset used to offset video timestamps in the event of a clock mismatch
    has_datetime = "datetime" in self.data[0]
    has_timestamp = "timestamp" in self.data[0]
    if not has_datetime and not has_timestamp:
      return None

    time_and_dur = []
    for video in videos:
      video_metadata = otk.detector.read_video_metadata(video)
      
      if video_metadata and "streams" in video_metadata:
        video_creation = None
        video_duration = None
        if "tags" in video_metadata["streams"][0]     \
           and "creation_time" in video_metadata["streams"][0]["tags"]:
          video_creation = dup.parse(video_metadata["streams"][0]["tags"]["creation_time"])
        else:
          return None

        if "duration" in video_metadata["streams"][0]:
          video_duration = float(video_metadata["streams"][0]["duration"])
        else:
          return None

        if has_timestamp:
          video_creation = video_creation.timestamp() + video_offset
        time_and_dur.append((video_creation, video_duration, video))
      else:
        return None

    time_and_dur.sort(key=lambda vid: vid[0])

    split = {}
    start_idx = 0
    end_idx = 0
    for vid in time_and_dur:
      if vid[0] > self.data[-1]['timestamp'].to_seconds().value or \
         vid[0] + vid[1] > self.data[-1]['timestamp'].value:
        # Video not fully contained in telemetry
        break
      if has_timestamp:
        start_idx += next(idx for idx, packet in enumerate(self.data[start_idx:])
                          if packet['timestamp'].to_seconds().value >= vid[0])

        end_idx = start_idx + \
                  next(idx for idx, packet in enumerate(self.data[start_idx:]) 
                       if packet['timestamp'].to_seconds().value > vid[0] + vid[1])

      elif has_datetime:
        td = timedelta(seconds=vid[1])
        start_idx = next(idx for idx, packet in enumerate(self.data[start_idx:])
                                if packet['datetime'].value >= vid[0])

        end_idx = next(idx for idx, packet in enumerate(self.data[start_idx:]) 
                              if packet['datetime'].value > vid[0] + td)

      if (start_idx < end_idx):
        split[vid[2]] = (Telemetry(self.data[start_idx:end_idx]))
        start_idx = end_idx
    
    return split
