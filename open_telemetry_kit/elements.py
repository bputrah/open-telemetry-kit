from .element import Element
from .misb_0601 import MISB_0601, MISB_int, MISB_float, MISB_str 
from datetime import datetime
from dateutil import parser as dup
from .klv_common import bytes_to_int, bytes_to_float, bytes_to_str

class ChecksumElement(Element, MISB_int):
  name = "checksum"
  names = {"checksum", "Checksum"}

  misb_name = "Checksum"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 02 03 01 00 00 00"
  misb_tag = 1
  misb_units = "None"

  def __init__(self, value: int):
    self.value = int(value)

class TimestampElement(Element, MISB_int):
  name = "timestamp"
  names = {"timestamp", "Timestamp", "time stamp", "Time Stamp"}

  misb_name = "Precision Time Stamp"
  misb_key = "06 0E 2B 34 01 01 01 03 07 02 01 01 01 05 00 00"
  misb_tag = 2
  misb_units = "Microseconds"

  _state_code = {0 : "seconds",
                1 : "milliseconds",
                2 : "microseconds"}

  # Python returns a float value in seconds for timestamp so conform to that 
  def __init__(self, value: float):
    self.value = float(value)
    self.state = self._state_code[0]

  @classmethod
  def fromMISB(cls, value: bytes):
    # Initialize as 0 to avoid converting back and for between [micro]seconds
    ts = cls(0).to_microseconds()
    ts.value = bytes_to_int(value)
    return ts
  
  def to_seconds(self):
    if self.state == self._state_code[1]:
      self.value = self.value * 1e-3
      self.state = self._state_code[0]

    elif self.state == self._state_code[2]:
      self.value = self.value * 1e-6
      self.state = self._state_code[0]

    return self

  def to_milliseconds(self):
    if self.state == self._state_code[0]:
      self.value = self.value * 1e3
      self.state = self._state_code[1]

    elif self.state == self._state_code[2]:
      self.value = self.value * 1e-3
      self.state = self._state_code[1]

    return self

  def to_microseconds(self):
    if self.state == self._state_code[0]:
      self.value = int(self.value * 1e6)
      self.state = self._state_code[2]

    elif self.state == self._state_code[1]:
      self.value = int(self.value * 1e3)
      self.state = self._state_code[2]

    return self

class DatetimeElement(Element):
  name = "datetime"
  names = {"datetime", "Datetime", "DateTime", "time"}

  def __init__(self, value: datetime):
    self.value = dup.parse(value)

  def toJson(self) -> str:
    return str(self.value)

class MissionIDElement(Element, MISB_str):
  name = "missionID" 
  names = {"missionID", "MissionId", "Missionid", "missionID",
           "missionId", "missionid"}

  misb_name = "Mission ID"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 04 01 03 00 00 00"
  misb_tag = 3
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

class PlatformHeadingAngleElement(Element, MISB_float):
  name = "platformHeadingAngle"
  names = {"platformHeadingAngle", "PlatformHeadingAngle", "platformheadingangle",
           "headingAngle", "HeadingAngle", "headingangle", "Heading Angle",
           "heading angle", "heading", "Heading"}

  misb_name = "Platform Heading Angle"
  misb_key = "06 0E 2B 34 01 01 01 07 07 01 10 01 06 00 00 00"
  misb_tag = 5
  misb_units = "Degrees"
  _domain = (0, 2**16 - 1)
  _range = (0, 360)

  def __init__(self, value: float):
    self.value = float(value)

class PlatformPitchAngleElement(Element, MISB_float):
  name = "platformPitchAngleShort"
  names = {"platformPitchAngleShort", "PlatformPitchAngleShort", "platformpitchangleshort",
           "pitchAngleShort", "PitchAngleShort", "pitchangleshort", "Pitch Angle Short", 
           "pitch angle short"}

  misb_name = "Platform Pitch Angle"
  misb_key = "06 0E 2B 34 01 01 01 07 07 01 10 01 05 00 00 00"
  misb_tag = 6
  misb_units = "Degrees"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-20, 20)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class PlatformPitchAngleFullElement(Element, MISB_float):
  name = "platformPitchAngleFull"
  names = {"platformPitchAngleFull", "PlatformPitchAngleFull", "platformpitchangleFull",
           "pitchAngleFull", "PitchAngleFull", "pitchanglefull", "Pitch Angle Full", 
           "pitch angle full", "pitch", "Pitch"}

  misb_name = "Platform Pitch Angle (Full)"
  misb_key = "06 0E 2B 34 01 01 01 07 07 01 10 01 05 00 00 00"
  misb_tag = 90
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-90, 90)
  _invalid = bytes.fromhex('80000000')

  def __init__(self, value: float):
    self.value = float(value)

class PlatformRollAngleElement(Element, MISB_float):
  name = "platformRollAngleShort"
  names = {"platformRollAngleShort", "PlatformRollAngleShort", "platformrollangleshort",
           "rollAngleShort", "RollAngleShort", "rollangleshort", "Roll Angle Short",
           "roll angle short", "roll short", "Roll Short"}

  misb_name = "Platform Roll Angle"
  misb_key = "06 0E 2B 34 01 01 01 07 07 01 10 01 04 00 00 00"
  misb_tag = 7
  misb_units = "Degrees"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-50, 50)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class PlatformRollAngleFullElement(Element, MISB_float):
  name = "platformRollAngleFull"
  names = {"platformRollAngleFull", "PlatformRollAngleFull", "platformrollanglefull",
           "rollAngleFull", "RollAngleFull", "rollanglefull", "Roll Angle Full",
           "roll angle full", "roll full", "Roll Full", "roll", "Roll"}

  misb_name = "Platform Roll Angle (Full)"
  misb_key = "06 0E 2B 34 01 01 01 07 07 01 10 01 04 00 00 00"
  misb_tag = 91
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-90, 90)
  _invalid = bytes.fromhex('80000000')

  def __init__(self, value: float):
    self.value = float(value)

