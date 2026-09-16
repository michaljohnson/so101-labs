#!/bin/bash
# Start the robot side on the Jetson.
#
#   ./run.sh                          driver + controllers, arm on /dev/ttyACM0
#   ./run.sh /dev/ttyACM1             arm on another port
#   ./run.sh /dev/ttyACM0 ros2 launch so_arm101_moveit_config demo.launch.py hardware_type:=real
#                                     local test with MoveIt + RViz (needs a monitor on the Jetson)
port="${1:-/dev/ttyACM0}"
shift

# --network/--ipc host: ROS nodes in the container talk to the Jetson and the lab
#   network directly (DDS discovery and shared memory need both).
# --device: the arm appears inside as /dev/LeRobotFollower, the name ros2_so_arm expects.
# DISPLAY + X11 socket: lets RViz open on the Jetson's monitor (run `xhost +local:` once).
docker run --rm -it --name so101 \
  --network host --ipc host \
  --device "$port":/dev/LeRobotFollower \
  -e ROS_DOMAIN_ID=42 \
  -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
  cas-so101-robot "$@"
