import open_telemetry_kit.writers as write
import open_telemetry_kit.detector as detector
from open_telemetry_kit.telemetry import Telemetry

import sys

# Read in source file and output file
source = sys.argv[1]
dest = sys.argv[2]

# Create Parser object used to parse source file
parser = detector.create_telemetry_parser(source)

# Use parser object to read telemetry
# Returns a Telemetry object
telemetry = parser.read()

# Example telemetry manipulation
# Filters out anything thats not a GPS element
gps = Telemetry()
for packet in telemetry:
  gps.append({ k:v for k, v in packet.items() if k in ['latitude', 'longitude', 'altitude']})

# Write Telemetry object to JSON
write.telemetryToJson(gps, dest)