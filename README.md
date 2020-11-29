# ITWORKS.sometimes

# How To Install

git clone https://github.com/Tsukun/ITWORKS.sometimes.git
 
## Install Dependecies:
  cython
  
  numpy>=1
  
  numpy
  
  pydub
  
  scipy
  
  werkzeug
  
  flask
  
  matplotlib
  
## Running

Load your music in music/ directory

Run reset-db.py to reset database of music

Run collect-fingerprints-by-dir to save music in your database

Run Server.py

#### If error:
> RuntimeWarning: Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work

> RuntimeWarning: Couldn't find ffprobe or avprobe - defaulting to ffprobe, but may not work
#### Do:
open a powershell in administration mode

choco install -y ffmpeg


  