class PlatformDesignationElement(Element, MISB_str):
  name = "platformDesignation"
  names = {"platformDesignation", "PlatformDesignation", "platformdesignation",
           "Platform Designation", "platform designation", "platform", "model"}

  misb_name = "Platform Designation"
  misb_key = "06 0E 2B 34 01 01 01 01 01 01 20 01 00 00 00 00"
  misb_tag = 10
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

class ImageSourceSensorElement(Element, MISB_str):
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

class ImageCoordinateSystemElement(Element, MISB_str):
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

class LatitudeElement(Element, MISB_float):
  name = "latitude"
  names = {"Latitude", "latitude", "sensorLatitude", "SensorLatitude", "sensorlatitude",
           "Sensor Latitude", "sensor latitude", "Lat", "lat", "LATITUDE", "LAT"}

  misb_name = "Sensor Latitude"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 02 04 02 00"
  misb_tag = 13
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-90, 90)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class LongitudeElement(Element, MISB_float):
  name = "longitude"
  names = {"Longitude", "longitude", "sensorLongitude", "SensorLongitude",
           "sensorlongitude", "Sensor Longitude", "sensor longitude", "Long", "long",
           "LONG", "Lon", "lon", "LON", "longtitude"} #DJI can't spell

  misb_name = "Sensor Longitude"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 02 06 02 00"
  misb_tag = 14
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-180, 180)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class AltitudeElement(Element, MISB_float):
  name = "altitude"
  names = {"Altitude", "altitude", "sensorTrueAltitude", "SensorTrueAltitude",
           "sensortruealtitude", "Sensor True Altitude", "sensor true altitude",
           "ALT", "Alt", "alt", "Altitude (m)", "ele"}

  misb_name = "Sensor True Altitude"
  misb_key = "06 0E 2B 34 01 01 01 01 07 01 02 01 02 02 00 00"
  misb_tag = 15
  misb_units = "Meters"
  _domain = (0, 2**16 - 1)
  _range = (-900, 19000)

  def __init__(self, value: float):
    self.value = float(value)

class SensorEllipsoidHeightElement(Element, MISB_float):
  name = "sensorEllipsoidHeight"
  names = {"sensorEllipsoidHeight", "SensorEllipsoidHeight", "sensorellipsoidheight",
           "Sensor Ellipsoid Height", "sensor ellipsoid height"}

  misb_name = "Sensor Ellipsoid Height"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 02 01 82 47 00 00"
  misb_tag = 75
  misb_units = "Meters"
  _domain = (0, 2**16 - 1)
  _range = (-900, 19000)

  def __init__(self, value: float):
    self.value = float(value)

class SensorEllipsoidHeightExtendedElement(Element, MISB_float):
  name = "sensorEllipsoidHeightExtended"
  names = {"sensorEllipsoidHeightExtended", "SensorEllipsoidHeightExtended",
           "sensorellipsoidheightextended", "Sensor Ellipsoid Height Extended",
           "sensor ellipsoid heigt extended"}

  misb_name = "Sensor Ellipsoid Height Extended"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 02 01 82 47 00 00"
  misb_tag = 104
  misb_units = "Meters"
  #TODO
  # IMAPB ??? based on length?
  _domain = (0, 2**16 - 1)
  _range = (-900, 40000)

  def __init__(self, value: float):
    self.value = float(value)

class SensorHorizontalFOVElement(Element, MISB_float):
  name = "sensorHorizontalFOV"
  names = {"sensorHorizontalFOV", "SensorHorizontalFOV", "sensorhorizontalfov",
           "Sensor Horizontal FOV", "sensor horizontal FOV", "sensor horizontal fov",
           "Horizontal FOV", "horizontal FOV", "horizontal fov", "Horizontal FOV (deg)",
           "sensorHorizontalFov"}

  misb_name = "Sensor Horizontal Field of View"
  misb_key = "06 0E 2B 34 01 01 01 02 04 20 02 01 01 08 00 00"
  misb_tag = 16
  misb_units = "Degrees"
  _domain = (0, 2**16 - 1)
  _range = (0, 180)

  def __init__(self, value: float):
    self.value = float(value)

class SensorVerticalFOVElement(Element, MISB_float):
  name = "sensorVerticalFOV"
  names = {"sensorVerticalFOV", "SensorVerticalFOV", "sensorverticalfov",
           "Sensor Vertical FOV", "sensor vertical FOV", "sensor vertical fov",
           "Vertical FOV", "vertical FOV", "vertical fov", "Vertical FOV (deg)",
           "sensorVerticalFov"}

  misb_name = "Sensor Vertical Field of View"
  misb_key = "06 0E 2B 34 01 01 01 07 04 20 02 01 01 0A 01 00"
  misb_tag = 17
  misb_units = "Degrees"
  _domain = (0, 2**16 - 1)
  _range = (0, 180)

  def __init__(self, value: float):
    self.value = float(value)

