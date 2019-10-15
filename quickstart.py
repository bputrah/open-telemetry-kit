import open_telemetry_kit.writers as write
import open_telemetry_kit.detector as detector
from open_telemetry_kit.telemetry import Telemetry

import sys

# Read in source file and output file
source = sys.argv[1]
dest = sys.argv[2]

# This package is organized in Parser, Telemetry, Packet, and Element objects.
# A Parser is initialized with the source and is used to read in and parse the 
#    telemetry into a Telemetry object.
# A Telemetry object is a list of Packet objects.
# A Packet object is a dictionary of Elements and represents a temporal 
#    grouping of the telmetry. (e.g. data all recorded during at the same 
#    timestamp). The key is the canonical name of the data ('latitude', 
#    'longitude', etc.). The value is the Element object itself 
# An Element contains the actual value of the reading.
# There is also a small library of functions used for telemetry type detection
#    as well as writing the Telemetry to a new file.

# Create Parser object used to parse source file
parser = detector.create_telemetry_parser(source)

# Use parser object to read telemetry
# Returns a Telemetry object
telemetry = parser.read()

# Write Telemetry object to JSON
write.telemetryToJson(telemetry, dest)

# Example telemetry manipulation
# Filters out anything thats not a GPS element
# gps = Telemetry()
# for packet in telemetry:
#   gps.append({ k:v for k, v in packet.items() if k in ['latitude', 'longitude', 'altitude']})

# Write gps only Telemetry object to JSON
# write.telemetryToJson(gps, dest)