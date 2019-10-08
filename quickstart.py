import open_telemetry_kit.writers as write
import open_telemetry_kit.detector as detector

import sys

source = sys.argv[1]
dest = sys.argv[2]

parser = detector.create_telemetry_parser(source)
telemetry = parser.read()
write.telemetryToJson(telemetry, dest)