#!/usr/bin/env bash

ROS_WORKSPACE=/home/vm/catkin_ws
QEMU_PERCEPTION_PATH=$ROS_WORKSPACE/src/perception

if [ ! -e $DRVLSS_PERCEPTION_PATH ]; then
    echo "Please set your perception path first." >&2
    exit
fi

# We use this script to execute changes in the codebase through a running
# virtual machine with sshd listening on vm@localhost at port 7777

# We first send our changes through rsync
rsync -vrz -e 'ssh -p7777' --progress $DRVLSS_PERCEPTION_PATH vm@localhost:$QEMU_PERCEPTION_PATH \
	--exclude venv38 \
	--exclude .git \
	--exclude submodules \
	--exclude data \
	--exclude dummylogs
# Then assuming roscore is running, we run $1
ssh -p7777 vm@localhost << EOF
	source $ROS_WORKSPACE/devel/setup.bash;
	cd $ROS_WORKSPACE && catkin_make;
	rosrun perception $1;
EOF