class SensorRelativeAzimuthAngleElement(Element, MISB_float):
  name = "sensorRelativeAzimuthAngle"
  names = {"sensorRelativeAzimuthAngle", "SensorRelativeAzimuthAngle",
           "sensorrelaztiveazimuthangle", "Sensor Relative Azimuth Angle",
           "sensor relative azimuth angle", "azimuthAngle", "AzimuthAngle",
           "azimuthangle", "Azimuth Angle", "azimuth angle", "Pan", "pan", "Pan (deg)"}

  misb_name = "Sensor Relative Azimuth Angle"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 02 04 00 00 00"
  misb_tag = 18
  misb_units = "Degrees"
  _domain = (0, 2**32 - 1)
  _range = (0, 360)

  def __init__(self, value: float):
    self.value = float(value)

class SensorRelativeElevationAngleElement(Element, MISB_float):
  name = "sensorRelativeElevationAngle"
  names = {"sensorRelativeElevationAngle", "SensorRelativeElevationAngle",
           "sensorrelativeelevationangle", "Sensor Relative Elevation Angle",
           "sensor relative elevation angle", "Tilt", "tilt", "Tilt (deg)"}

  misb_name = "Sensor Relative Elevation Angle"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 02 05 00 00 00"
  misb_tag = 19
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-180, 180)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class SensorRelativeRollAngleElement(Element, MISB_float):
  name = "sensorRelativeRollAngle"
  names = {"sensorRelativeRollAngle", "SensorRelativeRollAngle",
           "sensorrelativerollangle", "Sensor Relative Roll Angle",
           "sensor relative roll angle", "Roll", "roll", "Roll (deg)"}

  misb_name = "Sensor Relative Roll Angle"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 02 06 00 00 00"
  misb_tag = 20
  misb_units = "Degrees"
  _domain = (0, 2**32 - 1)
  _range = (0, 360)

  def __init__(self, value: float):
    self.value = float(value)

class SlantRangeElement(Element, MISB_float):
  name = "slantRange"
  names = {"slantRange", "SlantRange", "slantrange", "Slant Range", "slant range",
           "Slant Range (m)"}

  misb_name = "Slant Range"
  misb_key = "06 0E 2B 34 01 01 01 01 07 01 08 01 01 00 00 00"
  misb_tag = 21
  misb_units = "Meters"
  _domain = (0, 2**32 - 1)
  _range = (0, 5000000)

  def __init__(self, value: float):
    self.value = float(value)

class TargetWidthElement(Element, MISB_float):
  name = "targetWidth"
  names = {"targetWidth", "TargetWidth", "targetwidth", "Target Width", "target width",
           "Horizontal Span (m)"}

  misb_name = "Target Width"
  misb_key = "06 0E 2B 34 01 01 01 01 07 01 09 02 01 00 00 00"
  misb_tag = 22
  misb_units = "Meters"
  _domain = (0, 2**16 - 1)
  _range = (0, 10000)

  def __init__(self, value: float):
    self.value = float(value)

class TargetWidthExtendedElement(Element, MISB_float):
  name = "targetWidthExtended"
  names = {"targetWidthExtended", "TargetWidthExtended", "targetwidthextended",
           "Target Width Extended", "target width extended"}

  misb_name = "Target Width Extended"
  misb_key = "06 0E 2B 34 01 01 01 01 07 01 09 02 01 00 00 00"
  misb_tag = 96
  misb_units = "Meters"
  # TODO
  # IMAPB ?????
  _domain = (0, 2**16 - 1)
  _range = (0, 1500000)

  def __init__(self, value: float):
    self.value = float(value)

class FrameCenterLatitudeElement(Element, MISB_float):
  name = "frameCenterLatitude"
  names = {"frameCenterLatitude", "FrameCenterLatitude", "framecenterlatitude",
           "Frame Center Latitude", "frame center latitude", "Center Latitude",
           "center latitude"}

  misb_name = "Frame Center Latitude"
  misb_key = "06 0E 2B 34 01 01 01 01 07 01 02 01 03 02 00 00"
  misb_tag = 23
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-90, 90)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class FrameCenterLongitudeElement(Element, MISB_float):
  name = "frameCenterLongitude"
  names = {"frameCenterLongitude", "FrameCenterLongitude", "framecenterlongitude",
           "Frame Center Longitude", "frame center longitude", "Center Longitude",
           "center longitude"}

  misb_name = "Frame Center Longitude "
  misb_key = "06 0E 2B 34 01 01 01 01 07 01 02 01 03 04 00 00"
  misb_tag = 24
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-180, 180)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class FrameCenterElevationElement(Element, MISB_float):
  name = "frameCenterAltitude"
  names = {"frameCenterAltitude", "FrameCenterAltitude", "framecenteraltitude",
           "Frame Center Altitude", "frame center altitude", "Center Altitude",
           "center altitude", "Center Altitude (m)", "frameCenterElevation",
           "FrameCenterElevation", "framecenterelevation"}

  misb_name = "Frame Center Elevation "
  misb_key = "06 0E 2B 34 01 01 01 0A 07 01 02 01 03 16 00 00"
  misb_tag = 25
  misb_units = "Meters"
  _domain = (0, 2**16 - 1)
  _range = (-900, 19000)

  def __init__(self, value: float):
    self.value = float(value)

