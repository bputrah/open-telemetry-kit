#!/usr/bin/env python3

from .misb_0601 import MISB_0601
import logging
from abc import ABCMeta
from abc import abstractmethod
from datetime import datetime
from dateutil import parser as dup
from typing import Any, Set

class Element(metaclass=ABCMeta):
  def __init__(self, value: Any):
    self.value = value

  def __str__(self):
    # return '{}'.format(self.value)
    return str(self.value)

  def __repr__(self) -> str:
    return "{}('{}')".format(self.__class__.__name__, self.value)

  @property
  @classmethod
  @abstractmethod
  def name(cls) -> str:
    pass

  @property
  @classmethod
  @abstractmethod
  def names(cls) -> Set[str]:
    pass

  def toJson(self) -> Any:
    return self.value

class ChecksumElement(Element, MISB_0601):
  name = "checksum"
  names = {"checksum", "Checksum"}

  misb_name = "Checksum"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 02 03 01 00 00 00"
  misb_tag = 1
  misb_units = "None"

  def __init__(self, value: int):
    self.value = int(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # self.value = bytes_to_hex(value)
  
class TimestampElement(Element, MISB_0601):
  name = "timestamp"
  names = {"timestamp", "Timestamp", "time stamp", "Time Stamp"}

  misb_name = "Precision Time Stamp"
  misb_key = "06 0E 2B 34 01 01 01 03 07 02 01 01 01 05 00 00"
  misb_tag = 2
  misb_units = "Microseconds"
  _unit_code = {0 : "seconds",
                 1 : "milliseconds",
                 2 : "microseconds"}

  # Python returns a float value in seconds for timestamp so conform to that 
  def __init__(self, value: float):
    self.value = float(value)
    self.units = self._unit_code[0]

  def __repr__(self) -> str:
    return "{}('{}','{}')".format(self.__class__.__name__, self.value, self.units)

  def to_seconds(self):
    if self.units == self._unit_code[0]:
      return self
    elif self.units == self._unit_code[1]:
      self.value = self.value * 1e-3
      self.units = self._unit_code[0]
      return self
    elif self.units == self._unit_code[2]:
      self.value = self.value * 1e-6
      self.units = self._unit_code[0]
      return self

  def to_milliseconds(self):
    if self.units == self._unit_code[0]:
      self.value = self.value * 1e3
      self.units = self._unit_code[1]
      return self
    elif self.units == self._unit_code[1]:
      return self
    elif self.units == self._unit_code[2]:
      self.value = self.value * 1e-3
      self.units = self._unit_code[1]
      return self

  def to_microseconds(self):
    if self.units == self._unit_code[0]:
      self.value = int(self.value * 1e6)
      self.units = self._unit_code[2]
      return self
    elif self.units == self._unit_code[1]:
      self.value = int(self.value * 1e3)
      self.units = self._unit_code[2]
      return self
    elif self.units == self._unit_code[2]:
      return self

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # self.value = bytes_to_int(value)

class DatetimeElement(Element):
  name = "datetime"
  names = {"datetime", "Datetime", "DateTime", "time"}

  def __init__(self, value: datetime):
    self.value = dup.parse(value)

  def toJson(self) -> str:
    return str(self.value)

class MissionIDElement(Element, MISB_0601):
  name = "missionID" 
  names = {"missionID", "MissionId", "Missionid", "missionID",
           "missionId", "missionid"}

  misb_name = "Mission ID"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 04 01 03 00 00 00"
  misb_tag = 3
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # self.value = bytes_to_str(value)

class PlatformHeadingAngleElement(Element, MISB_0601):
  name = "platformHeadingAngle"
  names = {"platformHeadingAngle", "PlatformHeadingAngle", "platformheadingangle",
           "headingAngle", "HeadingAngle", "headingangle", "Heading Angle",
           "heading angle", "heading", "Heading"}

  misb_name = "Platform Heading Angle"
  misb_key = "06 0E 2B 34 01 01 01 07 07 01 10 01 06 00 00 00"
  misb_tag = 5
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0 to 360
    # 0 to (2^16)-1
    # python built in int().from_bytes
    # then map to range
    # self.value = bytes_to_int(value) * (360/65535)

class PlatformPitchAngleElement(Element, MISB_0601):
  name = "platformPitchAngleShort"
  names = {"platformPitchAngleShort", "PlatformPitchAngleShort", "platformpitchangleshort",
           "pitchAngleShort", "PitchAngleShort", "pitchangleshort", "Pitch Angle Short", 
           "pitch angle short"}

  misb_name = "Platform Pitch Angle"
  misb_key = "06 0E 2B 34 01 01 01 07 07 01 10 01 05 00 00 00"
  misb_tag = 6
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0x8000= "Out of Range"
    # -20 to 20
    # -((2^15)-1) to (2^15)-1
    # python built in int().from_bytes
    # then map to range
    # self.value = bytes_to_int(value) * (40/65535)

class PlatformPitchAngleFullElement(Element, MISB_0601):
  name = "platformPitchAngleFull"
  names = {"platformPitchAngleFull", "PlatformPitchAngleFull", "platformpitchangleFull",
           "pitchAngleFull", "PitchAngleFull", "pitchanglefull", "Pitch Angle Full", 
           "pitch angle full", "pitch", "Pitch"}

  misb_name = "Platform Pitch Angle (Full)"
  misb_key = "06 0E 2B 34 01 01 01 07 07 01 10 01 05 00 00 00"
  misb_tag = 90
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0x80000000 = "Out of Range"
    # -90 to 90
    # -((2^31)-1) to (2^31)-1
    # int().from_bytes
    # lerp

class PlatformRollAngleElement(Element, MISB_0601):
  name = "platformRollAngleShort"
  names = {"platformRollAngleShort", "PlatformRollAngleShort", "platformrollangleshort",
           "rollAngleShort", "RollAngleShort", "rollangleshort", "Roll Angle Short",
           "roll angle short", "roll short", "Roll Short"}

  misb_name = "Platform Roll Angle"
  misb_key = "06 0E 2B 34 01 01 01 07 07 01 10 01 04 00 00 00"
  misb_tag = 7
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0x8000= "Out of Range"
    # -50 to 50
    # -((2^15)-1) to (2^15)-1
    # int().from_bytes
    # lerp

class PlatformRollAngleFullElement(Element, MISB_0601):
  name = "platformRollAngleFull"
  names = {"platformRollAngleFull", "PlatformRollAngleFull", "platformrollanglefull",
           "rollAngleFull", "RollAngleFull", "rollanglefull", "Roll Angle Full",
           "roll angle full", "roll full", "Roll Full", "roll", "Roll"}

  misb_name = "Platform Roll Angle (Full)"
  misb_key = "06 0E 2B 34 01 01 01 07 07 01 10 01 04 00 00 00"
  misb_tag = 91
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0x80000000 = "Out of Range"
    # -90 to 90
    # -((2^31)-1) to (2^31)-1
    # int().from_bytes
    # lerp

class PlatformDesignationElement(Element, MISB_0601):
  name = "platformDesignation"
  names = {"platformDesignation", "PlatformDesignation", "platformdesignation",
           "Platform Designation", "platform designation", "platform", "model"}

  misb_name = "Platform Designation"
  misb_key = "06 0E 2B 34 01 01 01 01 01 01 20 01 00 00 00 00"
  misb_tag = 10
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # bytes_to_str()

class ImageSourceSensorElement(Element, MISB_0601):
  name = "imageSourceSensor"
  names = {"imageSourceSensor", "ImageSourceSensor", "imagesourcesensor",
           "Image Source Sensor", "image source sensor", "Image Source", 
           "image source", "Source Sensor", "source sensor"}

  misb_name = "Image Source Sensor"
  misb_key = "06 0E 2B 34 01 01 01 01 04 20 01 02 01 01 00 00"
  misb_tag = 11
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # bytes_to_str()

class ImageCoordinateSystemElement(Element, MISB_0601):
  name = "imageCoordinateSystem"
  names = {"imageCoordinateSystem", "ImageCoordinateSystem", "imagecoordinateSystem",
           "Image Coordinate System", "image coordinate system", "Coordinate System",
           "coordinate system"}

  misb_name = "Image Coordinate System"
  misb_key = "06 0E 2B 34 01 01 01 01 07 01 01 01 00 00 00 00"
  misb_tag = 12
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # bytes_to_str()

class LatitudeElement(Element, MISB_0601):
  name = "latitude"
  names = {"Latitude", "latitude", "sensorLatitude", "SensorLatitude", "sensorlatitude",
           "Sensor Latitude", "sensor latitude", "Lat", "lat", "LATITUDE", "LAT"}

  misb_name = "Sensor Latitude"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 02 04 02 00"
  misb_tag = 13
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # 0x80000000 = "Reserved"
    # -90 to 90
    # -((2^31)-1) to (2^31)-1
    # int.from_bytes()
    # linear map

class LongitudeElement(Element, MISB_0601):
  name = "longitude"
  names = {"Longitude", "longitude", "sensorLongitude", "SensorLongitude",
           "sensorlongitude", "Sensor Longitude", "sensor longitude", "Long", "long",
           "LONG", "Lon", "lon", "LON", "longtitude"} #DJI can't spell

  misb_name = "Sensor Longitude"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 02 06 02 00"
  misb_tag = 14
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # 0x80000000 = "Reserved"
    # -180 to 180
    # -((2^31)-1) to (2^31)-1
    # int.from_bytes()
    # linear map

class AltitudeElement(Element, MISB_0601):
  name = "altitude"
  names = {"Altitude", "altitude", "sensorTrueAltitude", "SensorTrueAltitude",
           "sensortruealtitude", "Sensor True Altitude", "sensor true altitude",
           "ALT", "Alt", "alt", "Altitude (m)", "ele"}

  misb_name = "Sensor True Altitude"
  misb_key = "06 0E 2B 34 01 01 01 01 07 01 02 01 02 02 00 00"
  misb_tag = 15
  misb_units = "Meters"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # -900 to 19000
    # 0 to (2^16)-1
    # int.from_bytes()
    # linear map

class SensorEllipsoidHeightElement(Element, MISB_0601):
  name = "sensorEllipsoidHeight"
  names = {"sensorEllipsoidHeight", "SensorEllipsoidHeight", "sensorellipsoidheight",
           "Sensor Ellipsoid Height", "sensor ellipsoid heigt"}

  misb_name = "Sensor Ellipsoid Height"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 02 01 82 47 00 00"
  misb_tag = 75
  misb_units = "Meters"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # -900 to 19000
    # 0 to (2^16)-1
    # int.from_bytes()
    # lerp

class SensorEllipsoidHeightExtendedElement(Element):
  name = "sensorEllipsoidHeightExtended"
  names = {"sensorEllipsoidHeightExtended", "SensorEllipsoidHeightExtended",
           "sensorellipsoidheightextended", "Sensor Ellipsoid Height Extended",
           "sensor ellipsoid heigt extended"}

  def __init__(self, value: float):
    self.value = float(value)

class SensorHorizontalFOVElement(Element, MISB_0601):
  name = "sensorHorizontalFOV"
  names = {"sensorHorizontalFOV", "SensorHorizontalFOV", "sensorhorizontalfov",
           "Sensor Horizontal FOV", "sensor horizontal FOV", "sensor horizontal fov",
           "Horizontal FOV", "horizontal FOV", "horizontal fov", "Horizontal FOV (deg)",
           "sensorHorizontalFov"}

  misb_name = "Sensor Horizontal Field of View"
  misb_key = "06 0E 2B 34 01 01 01 02 04 20 02 01 01 08 00 00"
  misb_tag = 16
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # 0 to 180
    # 0 to (2^16)-1
    # int.from_bytes()
    # linear map

class SensorVerticalFOVElement(Element, MISB_0601):
  name = "sensorVerticalFOV"
  names = {"sensorVerticalFOV", "SensorVerticalFOV", "sensorverticalfov",
           "Sensor Vertical FOV", "sensor vertical FOV", "sensor vertical fov",
           "Vertical FOV", "vertical FOV", "vertical fov", "Vertical FOV (deg)",
           "sensorVerticalFov"}

  misb_name = "Sensor Vertical Field of View"
  misb_key = "06 0E 2B 34 01 01 01 07 04 20 02 01 01 0A 01 00"
  misb_tag = 17
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # 0 to 180
    # 0 to (2^16)-1
    # int.from_bytes()
    # linear map

class SensorRelativeAzimuthAngleElement(Element, MISB_0601):
  name = "sensorRelativeAzimuthAngle"
  names = {"sensorRelativeAzimuthAngle", "SensorRelativeAzimuthAngle",
           "sensorrelaztiveazimuthangle", "Sensor Relative Azimuth Angle",
           "sensor relative azimuth angle", "azimuthAngle", "AzimuthAngle",
           "azimuthangle", "Azimuth Angle", "azimuth angle", "Pan", "pan", "Pan (deg)"}

  misb_name = "Sensor Relative Azimuth Angle"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 02 04 00 00 00"
  misb_tag = 18
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # 0 to 360
    # 0 to (2^32)-1
    # int.from_bytes()
    # linear map

class SensorRelativeElevationAngleElement(Element, MISB_0601):
  name = "sensorRelativeElevationAngle"
  names = {"sensorRelativeElevationAngle", "SensorRelativeElevationAngle",
           "sensorrelativeelevationangle", "Sensor Relative Elevation Angle",
           "sensor relative elevation angle", "Tilt", "tilt", "Tilt (deg)"}

  misb_name = "Sensor Relative Elevation Angle"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 02 05 00 00 00"
  misb_tag = 19
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # 0x80000000 = "Reserved"
    # -180 to 180
    # -((2^31)-1) to (2^31)-1
    # int.from_bytes()
    # linear map

class SensorRelativeRollAngleElement(Element, MISB_0601):
  name = "sensorRelativeRollAngle"
  names = {"sensorRelativeRollAngle", "SensorRelativeRollAngle",
           "sensorrelativerollangle", "Sensor Relative Roll Angle",
           "sensor relative roll angle", "Roll", "roll", "Roll (deg)"}

  misb_name = "Sensor Relative Roll Angle"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 02 06 00 00 00"
  misb_tag = 20
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # 0 to 360
    # 0 to (2^32)-1
    # int.from_bytes()
    # linear map

class SlantRangeElement(Element, MISB_0601):
  name = "slantRange"
  names = {"slantRange", "SlantRange", "slantrange", "Slant Range", "slant range",
           "Slant Range (m)"}

  misb_name = "Slant Range"
  misb_key = "06 0E 2B 34 01 01 01 01 07 01 08 01 01 00 00 00"
  misb_tag = 21
  misb_units = "Meters"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # 0 to 5000000
    # 0 to (2^32)-1
    # int.from_bytes()
    # linear map

class TargetWidthElement(Element, MISB_0601):
  name = "targetWidth"
  names = {"targetWidth", "TargetWidth", "targetwidth", "Target Width", "target width",
           "Horizontal Span (m)"}

  misb_name = "Target Width"
  misb_key = "06 0E 2B 34 01 01 01 01 07 01 09 02 01 00 00 00"
  misb_tag = 22
  misb_units = "Meters"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # 0 to 10000
    # 0 to (2^16)-1
    # int.from_bytes()
    # linear map

class TargetWidthExtendedElement(Element):
  name = "targetWidthExtended"
  names = {"targetWidthExtended", "TargetWidthExtended", "targetwidthextended",
           "Target Width Extended", "target width extended"}

  def __init__(self, value: float):
    self.value = float(value)

class FrameCenterLatitudeElement(Element, MISB_0601):
  name = "frameCenterLatitude"
  names = {"frameCenterLatitude", "FrameCenterLatitude", "framecenterlatitude",
           "Frame Center Latitude", "frame center latitude", "Center Latitude",
           "center latitude"}

  misb_name = "Frame Center Latitude "
  misb_key = "06 0E 2B 34 01 01 01 01 07 01 02 01 03 02 00 00"
  misb_tag = 23
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # 0x80000000 = "N/A (Off-Earth)"
    # -90 to 90
    # -((2^31)-1) to (2^31)-1
    # int.from_bytes()
    # linear map

class FrameCenterLongitudeElement(Element, MISB_0601):
  name = "frameCenterLongitude"
  names = {"frameCenterLongitude", "FrameCenterLongitude", "framecenterlongitude",
           "Frame Center Longitude", "frame center longitude", "Center Longitude",
           "center longitude"}

  misb_name = "Frame Center Longitude "
  misb_key = "06 0E 2B 34 01 01 01 01 07 01 02 01 03 04 00 00"
  misb_tag = 24
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # 0x80000000 = "N/A (Off-Earth)"
    # -180 to 180
    # -((2^31)-1) to (2^31)-1
    # int.from_bytes()
    # linear map

class FrameCenterElevationElement(Element, MISB_0601):
  name = "frameCenterAltitude"
  names = {"frameCenterAltitude", "FrameCenterAltitude", "framecenteraltitude",
           "Frame Center Altitude", "frame center altitude", "Center Altitude",
           "center altitude", "Center Altitude (m)", "frameCenterElevation",
           "FrameCenterElevation", "framecenterelevation"}

  misb_name = "Frame Center Elevation "
  misb_key = "06 0E 2B 34 01 01 01 0A 07 01 02 01 03 16 00 00"
  misb_tag = 25
  misb_units = "Meters"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # -900 to 19000
    # 0 to (2^16)-1
    # int.from_bytes()
    # linear map

class FrameCenterHeightAboveEllipsoidElement(Element, MISB_0601):
  name = "frameCenterHeightAboveEllipsoid"
  names = {"frameCenterHeightAboveEllipsoid", "FrameCenterHeightAboveEllipsoid",
           "framecenterheightaboveellipsoid", "Frame Center Height Above Ellipsoid",
           "frame center height above ellipsoid"}

  misb_name = "Frame Center Height Above Ellipsoid"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 02 03 48 00 00 00"
  misb_tag = 78
  misb_units = "Meters"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # -900 to 19000
    # 0 to (2^16)-1
    # int.from_bytes()
    # linear map

class UASLocalSetVersionElement(Element, MISB_0601):
  name = "UASLocalSetVersion"
  names = {"UASLocalSetVersion", "uaslocalsetversion", "UAS Local Set Version",
           "uas local set version", "uasLocalSetVersion"}

  misb_name = "UAS Datalink LS Version Number"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 02 03 03 00 00 00"
  misb_tag = 65
  misb_units = "None"

  def __init__(self, value: int):
    self.value = int(value)

  @classmethod
  def fromMISB(cls, value: str) -> Element:
    pass
    # 0 to 255
    # 0 to 255
    # int.from_bytes()

# class MotionImageryCoreIdentifierElement(Element):
#   #This is a KVL/MISB specific element
#   #This doesn't seem to be correctly implemented anywhere so just going to leave
#   #it commented out until further notice
#   name = "motionImageryCoreIdentifier"
#   names = {"motionImageryCoreIdentifier"}

#   def __init__(self, value: float):
#     self.value = value
  
class SensorWGS84AltitudeElement(Element):
  name = "sensorWGS84Altitude"
  names = {"sensorWGS84Altitude", "SensorWGS84Altitude", "sensorWGS84altitude",
           "sensortwgs64altitude"}

  def __init__(self, value: float):
    self.value = float(value)

class SensorGroundAltitudeElement(Element):
  name = "sensorGroundAltitude"
  names = {"sensorGroundAltitude", "SensorGroundAltitude", "sensorgroundaltitude",
           "Sensor Ground Altitude", "sensor ground altitude"}

  def __init__(self, value: float):
    self.value = float(value)

class SensorLaunchAltitudeElement(Element):
  name = "sensorLaunchAltitude"
  names = {"sensorLaunchAltitude", "SensorLaunchAltitude", "sensorlaunchaltitude",
           "Sensor Launch Altitude", "sensor launch altitude"}

  def __init__(self, value: float):
    self.value = float(value)

class TimeframeBeginElement(Element):
  name = "timeframeBegin"
  names = {"timeframeBegin", "TimeframeBegin", "timeframebegin", "Timeframe Begin",
           "timeframe begin"}

  def __init__(self, value: float):
    self.value = float(value)

class TimeframeEndElement(Element):
  name = "timeframeEnd"
  names = {"timeframeEnd", "TimeframeEnd", "timeframeend", "Timeframe End",
           "timeframe end"}

  def __init__(self, value: float):
    self.value = float(value)

class SpeedElement(Element, MISB_0601):
  name = "speed"
  names = {"speed", "Speed", "velocity", "Velocity", "badelf:speed"}

  misb_name = "Platform True Airspeed"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 0A 00 00 00"
  misb_tag = 8
  misb_units = "Meters/Second"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0 to 255
    # 0 to 255
    # self.value = int.from_bytes(value)
  
class PlatformTailNumberElement(Element, MISB_0601):
  name = "platformTailNumber"
  names = {"platformTailNumber"}

  misb_name = "Platform Tail Number"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 04 01 02 00 00 00"
  misb_tag = 4
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # self.value = bytes_to_str(value)
  
class PlatformIndicatedAirspeedElement(Element, MISB_0601):
  name = "platformIndicatedAirspeed"
  names = {"platformIndicatedAirspeed"}

  misb_name = "Platform Indicated Airspeed"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 0B 00 00 00"
  misb_tag = 9
  misb_units = "Meters/Second"

  def __init__(self, value: int):
    self.value = int(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0 to 255
    # 0 to 255
    # int.from_bytes()
  
class OffsetCornerLatitudePoint1Element(Element, MISB_0601):
  name = "offsetCornerLatitude"
  names = {"offsetCornerLatitude"}

  misb_name = "Offset Corner Latitude Point 1"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 07 01 00"
  misb_tag = 26
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0x8000 means "N/A (Off-Earth)"
    # -0.075 to 0.075
    # -((2^15)-1) to (2^15)-1
    # int.from_bytes()
    # lerp
    # + FrameCenterLat (Tag 23)

class OffsetCornerLatitudePoint2Element(Element, MISB_0601):
  name = "offsetCornerLatitude2"
  names = {"offsetCornerLatitude2"}

  misb_name = "Offset Corner Latitude Point 2"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 08 01 00"
  misb_tag = 28
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0x8000 means "N/A (Off-Earth)"
    # -0.075 to 0.075
    # -((2^15)-1) to (2^15)-1
    # int.from_bytes()
    # lerp
    # + FrameCenterLat (Tag 23)

class OffsetCornerLatitudePoint3Element(Element, MISB_0601):
  name = "offsetCornerLatitude3"
  names = {"offsetCornerLatitude3"}

  misb_name = "Offset Corner Latitude Point 3"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 09 01 00"
  misb_tag = 30
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0x8000 means "N/A (Off-Earth)"
    # -0.075 to 0.075
    # -((2^15)-1) to (2^15)-1
    # int.from_bytes()
    # lerp
    # + FrameCenterLat (Tag 23)

class OffsetCornerLatitudePoint4Element(Element, MISB_0601):
  name = "offsetCornerLatitude4"
  names = {"offsetCornerLatitude4"}

  misb_name = "Offset Corner Latitude Point 4"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0A 01 00"
  misb_tag = 32
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0x8000 means "N/A (Off-Earth)"
    # -0.075 to 0.075
    # -((2^15)-1) to (2^15)-1
    # int.from_bytes()
    # lerp
    # + FrameCenterLat (Tag 23)

class OffsetCornerLongitudePoint1Element(Element, MISB_0601):
  name = "offsetCornerLongitude"
  names = {"offsetCornerLongitude"}

  misb_name = "Offset Corner Longitude Point 1"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0B 01 00"
  misb_tag = 27
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0x8000 means "N/A (Off-Earth)"
    # -0.075 to 0.075
    # -((2^15)-1) to (2^15)-1
    # int.from_bytes()
    # lerp
    # + FrameCenterLong (Tag 24)

class OffsetCornerLongitudePoint2Element(Element, MISB_0601):
  name = "offsetCornerLongitude2"
  names = {"offsetCornerLongitude2"}

  misb_name = "Offset Corner Longitude Point 2"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0C 01 00"
  misb_tag = 29
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0x8000 means "N/A (Off-Earth)"
    # -0.075 to 0.075
    # -((2^15)-1) to (2^15)-1
    # int.from_bytes()
    # lerp
    # + FrameCenterLong (Tag 24)

class OffsetCornerLongitudePoint3Element(Element, MISB_0601):
  name = "offsetCornerLongitude3"
  names = {"offsetCornerLongitude3"}

  misb_name = "Offset Corner Longitude Point 3"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0D 01 00"
  misb_tag = 31
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0x8000 means "N/A (Off-Earth)"
    # -0.075 to 0.075
    # -((2^15)-1) to (2^15)-1
    # int.from_bytes()
    # lerp
    # + FrameCenterLong (Tag 24)

class OffsetCornerLongitudePoint4Element(Element, MISB_0601):
  name = "offsetCornerLongitude4"
  names = {"offsetCornerLongitude4"}

  misb_name = "Offset Corner Longitude Point 4"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0E 01 00"
  misb_tag = 33
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0x8000 means "N/A (Off-Earth)"
    # -0.075 to 0.075
    # -((2^15)-1) to (2^15)-1
    # int.from_bytes()
    # lerp
    # + FrameCenterLong (Tag 24)

class IcingDetectedElement(Element, MISB_0601):
  name = "icingDetected"
  names = {"icingDetected"}

  misb_name = "Icing Detected"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 0C 00 00 00"
  misb_tag = 34
  misb_units = "Icing Code"

  _code = {0 : "Detector off",
          1 : "No icing detected",
          2 : "Icing detected"}

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0 to 2
    # 0 to 2
    # int.from_bytes()
    # code dict

class WindDirectionElement(Element, MISB_0601):
  name = "windDirection"
  names = {"windDirection"}

  misb_name = "Wind Direction"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 0D 00 00 00"
  misb_tag = 35
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0 to 360
    # 0 to (2^16)-1
    # int.from_bytes()
    # lerp

class WindSpeedElement(Element, MISB_0601):
  name = "windSpeed"
  names = {"windSpeed"}

  misb_name = "Wind Speed"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 0E 00 00 00"
  misb_tag = 36
  misb_units = "Meters/Second"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0 to 100
    # 0 to 255
    # int.from_bytes()
    # lerp

class StaticPressureElement(Element, MISB_0601):
  name = "staticPressure"
  names = {"staticPressure"}

  misb_name = "Static Pressure"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 0F 00 00 00"
  misb_tag = 37
  misb_units = "Millibar"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0 to 5000
    # 0 to (2^16)-1
    # int.from_bytes()
    # lerp

class DensityAltitudeElement(Element, MISB_0601):
  name = "densityAltitude"
  names = {"densityAltitude"}

  misb_name = "Density Altitude"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 10 00 00 00"
  misb_tag = 38
  misb_units = "Meters"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # -900 to 19000
    # 0 to (2^16)-1
    # int.from_bytes()
    # lerp

class OutsideAirTemperatureElement(Element, MISB_0601):
  name = "outsideAirTemperature"
  names = {"outsideAirTemperature"}

  misb_name = "Outside Air Temperature"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 11 00 00 00"
  misb_tag = 39
  misb_units = "Celsius"

  def __init__(self, value: int):
    self.value = int(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # -128 to 127
    # -128 to 127
    # int.from_bytes()

class TargetLocationLatitudeElement(Element, MISB_0601):
  name = "targetLocationLatitude"
  names = {"targetLocationLatitude"}

  misb_name = "Target Location Latitude"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 03 02 00 00 00"
  misb_tag = 40
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0x80000000 =  "N/A (Off-Earth)" 
    # -90 to 90
    # -((2^31)-1) to (2^31)-1
    # int.from_bytes()
    # lerp

class TargetLocationLongitudeElement(Element, MISB_0601):
  name = "targetLocationLongitude"
  names = {"targetLocationLongitude"}

  misb_name = "Target Location Longitude"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 03 03 00 00 00"
  misb_tag = 41
  misb_units = "Degrees"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0x80000000 =  "N/A (Off-Earth)" 
    # -180 to 180
    # -((2^31)-1) to (2^31)-1
    # int.from_bytes()
    # lerp

class TargetLocationElevationElement(Element, MISB_0601):
  name = "targetLocationElevation"
  names = {"targetLocationElevation"}

  misb_name = "Target Location Elevation"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 03 04 00 00 00"
  misb_tag = 42
  misb_units = "Meters"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # -900 to 190000
    # 0 to (2^32)-1
    # int.from_bytes()
    # lerp

class TargetTrackGateWidthElement(Element, MISB_0601):
  name = "targetTrackGateWidth"
  names = {"targetTrackGateWidth"}

  misb_name = "Target Track Gate Width"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 03 05 00 00 00"
  misb_tag = 43
  misb_units = "Pixels"

  def __init__(self, value: int):
    self.value = int(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0 to 510
    # 0 to 255
    # int.from_bytes() * 2

class TargetTrackGateHeightElement(Element, MISB_0601):
  name = "targetTrackGateHeight"
  names = {"targetTrackGateHeight"}

  misb_name = "Target Track Gate Height"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 03 06 00 00 00"
  misb_tag = 44
  misb_units = "Pixels"

  def __init__(self, value: int):
    self.value = int(value)

  @classmethod
  def fromMISB(cls, value: str):
    pass
    # 0 to 510
    # 0 to 255
    # int.from_bytes() * 2

class UnknownElement(Element):
  name = "unknown"
  names = {}

  def __init__(self, value: str):
    self.value = str(value)

