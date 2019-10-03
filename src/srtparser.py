#example:
# 1
# 00:00:00,000 --> 00:00:00,033
# <font size="36">FrameCnt : 1, DiffTime : 33ms
# 2019-09-25 01:22:35,085,332
# [iso : 110] [shutter : 1/200.0] [fnum : 280] [ev : 0.7] [ct : 5064] [color_md : default] [focal_len : 240] [latitude: 0.608553] [longtitude: -1.963763] [altitude: 1429.697998] </font>

# 2
# 00:00:00,033 --> 00:00:00,066
# <font size="36">FrameCnt : 2, DiffTime : 33ms
# 2019-09-25 01:22:35,118,697
# [iso : 110] [shutter : 1/200.0] [fnum : 280] [ev : 0.7] [ct : 5064] [color_md : default] [focal_len : 240] [latitude: 0.608553] [longtitude: -1.963763] [altitude: 1429.697998] </font>

# Alternative GPS form:
# GPS(-122.3699,37.5929,19) BAROMETER:64.3 (long, lat)
# GPS(37.8757,-122.3061,0.0M) BAROMETER:36.9M (lat, long)

from datetime import timedelta
import pandas as pd
import re

from parser import Parser
from telemetry import Telemetry
from packet import Packet
import element

from element import Element
from typing import Dict

class SRTParser(Parser):
  ext = "srt"

  def __init__(self, source: str):
    self.source = source
    self.element_dict = {}
    for cls in element.Element.__subclasses__():
      for name in cls.names:
        self.element_dict[name] = cls

  def read(self) -> Telemetry:
    tel = Telemetry()
    with open(self.source, 'r') as src:
      # read block
      block = ""
      for line in src:
        if line == '\n':
          packet = Packet()
          sec_line_beg = block.find('\n') + 1
          sec_line_end = block.find('\n', sec_line_beg)
          # get block times
          self._extractTimeframe(block[sec_line_beg: sec_line_end], packet)
          # get datetime
          self._extractTimestamp(block[sec_line_end + 1 :], packet)
          # search GPS
          self._extractData(block[sec_line_end + 1:], packet)
          tel.append(packet)
          block = ""
        else:
          block += line

      return tel

  def _extractTimeframe(self, line: str, packet: Dict[str, Element]):
    sep_pos = line.find("-->")
    tfb = pd.Timestamp(line[:sep_pos].strip())
    tfb = timedelta(hours=tfb.hour, minutes=tfb.minute, seconds=tfb.second, microseconds=tfb.microsecond).total_seconds()
    packet["timeFrameBegin"] = element.TimeframeBeginElement.fromSRT(tfb)
    tfe = pd.Timestamp(line[sep_pos+3:].strip())
    tfe = timedelta(hours=tfe.hour, minutes=tfe.minute, seconds=tfe.second, microseconds=tfe.microsecond).total_seconds()
    packet["timeFrameEnd"] = element.TimeframeBeginElement.fromSRT(tfe)

  def _extractTimestamp(self, block: str, packet: Dict[str, Element]):
    # This should find any reasonably formatted (and some not so reasonably formatted) datetimes
    # 1+ digits, '/', '-', or '.', 1+ digits, the same separator previously found
    #   1+ digits, 1+ whitespace, 1+ digits, ':' 1+ digits,
    #   ':', 1+ digits, '.' or ',', any amount of whitespace, any number of digits, 
    #   the same separator previously found, any amount of whitespace, any number of digits 
    ts = re.search(r"\d+([\/\-\.])\d+\1\d+\s+\d+:\d+:\d+([.,])?\s*\d*\2?\s*\d*", block)

    # pandas timestamp is pretty good, but can't handle the double microsecond separator 
    # that sometimes shows up in DJIs stuff
    # Also, convert to epoch microseconds while we're at it
    if ts:
      micro_syn = ts[2]
      ts = ts[0]
      if ts.count(micro_syn) > 1:
        #concatentate timestamp pre-2nd separator with post-2nd separator
        ts = ts[:ts.rfind(micro_syn)] + ts[ts.rfind(micro_syn)+1:]
      
      ts = int(pd.Timestamp(ts).to_pydatetime().timestamp() * 1000)
      packet["timestamp"] = element.TimestampElement.fromSRT(ts)

  def _extractGPS(self, block: str, packet: Dict[str, Element]):
    gps_pos = block.find("GPS")
    end_line = block.find('\n', gps_pos)

    val1_end = block.find(',', gps_pos)
    val1 = block[gps_pos+3 : val1_end] 
    val2_end = block.find(',', val1_end + 1)
    val2 = block[val1_end : val2_end]
    # lat, long
    if 'M' == block[end_line - 1]:
      packet["Latitude"] = element.LatitudeElement.fromSRT(val1.strip(" ,()"))
      packet["Longitude"] = element.LongitudeElement.fromSRT(val2.strip(" ,()"))
    #long, lat
    else:
      packet["Longitude"] = element.LatitudeElement.fromSRT(val1.strip(" ,()"))
      packet["Latitude"] = element.LongitudeElement.fromSRT(val2.strip(" ,()"))

    alt_end = block.find(')', val2_end)
    alt = block[val2_end : alt_end]
    bar_pos = block.index("BAROMETER", gps_pos, end_line)
    if bar_pos:
      bar_end = bar_pos + 9 #len("BAROMETER")
      alt = block[bar_end : ].strip(' M:,\n')
    
    packet["Altitude"] = element.AltitudeElement.fromSRT(alt)

  def _extractData(self, block: str, packet: Dict[str, Element]):
    if "GPS" in block:
      self._extractGPS(block, packet)
    else:
      # DJI wraps their telemetry in '[]' 
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