class FrameCenterHeightAboveEllipsoidElement(Element, MISB_float):
  name = "frameCenterHeightAboveEllipsoid"
  names = {"frameCenterHeightAboveEllipsoid", "FrameCenterHeightAboveEllipsoid",
           "framecenterheightaboveellipsoid", "Frame Center Height Above Ellipsoid",
           "frame center height above ellipsoid"}

  misb_name = "Frame Center Height Above Ellipsoid"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 02 03 48 00 00 00"
  misb_tag = 78
  misb_units = "Meters"
  _domain = (0, 2**16 - 1)
  _range = (-900, 19000)

  def __init__(self, value: float):
    self.value = float(value)

class UASLocalSetVersionElement(Element, MISB_int):
  name = "UASLocalSetVersion"
  names = {"UASLocalSetVersion", "uaslocalsetversion", "UAS Local Set Version",
           "uas local set version", "uasLocalSetVersion"}

  misb_name = "UAS Datalink LS Version Number"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 02 03 03 00 00 00"
  misb_tag = 65
  misb_units = "None"

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

class SpeedElement(Element, MISB_int):
  name = "speed"
  names = {"speed", "Speed", "velocity", "Velocity", "badelf:speed"}

  misb_name = "Platform True Airspeed"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 0A 00 00 00"
  misb_tag = 8
  misb_units = "Meters/Second"

  def __init__(self, value: float):
    self.value = float(value)

class PlatformTailNumberElement(Element, MISB_str):
  name = "platformTailNumber"
  names = {"platformTailNumber"}

  misb_name = "Platform Tail Number"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 04 01 02 00 00 00"
  misb_tag = 4
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

class PlatformIndicatedAirspeedElement(Element, MISB_int):
  name = "platformIndicatedAirspeed"
  names = {"platformIndicatedAirspeed"}

  misb_name = "Platform Indicated Airspeed"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 0B 00 00 00"
  misb_tag = 9
  misb_units = "Meters/Second"

  def __init__(self, value: int):
    self.value = int(value)

class OffsetCornerLatitudePoint1Element(Element, MISB_float):
  name = "offsetCornerLatitude"
  names = {"offsetCornerLatitude"}

  misb_name = "Offset Corner Latitude Point 1"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 07 01 00"
  misb_tag = 26
  misb_units = "Degrees"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-0.075, 0.075)
  # TODO
  # + FrameCenterLat (Tag 23)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class OffsetCornerLatitudePoint2Element(Element, MISB_float):
  name = "offsetCornerLatitude2"
  names = {"offsetCornerLatitude2"}

  misb_name = "Offset Corner Latitude Point 2"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 08 01 00"
  misb_tag = 28
  misb_units = "Degrees"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-0.075, 0.075)
  # TODO
  # + FrameCenterLat (Tag 23)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class OffsetCornerLatitudePoint3Element(Element, MISB_float):
  name = "offsetCornerLatitude3"
  names = {"offsetCornerLatitude3"}

  misb_name = "Offset Corner Latitude Point 3"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 09 01 00"
  misb_tag = 30
  misb_units = "Degrees"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-0.075, 0.075)
  # TODO
  # + FrameCenterLat (Tag 23)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class OffsetCornerLatitudePoint4Element(Element, MISB_float):
  name = "offsetCornerLatitude4"
  names = {"offsetCornerLatitude4"}

  misb_name = "Offset Corner Latitude Point 4"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0A 01 00"
  misb_tag = 32
  misb_units = "Degrees"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-0.075, 0.075)
  # TODO
  # + FrameCenterLat (Tag 23)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class OffsetCornerLongitudePoint1Element(Element, MISB_float):
  name = "offsetCornerLongitude"
  names = {"offsetCornerLongitude"}

  misb_name = "Offset Corner Longitude Point 1"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0B 01 00"
  misb_tag = 27
  misb_units = "Degrees"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-0.075, 0.075)
  # TODO
  # + FrameCenterLong (Tag 24)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class OffsetCornerLongitudePoint2Element(Element, MISB_float):
  name = "offsetCornerLongitude2"
  names = {"offsetCornerLongitude2"}

  misb_name = "Offset Corner Longitude Point 2"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0C 01 00"
  misb_tag = 29
  misb_units = "Degrees"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-0.075, 0.075)
  # TODO
  # + FrameCenterLong (Tag 24)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class OffsetCornerLongitudePoint3Element(Element, MISB_float):
  name = "offsetCornerLongitude3"
  names = {"offsetCornerLongitude3"}

  misb_name = "Offset Corner Longitude Point 3"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0D 01 00"
  misb_tag = 31
  misb_units = "Degrees"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-0.075, 0.075)
  # TODO
  # + FrameCenterLong (Tag 24)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class OffsetCornerLongitudePoint4Element(Element, MISB_float):
  name = "offsetCornerLongitude4"
  names = {"offsetCornerLongitude4"}

  misb_name = "Offset Corner Longitude Point 4"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0E 01 00"
  misb_tag = 33
  misb_units = "Degrees"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-0.075, 0.075)
  # TODO
  # + FrameCenterLong (Tag 24)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class IcingDetectedElement(Element, MISB_int):
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
  def fromMISB(cls, value: bytes):
    return cls(cls._code[bytes_to_int(value)])

class WindDirectionElement(Element, MISB_float):
  name = "windDirection"
  names = {"windDirection"}

  misb_name = "Wind Direction"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 0D 00 00 00"
  misb_tag = 35
  misb_units = "Degrees"
  _domain = (0, 2**16 - 1)
  _range = (0, 360)

  def __init__(self, value: float):
    self.value = float(value)

