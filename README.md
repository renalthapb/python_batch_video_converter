Batch Video Converter
==========================

Batch Video Converter Written in Python

Curently Support :
1. (.ts) to (.mp4) convert
2. Only support for Windows OS
3. NVidia Hardware Acceleration On by default

Using [FFMPEG](https://ffmpeg.org/download.html) (windows build) and [althonos's ffpb](https://github.com/althonos/ffpb)

Requirements:
-------------
- Python 3.7.x
- Python tqdm
- ffmpeg windows build

Usage:
---------
- download ffmpeg from https://ffmpeg.org/download.html (windows build)
- extract all files to folder ffmpeg
- change `source_dir` variable in `batch_converter.py` into the location of the folder you want to convert
- make sure the (.ts) video is in that folder
- run `batch_converter.py`


To Do:
---------
- [ ] support more video encoder
- [ ] support more OS
- [ ] support more hardware acceleration
- [ ] terminal GUI
- [ ] ...
