#!/usr/bin/env bash
### GNU bash, version 5.1.4(1)-release (x86_64-pc-linux-gnu)
### ffmpeg version n4.4 Copyright (c) 2000-2021 the FFmpeg developers
###   built with gcc 10.2.0 (GCC)
### grep (GNU grep) 3.6

# create -h message fnc and call it whenever the user messes up or calls -h

# HERE ARE SOME DEFAULT VALUES FOR THE SCRIPT
# IN THE FUTURE, WE CAN ADD ENVIRONMENT VARIABLE SUPPORT FOR THESE
DEV_COUNT=2
# create logs directory just in case
# check if DRVLSS_LOG_PATH exists, if not, save to local
if [ -e "$DRVLSS_LOG_PATH" ]; then
    LOG_PATH=$DRVLSS_LOG_PATH
else
    LOG_PATH=$PWD
fi

mkdir -p $LOG_PATH/dummylogs
LOG_FILE=$LOG_PATH/dummylogs/dummycam.$(date +%H%M).log

OPTS=$(getopt -o "f:h" -l "file: help" -- "$@")
eval set -- "$OPTS"
unset OPTS

function help_msg() {
    echo -ne "Usage: $0 -f|--file [media file] -h|--help\n"
    exit 0
}

while true; do
    case "$1" in
        '-f'|'--file')
            MFILE=$2
            shift 2
            continue
        ;;
        '-h'|'--help')
            help_msg
            break
        ;;
        '--')
            shift
            break
        ;;
        *)
            echo "Pretty bad error. Start the script again."
            exit 1
        ;;
    esac
done


if ! [ -e "$MFILE" ]; then
	echo "The file you specified does not exist or cannot be accessed." 1>&2;
    help_msg >&2
	exit
fi

## start off simple: create a single video device off v4l2loopback
# check whether v4l2loopback is running
if [ "$(lsmod | grep -E '^v4l2loopback')" == "" ]; then
	echo "v4l2loopback is not running. Please sudo to run it."
    sudo -k modprobe v4l2loopback devices=$DEV_COUNT
	if [ "$(lsmod | grep -E '^v4l2loopback')" == "" ]; then
		echo "Failed to run v4l2loopback." 1>&2;
		exit
	fi
fi

# get a list of all dummy devices
DEVICES=$(v4l2-ctl --list-devices  |\
    sed -n '/v4l2loopback/,/^$/p' |\
    grep -v v4l2loopback |\
    sed 's/\s//g; /^[[:space:]]*$/d')

# pick the first available device
while IFS= read -r line; do
    DEVICE_NAME=$line
    if [ "$(fuser $DEVICE_NAME)" == "" ]; then
        break
    fi
    DEVICE_NAME="NO_DEVICE"
done <<< "$DEVICES"

if [ $DEVICE_NAME == "NO_DEVICE" ]; then
    echo "No devices are available." 1>&2;
    exit
fi

# check for other users
if [ "$(fuser $DEVICE_NAME)" != "" ]; then
	echo -e "Someone is already using the device $DEVICE_NAME.\n" \
		    "Please make sure no one is using the device before continuing.\n" 1>&2;
	exit
fi

## and pipe the specified footage to the device
echo -e "Writing output to device:\n"$DEVICE_NAME
ffmpeg -nostdin -re -stream_loop -1 -vsync vfr -i "$MFILE" -f v4l2 $DEVICE_NAME > $LOG_FILE 2>&1
