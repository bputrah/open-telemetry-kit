from .parser import Parser
from .telemetry import Telemetry
from .packet import Packet
from .element import Element, UnknownElement
from .element import TimestampElement, TimeframeBeginElement, TimeframeEndElement, DatetimeElement
from .element import LatitudeElement, LongitudeElement, AltitudeElement
import open_telemetry_kit.detector as detector

from datetime import timedelta
from dateutil import parser as dup
import re
import os
from typing import Dict


class SRTParser(Parser):
  ext = "srt"

  def __init__(self, 
               source: str, 
               is_embedded: bool = False, 
               convert_to_epoch: bool = False, 
               require_timestamp: bool = False):
    super().__init__(source, require_timestamp)
    self.is_embedded = is_embedded
    self.beg_timestamp = 0
    self.convert_to_epoch = convert_to_epoch

  def read(self) -> Telemetry:
    tel = Telemetry()

    _, _, ext = detector.split_path(self.source)
    if self.is_embedded and ext != ".srt":
      if self.require_timestamp:
        video_metadata = detector.read_video_metadata(self.source)
        video_datetime = video_metadata["streams"][0]["tags"]["creation_time"]
        self.beg_timestamp = int(dup.parse(video_datetime).timestamp() * 1000)

      srt = detector.read_embedded_subtitles(self.source)
      self._process(srt.splitlines(True), tel)

    else:
      with open(self.source, 'r') as srt:
        self._process(srt, tel)

    return tel

  def _process(self, srt: str, tel: Telemetry):
    block = ""
    for line in srt:
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

  # Example timeframe:
  # 00:00:00,033 --> 00:00:00,066
  def _extractTimeframe(self, line: str, packet: Dict[str, Element]):
    sep_pos = line.find("-->")
    tfb = (dup.parse(line[:sep_pos].strip()) - dup.parse("00:00:00")).total_seconds()
    packet["timeframeBegin"] = TimeframeBeginElement(tfb)
    tfe = (dup.parse(line[sep_pos+3:].strip()) - dup.parse("00:00:00")).total_seconds()
    packet["timeframeEnd"] = TimeframeEndElement(tfe)

  # Example timestamp
  # 2019-09-25 01:22:35,118,697
  def _extractTimestamp(self, block: str, packet: Dict[str, Element]):
    # This should find any reasonably formatted (and some not so reasonably formatted) datetimes
    # Looks for:
    # 1+ digits, '/', '-', or '.', 1+ digits, the same separator previously found
    #   1+ digits, 1+ whitespace, 1+ digits, ':' 1+ digits,
    #   ':', 1+ digits, '.' or ',', any amount of whitespace, any number of digits, 
    #   the same separator previously found, any amount of whitespace, any number of digits 
    dt = re.search(r"\d+([\/\-\.])\d+\1\d+\s+\d+:\d+:\d+([.,])?\s*\d*\2?\s*\d*", block)

    # dateutil is pretty good, but can't handle the double microsecond separator 
    # that sometimes shows up in DJIs telemetry so check to see if it exists and get rid of it
    # Also, convert to epoch microseconds while we're at it
    if dt:
      micro_syn = dt[2]
      dt = dt[0]
      if micro_syn and dt.count(micro_syn) > 1:
        #concatentate timestamp pre-2nd separator with post-2nd separator
        dt = dt[:dt.rfind(micro_syn)] + dt[dt.rfind(micro_syn)+1:]
      
      dt = int(dup.parse(dt))#.timestamp() * 1000)
      if (self.convert_to_epoch):
        dt = dt.timestamp() * 1000
        packet["timestamp"] = TimestampElement(dt)
      else:
        packet["datetime"] = DatetimeElement(dt)
    
    elif self.is_embedded and self.beg_timestamp != 0:
      tfb = packet["timeframeBegin"].value
      tfe = packet["timeframeEnd"].value
      dt = 500 * (tfb+tfe) #average and convert to microseconds (sum * 1000/2)
      packet["timestamp"] = TimestampElement(self.beg_timestamp + dt)

  # DJI
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
      packet["latitude"] = LatitudeElement(val1.strip(" ,()"))
      packet["longitude"] = LongitudeElement(val2.strip(" ,()"))
    #long, lat
    else:
      packet["longitude"] = LatitudeElement(val1.strip(" ,()"))
      packet["latitude"] = LongitudeElement(val2.strip(" ,()"))

    alt = block[val2_end : gps_end]

    # Favor BAROMETER measurement over altitude measurement
    bar_pos = block.find("BAROMETER", gps_pos, end_line)
    if bar_pos > 0:
      bar_end = bar_pos + 9 #len("BAROMETER")
      alt = block[bar_end : end_line]
    
    packet["altitude"] = AltitudeElement(alt.strip(' ,():M\n'))

  # DJI
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
          packet[element_cls.name] = element_cls(data[i+1])
        else:
          packet[key] = UnknownElement(data[i+1])
