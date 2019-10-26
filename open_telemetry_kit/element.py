#!/usr/bin/env python3

import logging
from abc import abstractmethod
from datetime import datetime
from dateutil import parser as dup
from typing import Any, Set

class Element():
  def __init__(self, value: Any):
    self.value = value

  def __str__(self):
    # return '{}'.format(self.value)
    return self.value

  def __repr__(self) -> str:
    return "{}('{}')".format(self.__class__.__name__, self.value)

  @property
  @classmethod
  @abstractmethod
  def name(self) -> str:
    pass

  @property
  @classmethod
  @abstractmethod
  def names(self) -> Set[str]:
    pass

  def toJson(self) -> Any:
    return self.value

class ChecksumElement(Element):
  name = "checksum"
  names = {"checksum", "Checksum"}

  def __init__(self, value: int):
    self.value = int(value)
  
class TimestampElement(Element):
  name = "timestamp"
  names = {"timestamp", "Timestamp", "time stamp", "Time Stamp"}

  def __init__(self, value: int):
    self.value = int(value)

class DatetimeElement(Element):
  name = "datetime"
  names = {"datetime", "Datetime", "DateTime", "time"}

  def __init__(self, value: datetime):
    self.value = dup.parse(value)

  def toJson(self) -> str:
    return str(self.value)

class MissionIDElement(Element):
  name = "missionID" 
  names = {"missionID", "MissionId", "Missionid", "missionID",
           "missionId", "missionid"}

  def __init__(self, value: str):
    self.value = value

class PlatformHeadingAngleElement(Element):
  name = "platformHeadingAngle"
  names = {"platformHeadingAngle", "PlatformHeadingAngle", "platformheadingangle",
           "headingAngle", "HeadingAngle", "headingangle", "Heading Angle",
           "heading angle", "heading", "Heading"}

  def __init__(self, value: float):
    self.value = float(value)

class PlatformPitchAngleElement(Element):
  name = "platformPitchAngle"
  names = {"platformPitchAngle", "PlatformPitchAngle", "platformpitchangle",
           "pitchAngle", "PitchAngle", "pitchangle", "Pitch Angle", "pitch angle",
           "pitch", "Pitch"}

  def __init__(self, value: float):
    self.value = float(value)

class PlatformRollAngleShortElement(Element):
  name = "platformRollAngleShort"
  names = {"platformRollAngleShort", "PlatformRollAngleShort", "platformrollangleshort",
           "rollAngleShort", "RollAngleShort", "rollangleshort", "Roll Angle Short",
           "roll angle short", "roll short", "Roll Short"}

  def __init__(self, value: float):
    self.value = float(value)

class PlatformRollAngleFullElement(Element):
  name = "platformRollAngleFull"
  names = {"platformRollAngleFull", "PlatformRollAngleFull", "platformrollanglefull",
           "rollAngleFull", "RollAngleFull", "rollanglefull", "Roll Angle Full",
           "roll angle full", "roll full", "Roll Full"}

  def __init__(self, value: float):
    self.value = float(value)

class PlatformDesignationElement(Element):
  name = "platformDesignation"
  names = {"platformDesignation", "PlatformDesignation", "platformdesignation",
           "Platform Designation", "platform designation", "platform", "model"}

  def __init__(self, value: str):
    self.value = value

class ImageSourceSensorElement(Element):
  name = "imageSourceSensor"
  names = {"imageSourceSensor", "ImageSourceSensor", "imagesourcesensor",
           "Image Source Sensor", "image source sensor", "Image Source", 
           "image source", "Source Sensor", "source sensor"}

  def __init__(self, value: str):
    self.value = value

class ImageCoordinateSystemElement(Element):
  name = "imageCoordinateSystem"
  names = {"imageCoordinateSystem", "ImageCoordinateSystem", "imagecoordinateSystem",
           "Image Coordinate System", "image coordinate system", "Coordinate System",
           "coordinate system"}

  def __init__(self, value: str):
    self.value = value

class LatitudeElement(Element):
  name = "latitude"
  names = {"Latitude", "latitude", "sensorLatitude", "SensorLatitude", "sensorlatitude",
           "Sensor Latitude", "sensor latitude", "Lat", "lat", "LATITUDE", "LAT"}

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromKML(cls, value: str) -> Element:
    return cls(float(value))

class LongitudeElement(Element):
  name = "longitude"
  names = {"Longitude", "longitude", "sensorLongitude", "SensorLongitude",
           "sensorlongitude", "Sensor Longitude", "sensor longitude", "Long", "long",
           "LONG", "Lon", "lon", "LON", "longtitude"} #DJI can't spell

  def __init__(self, value: float):
    self.value = float(value)

class AltitudeElement(Element):
  name = "altitude"
  names = {"Altitude", "altitude", "sensorTrueAltitude", "SensorTrueAltitude",
           "sensortruealtitude", "Sensor True Altitude", "sensor true altitude",
           "ALT", "Alt", "alt", "Altitude (m)", "ele"}

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromKML(cls, value: str) -> Element:
    return cls(float(value))

class SensorEllipsoidHeightElement(Element):
  name = "sensorEllipsoidHeight"
  names = {"sensorEllipsoidHeight", "SensorEllipsoidHeight", "sensorellipsoidheight",
           "Sensor Ellipsoid Height", "sensor ellipsoid heigt"}

  def __init__(self, value: float):
    self.value = float(value)