class WindSpeedElement(Element, MISB_float):
  name = "windSpeed"
  names = {"windSpeed"}

  misb_name = "Wind Speed"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 0E 00 00 00"
  misb_tag = 36
  misb_units = "Meters/Second"
  _domain = (0, 255)
  _range = (0, 100)

  def __init__(self, value: float):
    self.value = float(value)

class StaticPressureElement(Element, MISB_float):
  name = "staticPressure"
  names = {"staticPressure"}

  misb_name = "Static Pressure"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 0F 00 00 00"
  misb_tag = 37
  misb_units = "Millibar"
  _domain = (0, 2**16 - 1)
  _range = (0, 5000)

  def __init__(self, value: float):
    self.value = float(value)

class DensityAltitudeElement(Element, MISB_float):
  name = "densityAltitude"
  names = {"densityAltitude"}

  misb_name = "Density Altitude"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 10 00 00 00"
  misb_tag = 38
  misb_units = "Meters"
  _domain = (0, 2**16 - 1)
  _range = (-900, 19000)

  def __init__(self, value: float):
    self.value = float(value)

# TODO: This is supposed to be a MISB_int
# Verify that changing bytes_to_int to check for sign won't break everything
class OutsideAirTemperatureElement(Element, MISB_float):
  name = "outsideAirTemperature"
  names = {"outsideAirTemperature"}

  misb_name = "Outside Air Temperature"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 11 00 00 00"
  misb_tag = 39
  misb_units = "Celsius"
  _domain = (-128, 127)
  _range = (-128, 127)

  def __init__(self, value: int):
    self.value = int(value)

class TargetLocationLatitudeElement(Element, MISB_float):
  name = "targetLocationLatitude"
  names = {"targetLocationLatitude"}

  misb_name = "Target Location Latitude"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 03 02 00 00 00"
  misb_tag = 40
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-90, 90)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class TargetLocationLongitudeElement(Element, MISB_float):
  name = "targetLocationLongitude"
  names = {"targetLocationLongitude"}

  misb_name = "Target Location Longitude"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 03 03 00 00 00"
  misb_tag = 41
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-180, 180)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class TargetLocationElevationElement(Element, MISB_float):
  name = "targetLocationElevation"
  names = {"targetLocationElevation"}

  misb_name = "Target Location Elevation"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 03 04 00 00 00"
  misb_tag = 42
  misb_units = "Meters"
  _domain = (0, 2**32 - 1)
  _range = (-900, 19000)

  def __init__(self, value: float):
    self.value = float(value)

class TargetTrackGateWidthElement(Element, MISB_int):
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
    return cls(bytes_to_int(value) * 2)

class TargetTrackGateHeightElement(Element, MISB_float):
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
    return cls(bytes_to_int(value) * 2)

class TargetErrorEstimateCE90Element(Element, MISB_float):
  name = "targetErrorEstimateCE90"
  names = {"targetErrorEstimateCE90"}

  misb_name = "Target Error Estimate - CE90"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 03 07 00 00 00"
  misb_tag = 45
  misb_units = "Meters"
  _domain = (0, 2**16 - 1)
  _range = (0, 4095)

  def __init__(self, value: float):
    self.value = float(value)

class TargetErrorEstimateLE90Element(Element, MISB_float):
  name = "targetErrorEstimateLE90"
  names = {"targetErrorEstimateLE90"}

  misb_name = "Target Error Estimate - LE90"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 03 08 00 00 00"
  misb_tag = 46
  misb_units = "Meters"
  _domain = (0, 2**16 - 1)
  _range = (0, 4095)

  def __init__(self, value: float):
    self.value = float(value)

class GenericFlagDataElement(Element, MISB_int):
  name = "genericFlagData"
  names = {"genericFlagData"}

  misb_name = "Generic Flag Data"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 03 01 00 00 00"
  misb_tag = 47
  misb_units = "None"

  def __init__(self, value: int):
    self.value = int(value)

class SecurityLocalSetElement(Element, MISB_0601):
  name = "securityLocalSet"
  names = {"securityLocalSet"}

  misb_name = "Security Local Set"
  misb_key = "06 0E 2B 34 02 03 01 01 0E 01 03 03 02 00 00 00"
  misb_tag = 48
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: bytes):
    # This contains elements from a different standard so this will have
    # to have its own special procedures because it's a fancy boi
    pass

class DifferentialPressureElement(Element, MISB_float):
  name = "differentialPressure"
  names = {"differentialPressure"}

  misb_name = "Differential Pressure"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 01 00 00 00"
  misb_tag = 49
  misb_units = "Millibar"
  _domain = (0, 2**16 - 1)
  _range = (0, 5000)

  def __init__(self, value: float):
    self.value = float(value)

class PlatformAngleofAttackElement(Element, MISB_float):
  name = "platformAngleofAttack"
  names = {"platformAngleofAttack"}

  misb_name = "Platform Angle of Attack"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 02 00 00 00"
  misb_tag = 50
  misb_units = "Degrees"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-20, 20)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class PlatformVerticalSpeedElement(Element, MISB_float):
  name = "platformVerticalSpeed"
  names = {"platformVerticalSpeed"}

  misb_name = "Platform Vertical Speed"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 03 00 00 00"
  misb_tag = 51
  misb_units = "Meters/Second"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-180, 180)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class PlatformSideslipAngleElement(Element, MISB_float):
  name = "platformSideslipAngle"
  names = {"platformSideslipAngle"}

  misb_name = "Platform Sideslip Angle"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 04 00 00 00"
  misb_tag = 52
  misb_units = "Degrees"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-20, 20)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class AirfieldBarometricPressureElement(Element, MISB_float):
  name = "airfieldBarometricPressure"
  names = {"airfieldBarometricPressure"}

  misb_name = "Airfield Barometric Pressure"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 02 02 00 00 00"
  misb_tag = 53
  misb_units = "Millibar"
  _domain = (0, 2**16 - 1)
  _range = (0, 5000)

  def __init__(self, value: float):
    self.value = float(value)

