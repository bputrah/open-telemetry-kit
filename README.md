# Open Telemetry Kit

![Image of Open Telemetry Kit](https://github.com/Hivemapper/open-telemetry-kit/blob/master/OTK.jpg)

The Open Telemetry Kit (OTK) is an open source package for extracting and parsing telemetry associated with video streams and converting to common formats.
It comes out of a need for a singular API that can be used for multiple different video telemetry formats.

- Automatically detect telemetry format
- Manipulate telemetry with ease
- Write telemetry to a new format

## Getting Started
### Prerequisites
ffmpeg and ffprobe
>$ sudo apt install ffmpeg

### Installation
>$ pip install open-telemetry-kit

### Quick Start
Download `quickstart.py` from the [Open Telemetry Kit](https://github.com/Hivemapper/open-telemetry-kit/) git page.

Execute the script via:
>$ python3 quickstart.py [/path/to/source/file.ext] [/path/to/save/dest.json]

The script accepts a `.csv`, `.srt` or a video file with embedded subtitles. 
It will read in the data, convert it to JSON, and write it to the provided destination.

### Current Functionality
#### Reading
The OTK currently works with the following forms of telemetry:
- `.csv` files
- `.srt` files
- Any video file with embedded subtitles (e.g. video taken with some DJI drone models)

#### Writing
- JSON

### Future Releases
Expansions and updates for the OTK include but are not limited to:
#### Reading
- kml
- gpx
- klv

#### Writing
- geoJSON
- Binary formats?

#### Other
- Logging
- Error checking
- Unit Testing
