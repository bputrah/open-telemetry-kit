#example:
# 1
# 00:00:00,000 --> 00:00:00,033
# <font size="36">FrameCnt : 1, DiffTime : 33ms
# 2019-09-25 01:22:35,085,332
# [iso : 110] [shutter : 1/200.0] [fnum : 280] [ev : 0.7] [ct : 5064] [color_md : default] [focal_len : 240] [latitude: 0.608553] [longtitude: -1.963763] [altitude: 1429.697998] </font>

# 2
# <font size="36">FrameCnt : 2, DiffTime : 33ms
# [iso : 110] [shutter : 1/200.0] [fnum : 280] [ev : 0.7] [ct : 5064] [color_md : default] [focal_len : 240] [latitude: 0.608553] [longtitude: -1.963763] [altitude: 1429.697998] </font>

from datetime import timedelta
from dateutil import parser as dup
import re
from typing import Dict
import os

from .parser import Parser
from .telemetry import Telemetry
from .packet import Packet
import open_telemetry_kit.element as element
from .element import Element
import open_telemetry_kit.detector as detector

class SRTParser(Parser):
  ext = "srt"

  def __init__(self, source: str, is_embedded: bool = False):
    super().__init__(source)
    self.is_embedded = is_embedded
    self.beg_timestamp = 0

  def read(self) -> Telemetry:
    if self.is_embedded:
      path, _, _ = detector.split_path(self.source)
      metadata = detector.read_video_metadata(os.path.join(path, "metadata.json"))
      datetime = metadata["streams"][0]["tags"]["creation_time"]
      self.beg_timestamp = int(dup.parse(datetime).timestamp() * 1000)

    tel = Telemetry()
    with open(self.source, 'r') as src:
      block = ""
      for line in src:
        if line == '\n' and len(block) > 0:
          packet = Packet()
          sec_line_beg = block.find('\n') + 1
          sec_line_end = block.find('\n', sec_line_beg)
          self._extractTimeframe(block[sec_line_beg: sec_line_end], packet)
          self._extractTimestamp(block[sec_line_end + 1 :], packet)
          self._extractData(block[sec_line_end + 1:], packet)
          tel.append(packet)
          block = ""
        elif line == '\n':
          continue
        else:
          block += line

      return tel

  # Example timeframe:
  # 00:00:00,033 --> 00:00:00,066
  def _extractTimeframe(self, line: str, packet: Dict[str, Element]):
    sep_pos = line.find("-->")
    tfb = (dup.parse(line[:sep_pos].strip()) - dup.parse("00:00:00")).total_seconds()
    packet["timeframeBegin"] = element.TimeframeBeginElement.fromSRT(tfb)
    tfe = (dup.parse(line[sep_pos+3:].strip()) - dup.parse("00:00:00")).total_seconds()
    packet["timeframeEnd"] = element.TimeframeBeginElement.fromSRT(tfe)

  # Example timestamp
  # 2019-09-25 01:22:35,118,697
  def _extractTimestamp(self, block: str, packet: Dict[str, Element]):
    # This should find any reasonably formatted (and some not so reasonably formatted) datetimes
    # Looks for:
    # 1+ digits, '/', '-', or '.', 1+ digits, the same separator previously found
    #   1+ digits, 1+ whitespace, 1+ digits, ':' 1+ digits,
    #   ':', 1+ digits, '.' or ',', any amount of whitespace, any number of digits, 
    #   the same separator previously found, any amount of whitespace, any number of digits 
    ts = re.search(r"\d+([\/\-\.])\d+\1\d+\s+\d+:\d+:\d+([.,])?\s*\d*\2?\s*\d*", block)

    # dateutil is pretty good, but can't handle the double microsecond separator 
    # that sometimes shows up in DJIs telemetry so check to see if it exists and get rid of it
    # Also, convert to epoch microseconds while we're at it
    # TODO: conversion to epoch shouldn't be forced. Save as it's read in and add a funtion
    #       to convert if the user desires
    if ts:
      micro_syn = ts[2]
      ts = ts[0]
      if micro_syn and ts.count(micro_syn) > 1:
        #concatentate timestamp pre-2nd separator with post-2nd separator
        ts = ts[:ts.rfind(micro_syn)] + ts[ts.rfind(micro_syn)+1:]
      
      ts = int(dup.parse(ts).timestamp() * 1000)
      packet["timestamp"] = element.TimestampElement.fromSRT(ts)
    
    elif self.is_embedded and self.beg_timestamp != 0:
      tfb = packet["timeframeBegin"].value
      tfe = packet["timeframeEnd"].value
      ts = 500 * (tfb+tfe) #average and convert to microseconds (sum * 1000/2)
      packet["timestamp"] = element.TimestampElement.fromSRT(self.beg_timestamp + ts)

  # Looks for GPS telemetry of the form:
  # GPS(-122.3699,37.5929,19) BAROMETER:64.3 //(long, lat) OR
  # GPS(37.8757,-122.3061,0.0M) BAROMETER:36.9M //(lat, long)
  def _extractGPS(self, block: str, packet: Dict[str, Element]):
    gps_pos = block.find("GPS")
    gps_end = block.find(')', gps_pos)
    end_line = block.find('\n', gps_end)

    val1_end = block.find(',', gps_pos)
    val1 = block[gps_pos+3 : val1_end] 
    val2_end = block.find(',', val1_end + 1)
    val2 = block[val1_end : val2_end]
    # lat, long
    if 'M' == block[gps_end - 1]:
      packet["latitude"] = element.LatitudeElement.fromSRT(val1.strip(" ,()"))
      packet["longitude"] = element.LongitudeElement.fromSRT(val2.strip(" ,()"))
    #long, lat
    else:
      packet["longitude"] = element.LatitudeElement.fromSRT(val1.strip(" ,()"))
      packet["latitude"] = element.LongitudeElement.fromSRT(val2.strip(" ,()"))

    alt = block[val2_end : gps_end]

    # Favor BAROMETER measurement over altitude measurement
    bar_pos = block.find("BAROMETER", gps_pos, end_line)
    if bar_pos > 0:
      bar_end = bar_pos + 9 #len("BAROMETER")
      alt = block[bar_end : end_line]
    
    packet["altitude"] = element.AltitudeElement.fromSRT(alt.strip(' ,():M\n'))

  # Looks for telemetry of the form:
  # [iso : 110] [shutter : 1/200.0] [fnum : 280] [ev : 0.7] [ct : 5064] [color_md : default] [focal_len : 240] [latitude: 0.608553] [longtitude: -1.963763] [altitude: 1429.697998] 
  def _extractData(self, block: str, packet: Dict[str, Element]):
    if "GPS" in block:
      self._extractGPS(block, packet)
    else:
      # find the first '[' and last ']'
      data_start = block.find('[')
      data_end = block.rfind(']')
      data = block[data_start : data_end]

      # This will split on the common delimters found in DJIs srts and return a list
      # List _should_ be alternating keyword, value barring nothing weird from DJI
      # which they have proven is not a safe assumption
      data = re.split(r"[\[\]\s:]+", data)
      if not data[0]: #remove empty string from regex search
        data.pop(0)
      
      for i in range(0, len(data), 2):
        key = data[i]
        if key in self.element_dict:
          element_cls = self.element_dict[key]
          packet[element_cls.name] = element_cls.fromSRT(data[i+1])
        else:
          packet[key] = element.UnknownElement(data[i+1])