class AirfieldElevationElement(Element, MISB_float):
  name = "airfieldElevation"
  names = {"airfieldElevation"}

  misb_name = "Airfield Elevation"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 02 03 00 00 00"
  misb_tag = 54
  misb_units = "Meters"
  _domain = (0, 2**16 - 1)
  _range = (-900, 19000)

  def __init__(self, value: float):
    self.value = float(value)

class RelativeHumidityElement(Element, MISB_float):
  name = "relativeHumidity"
  names = {"relativeHumidity"}

  misb_name = "Relative Humidity"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 09 00 00 00"
  misb_tag = 55
  misb_units = "Percent"
  _domain = (0, 2**8 - 1)
  _range = (0, 100)

  def __init__(self, value: float):
    self.value = float(value)

class PlatformGroundSpeedElement(Element, MISB_int):
  name = "platformGroundSpeed"
  names = {"platformGroundSpeed"}

  misb_name = "Platform Ground Speed"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 05 00 00 00"
  misb_tag = 56
  misb_units = "Meters/Second"

  def __init__(self, value: int):
    self.value = int(value)

class GroundRangeElement(Element, MISB_float):
  name = "groundRange"
  names = {"groundRange"}

  misb_name = "Ground Range"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 06 00 00 00"
  misb_tag = 57
  misb_units = "Meters"
  _domain = (0, 2**32 - 1)
  _range = (0, 5000000)

  def __init__(self, value: float):
    self.value = float(value)

class PlatformFuelRemainingElement(Element, MISB_float):
  name = "platformFuelRemaining"
  names = {"platformFuelRemaining"}

  misb_name = "Platform Fuel Remaining"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 07 00 00 00"
  misb_tag = 58
  misb_units = "Kilograms"
  _domain = (0, 2**16 - 1)
  _range = (0, 10000)

  def __init__(self, value: float):
    self.value = float(value)

class PlatformCallSignElement(Element, MISB_str):
  name = "platformCallSign"
  names = {"platformCallSign"}

  misb_name = "Platform Call Sign"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 04 01 01 00 00 00"
  misb_tag = 59
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

class WeaponLoadElement(Element, MISB_int):
  name = "weaponLoad"
  names = {"weaponLoad"}

  misb_name = "Weapon Load"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 12 00 00 00"
  misb_tag = 60
  misb_units = "None"

  def __init__(self, value: int):
    self.value = int(value)

class WeaponFiredElement(Element, MISB_int):
  name = "weaponFired"
  names = {"weaponFired"}

  misb_name = "Weapon Fired"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 13 00 00 00"
  misb_tag = 61
  misb_units = "None"

  def __init__(self, value: int):
    self.value = int(value)

class LaserPRFCodeElement(Element, MISB_int):

  name = "laserPRFCode"
  names = {"laserPRFCode"}

  misb_name = "Laser PRF Code"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 02 02 01 00 00 00"
  misb_tag = 62
  misb_units = "None"

  def __init__(self, value: int):
    self.value = int(value)

class SensorFieldofViewNameElement(Element, MISB_int):
  name = "sensorFieldofViewName"
  names = {"sensorFieldofViewName"}

  misb_name = "Sensor Field of View Name"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 02 02 02 00 00 00"
  misb_tag = 63
  misb_units = "None"

  _code = {0 : "Ultranarrow",
           1 : "Narrow",
           2 : "Medium",
           3 : "Wide",
           4 : "Ultrawide",
           5 : "Narrow Medium",
           6 : "2x Ultranarrow",
           7 : "4x Ultranarrow"}

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: bytes):
    return cls(cls._code[bytes_to_int(value)])

class PlatformMagneticHeadingElement(Element, MISB_float):
  name = "platformMagneticHeading"
  names = {"platformMagneticHeading"}

  misb_name = "Platform Magnetic Heading"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 08 00 00 00"
  misb_tag = 64
  misb_units = "Degrees"
  _domain = (0, 2**16 - 1)
  _range = (0, 360)

  def __init__(self, value: float):
    self.value = float(value)

class AlternatePlatformLatitudeElement(Element, MISB_float):
  name = "alternatePlatformLatitude"
  names = {"alternatePlatformLatitude"}

  misb_name = "Alternate Platform Latitude"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 14 00 00 00"
  misb_tag = 67
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-90, 90)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class AlternatePlatformLongitudeElement(Element, MISB_float):
  name = "alternatePlatformLongitude"
  names = {"alternatePlatformLongitude"}

  misb_name = "Alternate Platform Longitude"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 15 00 00 00"
  misb_tag = 68
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-180, 180)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class AlternatePlatformAltitudeElement(Element, MISB_float):
  name = "alternatePlatformAltitude"
  names = {"alternatePlatformAltitude"}

  misb_name = "Alternate Platform Altitude"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 16 00 00 00"
  misb_tag = 69
  misb_units = "Degrees"
  _domain = (0, 2**32 - 1)
  _range = (-900, 19000)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class AlternatePlatformNameElement(Element, MISB_str):
  name = "alternatePlatformName"
  names = {"alternatePlatformName"}

  misb_name = "Alternate Platform Name"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 17 00 00 00"
  misb_tag = 70
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

