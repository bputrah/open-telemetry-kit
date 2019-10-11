# Open Telemetry Kit

![Image of Open Telemetry Kit](https://github.com/Hivemapper/open-telemetry-kit/blob/master/OTK.jpg)

The Open Telemetry Kit (OTK) is an open source package for extracting and parsing telemetry associated with video streams and converting to common formats.
It comes out of a need for a singular API that can be used for multiple different video telemetry formats.

Telemetry that can be parsed includes: GPS, time, camera information, speed

Features:
- Automatically detect telemetry format
- Manipulate telemetry with ease
- Write telemetry to a new format

## Getting Started
### Prerequisites
Python version: `>=3.6`

`ffmpeg` and `ffprobe`.

On Debian systems these can be installed with:
>$ sudo apt install ffmpeg

`dateutil`

On Debian systems this can be installed with:
>$ pip install python-dateutil

### Installation
>$ pip install open-telemetry-kit

### Importing
The OTK package can be imported into your project with:
>import open_telemetry_kit as otk

### Quick Start
Download `quickstart.py` and `DJI_telemetry.srt` from the [Open Telemetry Kit](https://github.com/Hivemapper/open-telemetry-kit/quickstart) git page.

Execute the script via:
>$ python3 quickstart.py [/path/to/source/DJI_telemetry.json] [/path/to/save/destination.json]

The script accepts a standalone `.csv` or `.srt` or a video file with an embedded `.srt`. 
It will read in the data, convert it to JSON, and write it to the provided destination. 

Note: this process will create a `metadata.json` file in the same path as the source file. 
If the telemetry is embedded it will also extract the data into `[video_name].json`

### Current Functionality
#### Input Formats
The OTK currently supports the following forms of telemetry:
- `.csv` files
- `.srt` files
- Any video file with embedded telemetry encoded as a `.srt` (e.g. video taken with some DJI drone models)

#### Output Formats
- JSON

### Future Releases
Planned expansions and updates for the OTK include:
#### Input Formats
- `.kml`
- `.gpx`
- KLV/MISB embedded data

#### Output Formats
- geoJSON

#### Other
- Logging
- Error checking
- Unit Tests