class SensorEllipsoidHeightExtendedElement(Element):
  name = "sensorEllipsoidHeightExtended"
  names = {"sensorEllipsoidHeightExtended", "SensorEllipsoidHeightExtended",
           "sensorellipsoidheightextended", "Sensor Ellipsoid Height Extended",
           "sensor ellipsoid heigt extended"}

  def __init__(self, value: float):
    self.value = float(value)

class SensorHorizontalFOVElement(Element):
  name = "sensorHorizontalFOV"
  names = {"sensorHorizontalFOV", "SensorHorizontalFOV", "sensorhorizontalfov",
           "Sensor Horizontal FOV", "sensor horizontal FOV", "sensor horizontal fov",
           "Horizontal FOV", "horizontal FOV", "horizontal fov", "Horizontal FOV (deg)"}

  def __init__(self, value: float):
    self.value = float(value)

class SensorVerticalFOVElement(Element):
  name = "sensorVerticalFOV"
  names = {"sensorVerticalFOV", "SensorVerticalFOV", "sensorverticalfov",
           "Sensor Vertical FOV", "sensor vertical FOV", "sensor vertical fov",
           "Vertical FOV", "vertical FOV", "vertical fov", "Vertical FOV (deg)"}

  def __init__(self, value: float):
    self.value = float(value)

class SensorRelativeAzimuthAngleElement(Element):
  name = "sensorRelativeAzimuthAngle"
  names = {"sensorRelativeAzimuthAngle", "SensorRelativeAzimuthAngle",
           "sensorrelaztiveazimuthangle", "Sensor Relative Azimuth Angle",
           "sensor relative azimuth angle", "azimuthAngle", "AzimuthAngle",
           "azimuthangle", "Azimuth Angle", "azimuth angle", "Pan", "pan", "Pan (deg)"}

  def __init__(self, value: float):
    self.value = float(value)

class SensorRelativeElevationAngleElement(Element):
  name = "sensorRelativeElevationAngle"
  names = {"sensorRelativeElevationAngle", "SensorRelativeElevationAngle",
           "sensorrelativeelevationangle", "Sensor Relative Elevation Angle",
           "sensor relative elevation angle", "Tilt", "tilt", "Tilt (deg)"}

  def __init__(self, value: float):
    self.value = float(value)

class SensorRelativeRollAngleElement(Element):
  name = "sensorRelativeRollAngle"
  names = {"sensorRelativeRollAngle", "SensorRelativeRollAngle",
           "sensorrelativerollangle", "Sensor Relative Roll Angle",
           "sensor relative roll angle", "Roll", "roll", "Roll (deg)"}

  def __init__(self, value: float):
    self.value = float(value)

class SlantRangeElement(Element):
  name = "slantRange"
  names = {"slantRange", "SlantRange", "slantrange", "Slant Range", "slant range",
           "Slant Range (m)"}

  def __init__(self, value: float):
    self.value = float(value)

class TargetWidthElement(Element):
  name = "targetWidth"
  names = {"targetWidth", "TargetWidth", "targetwidth", "Target Width", "target width",
           "Horizontal Span (m)"}

  def __init__(self, value: float):
    self.value = float(value)

class TargetWidthExtendedElement(Element):
  name = "targetWidthExtended"
  names = {"targetWidthExtended", "TargetWidthExtended", "targetwidthextended",
           "Target Width Extended", "target width extended"}

  def __init__(self, value: float):
    self.value = float(value)

class FrameCenterLatitudeElement(Element):
  name = "frameCenterLatitude"
  names = {"frameCenterLatitude", "FrameCenterLatitude", "framecenterlatitude",
           "Frame Center Latitude", "frame center latitude", "Center Latitude",
           "center latitude"}

  def __init__(self, value: float):
    self.value = float(value)

class FrameCenterLongitudeElement(Element):
  name = "frameCenterLongitude"
  names = {"frameCenterLongitude", "FrameCenterLongitude", "framecenterlongitude",
           "Frame Center Longitude", "frame center longitude", "Center Longitude",
           "center longitude"}

  def __init__(self, value: float):
    self.value = float(value)

class FrameCenterElevationElement(Element):
  name = "frameCenterAltitude"
  names = {"frameCenterAltitude", "FrameCenterAltitude", "framecenteraltitude",
           "Frame Center Altitude", "frame center altitude", "Center Altitude",
           "center altitude", "Center Altitude (m)"}

  def __init__(self, value: float):
    self.value = float(value)

class FrameCenterHeightAboveEllipsoidElement(Element):
  name = "frameCenterHeightAboveEllipsoid"
  names = {"frameCenterHeightAboveEllipsoid", "FrameCenterHeightAboveEllipsoid",
           "framecenterheightaboveellipsoid", "Frame Center Height Above Ellipsoid",
           "frame center height above ellipsoid"}

  def __init__(self, value: float):
    self.value = float(value)

class UASLocalSetVersionElement(Element):
  name = "UASLocalSetVersion"
  names = {"UASLocalSetVersion", "uaslocalsetversion", "UAS Local Set Version",
           "uas local set version"}

  def __init__(self, value: int):
    self.value = int(value)

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

class SpeedElement(Element):
  name = "speed"
  names = {"speed", "Speed", "velocity", "Velocity", "badelf:speed"}

  def __init__(self, value: float):
    self.value = float(value)

class UnknownElement(Element):
  name = "unknown"
  names = {}

  def __init__(self, value: str):
    self.value = value
