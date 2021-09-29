#!/usr/bin/env bash

# we check for environment variables related to the script first
if [ -e "$DRVLSS_OUT_PATH" ]; then
	OUT_PATH=$DRVLSS_OUT_PATH
else
	OUT_PATH=$PWD
fi

# we parse command line arguments
OPTS=$(getopt -o "i:" -l "input:" -- "$@")
eval set -- "$OPTS"
unset OPTS

if [ $? -ne 0 ] || [ $# -lt 2 ]; then
    echo -ne "Error parsing arguments. Please check what you passed.\n" \
             "Usage: $0 -i|--input <input device>\n"
    exit 1
fi

while true; do
    case "$1" in
        '-i'|'--input')
            IN_DEVICE=$2
            shift 2
            continue
        ;;
        '--')
            shift
            break
        ;;
        *)
            echo "bruh you done wrong" >&2
            exit 1
        ;;
    esac
done

# we set the scale as a multiple of 416x416
SCALE=1664:832

# set output file names relevant to time
DATE_STR=$(date +%d%y_%H%M)

# we force the data folder to exist
mkdir -p $OUT_PATH/data
OUT_SEQ=$OUT_PATH/data/image_sequence_$DATE_STR.h264
OUT_VID=$OUT_PATH/data/converted_$DATE_STR.mp4
# log ffmpeg outputs to DRVLSS_LOG_PATH
OUT_LOG=$OUT_PATH/sequence_$DATE_STR.log

# Stereo camera has 2 FHD cameras, thus the original resolution is 3840x1080
# Save the input as an image sequence
ffmpeg -y -i $IN_DEVICE -vf scale=$SCALE -f h264 $OUT_SEQ
# try to kill this process without disrupting the script; or we don't get to the later part

# save the image_sequence file to an mp4, the framerate doesn't matter
ffmpeg -y -r 30 -i $OUT_SEQ -c copy $OUT_VID

# display the size of our write
du -h $OUT_VID
exit 0
