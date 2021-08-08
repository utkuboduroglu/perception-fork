#!/usr/bin/env bash

# specify input device first
if [ "$1" == "" ]; then
    echo "Please specify a video device."
    exit 1
fi

IN_DEVICE=$1

# we set the scale as a multiple of 416x416
SCALE=1664:832

mkdir -p ./data
OUT_SEQ=./data/image_sequence.h264
OUT_VID=./data/converted.mp4

# Stereo camera has 2 FHD cameras, thus the original resolution is 3840x1080
# Save the input as an image sequence
ffmpeg -y -i $IN_DEVICE -vf scale=$SCALE -f h264 $OUT_SEQ
# try to kill this process without disrupting the script; or we don't get to the later part

# save the image_sequence file to an mp4, the framerate doesn't matter
ffmpeg -y -r 30 -i $OUT_SEQ -c copy $OUT_VID

du -h $OUT_VID

# or maybe use
# ffmpeg -i Forest.mp4 -vsync 0 forest/jpegs%06d.jpg