class AlternatePlatformHeadingElement(Element, MISB_float):
  name = "alternatePlatformHeading"
  names = {"alternatePlatformHeading"}

  misb_name = "Alternate Platform Heading"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 18 00 00 00"
  misb_tag = 71
  misb_units = "Degrees"
  _domain = (0, 2**16 - 1)
  _range = (0, 360)

  def __init__(self, value: str):
    self.value = str(value)

class EventStartTimeUTCElement(Element, MISB_int):
  name = "eventStartTimeUTC"
  names = {"evenStartTimeUTC"}

  misb_name = "Event Start Time - UTC"
  misb_key = "06 0E 2B 34 01 01 01 01 07 02 01 02 07 01 00 00"
  misb_tag = 72
  misb_units = "Microseconds"

  def __init__(self, value: str):
    self.value = str(value)

class RVTLocalSetElement(Element, MISB_0601):
  name = "RVTLocalSet"
  names = {"RVTLocalSet"}

  misb_name = "RVT Local Set"
  misb_key = "06 0E 2B 34 02 0B 01 01 0E 01 03 01 02 00 00 00"
  misb_tag = 73
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: bytes):
    # MISB ST 0806
    # This contains elements from a different standard so this will have
    # to have its own special procedures because it's a fancy boi
    pass

class VMTILocalSetElement(Element, MISB_0601):
  name = "VMTILocalSet"
  names = {"VMTILocalSet"}

  misb_name = "VMTI Local Set"
  misb_key = "06 0E 2B 34 02 0B 01 01 0E 01 03 03 06 00 00 00"
  misb_tag = 74
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: bytes):
    # MISB ST 0903
    # This contains elements from a different standard so this will have
    # to have its own special procedures because it's a fancy boi
    pass

class AlternatePlatformEllipsoidHeightElement(Element, MISB_float):
  name = "alternatePlatformEllipsoidHeight"
  names = {"alternatePlatformEllipsoidHeight", "AlternatePlatformEllipsoidHeight", "alternateplatformellipsoidheight",
           "Alternate Platform Ellipsoid Height", "alternate platform ellipsoid height"}

  misb_name = "Allternate Platform Ellipsoid Height"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 02 01 82 48 00 00"
  misb_tag = 76
  misb_units = "Meters"
  _domain = (0, 2**16 - 1)
  _range = (-900, 19000)

  def __init__(self, value: float):
    self.value = float(value)

class OperationalModeElement(Element, MISB_int):
  name = "operationalMode"
  names = {"operationalMode"}

  misb_name = "Operational Mode"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 03 21 00 00 00"
  misb_tag = 77
  misb_units = "Meters"
  _code = {0 : "Other",
           1 : "Operational",
           2 : "Training",
           3 : "Exercise",
           4 : "Maintenance",
           5 : "Test"}

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: bytes):
    return cls(cls._code[bytes_to_int(value)])

class SensorNorthVelocityElement(Element, MISB_float):
  name = "sensorNorthVelocity"
  names = {"sensorNorthVelocity"}

  misb_name = "Sensor North Velocity"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 02 02 7E 00 00 00"
  misb_tag = 79
  misb_units = "Meters/Second"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-327, 327)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class SensorEastVelocityElement(Element, MISB_float):
  name = "sensorEastVelocity"
  names = {"sensorEastVelocity"}

  misb_name = "Sensor East Velocity"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 02 02 7F 00 00 00"
  misb_tag = 80
  misb_units = "Meters/Second"
  _domain = (-(2**15 - 1), 2**15 - 1)
  _range = (-327, 327)
  _invalid = bytes.fromhex('8000')

  def __init__(self, value: float):
    self.value = float(value)

class ImageHorizonPixelPackElement(Element, MISB_0601):
  name = "imageHorizonPixelPack"
  names = {"imageHorizonPixelPack"}

  misb_name = "image Horizon Pixel Pack"
  misb_key = "06 0E 2B 34 02 05 01 01 0E 01 03 02 08 00 00 00"
  misb_tag = 81 
  misb_units = "None"

  def __init__(self, value: float):
    self.value = float(value)

  @classmethod
  def fromMISB(cls, value: str):
    # Looks like the initialization for this is system dependent
    # Something fancy will need to be done if this ever gets implemented
    pass

