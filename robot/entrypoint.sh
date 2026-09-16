#!/bin/bash
# Load ROS and the built workspace, then run the given command.
source /opt/ros/jazzy/setup.bash
source /ws/install/setup.bash
exec "$@"