class CornerLatitudePoint1Element(Element, MISB_float):
  name = "cornerLatitudePoint1"
  names = {"cornerLatitudePoint1"}

  misb_name = "Corner Latitude Point 1 (Full)"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 07 01 00"
  misb_tag = 82
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-90, 90)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class CornerLongitudePoint1Element(Element, MISB_float):
  name = "cornerLongitudePoint1"
  names = {"cornerLongitudePoint1"}

  misb_name = "Corner Longitude Point 1 (Full)"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0B 01 00"
  misb_tag = 83
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-180, 180)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class CornerLatitudePoint2Element(Element, MISB_float):
  name = "cornerLatitudePoint2"
  names = {"cornerLatitudePoint2"}

  misb_name = "Corner Latitude Point 2 (Full)"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 08 01 00"
  misb_tag = 84
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-90, 90)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class CornerLongitudePoint2Element(Element, MISB_float):
  name = "cornerLongitudePoint2"
  names = {"cornerLongitudePoint2"}

  misb_name = "Corner Longitude Point 2 (Full)"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0C 01 00"
  misb_tag = 85
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-180, 180)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class CornerLatitudePoint3Element(Element, MISB_float):
  name = "cornerLatitudePoint3"
  names = {"cornerLatitudePoint3"}

  misb_name = "Corner Latitude Point 3 (Full)"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 09 01 00"
  misb_tag = 86
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-90, 90)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class CornerLongitudePoint3Element(Element, MISB_float):
  name = "cornerLongitudePoint3"
  names = {"cornerLongitudePoint3"}

  misb_name = "Corner Longitude Point 3 (Full)"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0D 01 00"
  misb_tag = 87
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-180, 180)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class CornerLatitudePoint4Element(Element, MISB_float):
  name = "cornerLatitudePoint4"
  names = {"cornerLatitudePoint4"}

  misb_name = "Corner Latitude Point 4 (Full)"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0A 01 00"
  misb_tag = 88
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-90, 90)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class CornerLongitudePoint4Element(Element, MISB_float):
  name = "cornerLongitudePoint4"
  names = {"cornerLongitudePoint4"}

  misb_name = "Corner Longitude Point 4 (Full)"
  misb_key = "06 0E 2B 34 01 01 01 03 07 01 02 01 03 0E 01 00"
  misb_tag = 89
  misb_units = "Degrees"
  _domain = (-(2**31 - 1), 2**31 - 1)
  _range = (-180, 180)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class PlatformAngleofAttackFullElement(Element, MISB_float):
  name = "PlatformAngleofAttackFull"
  names = {"PlatformAngleofAttackFull"}

  misb_name = "Platform Angle of Attack (Full)"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 02 00 00 00"
  misb_tag = 92
  misb_units = "Degrees"
  _range = (-90, 90)
  _domain = (-(2**31 - 1), 2**31 - 1)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class PlatformSideslipAngleFullElement(Element, MISB_float):
  name = "PlatformSideslipAngleFull"
  names = {"PlatformSideslipAngleFull"}

  misb_name = "Platform Sideslip Angle (Full)"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 01 01 04 00 00 00"
  misb_tag = 93
  misb_units = "Degrees"
  _range = (-180, 180)
  _domain = (-(2**31 - 1), 2**31 - 1)
  _invalid = bytes.fromhex('8000 0000')

  def __init__(self, value: float):
    self.value = float(value)

class MIISCoreIdentifierElement(Element, MISB_0601):
  name = "MIISCoreIdentifier"
  names = {"MIISCoreIdentifier"}

  misb_name = "MIIS Core Identifier"
  misb_key = "06 0E 2B 34 01 01 01 01 0E 01 04 05 03 00 00 00"
  misb_tag = 94
  misb_units = "None"

  def __init__(self, value: bytes):
    self.value = bytes(value)

  @classmethod
  def fromMISB(cls, value: bytes):
    # MISB ST 1204
    # TODO: Not technically correct
    return cls(value)

class SARMotionImageryLocalSetElement(Element, MISB_0601):
  name = "SARMotionImageryLocalSet"
  names = {"SARMotionImageryLocalSet"}

  misb_name = "SAR Motion Imagery Local Set"
  misb_key = "06 0E 2B 34 02 0B 01 01 0E 01 03 03 0D 00 00 00"
  misb_tag = 95
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: bytes):
    # MISB 1206
    # This contains elements from a different standard so this will have
    # to have its own special procedures because it's a fancy boi
    pass

class RangeImageLocalSetElement(Element, MISB_0601):
  name = "rangeImageLocalSet"
  names = {"rangeImageLocalSet"}

  misb_name = "Range Image Local Set"
  misb_key = "06 0E 2B 34 02 0B 01 01 0E 01 03 03 0C 00 00 00"
  misb_tag = 97
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: bytes):
    # MISB 1002
    # This contains elements from a different standard so this will have
    # to have its own special procedures because it's a fancy boi
    pass

class GeoRegistrationLocalSetElement(Element, MISB_0601):
  name = "geoRegistrationLocalSet"
  names = {"geoRegistrationLocalSet"}

  misb_name = "Geo-Registration Local Set"
  misb_key = "06 0E 2B 34 02 0B 01 01 0E 01 03 03 01 00 00 00"
  misb_tag = 98
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: bytes):
    # MISB 1601
    # This contains elements from a different standard so this will have
    # to have its own special procedures because it's a fancy boi
    pass

class CompositeImagingLocalSetElement(Element, MISB_0601):
  name = "compositeImagingLocalSet"
  names = {"compositeImagingLocalSet"}

  misb_name = "Composite Imaging Local Set"
  misb_key = "06 0E 2B 34 02 0B 01 01 0E 01 03 03 02 00 00 00"
  misb_tag = 99
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: bytes):
    # MISB 1602
    # This contains elements from a different standard so this will have
    # to have its own special procedures because it's a fancy boi
    pass

class SegmentLocalSetElement(Element, MISB_0601):
  name = "segmentLocalSet"
  names = {"segmentLocalSet"}

  misb_name = "Segment Local Set"
  misb_key = "06 0E 2B 34 02 0B 01 01 0E 01 03 03 03 00 00 00"
  misb_tag = 100
  misb_units = "None"

  def __init__(self, value: str):
    self.value = str(value)

  @classmethod
  def fromMISB(cls, value: bytes):
    # MISB 1607
    # This contains elements from a different standard so this will have
    # to have its own special procedures because it's a fancy boi
    pass
