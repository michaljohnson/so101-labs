# Lab 3 — the real arm (Jetson) 🚧

The arm is plugged into a Jetson by USB. The Jetson runs only what has to sit next to
the arm: the servo driver and ros2_control, which updates the servos at 50 Hz and must
not depend on the network. MoveIt, RViz and your code run on RAP.

Jetsons run JetPack (usually Ubuntu 22.04), and ROS 2 Jazzy needs 24.04, so the robot
side runs in a container. `robot/Dockerfile` builds on `ros:jazzy-ros-base`, which
exists for arm64 — build it on the Jetson itself:

```bash
git clone https://github.zhaw.ch/cas-physical-ai/so101-labs.git && cd so101-labs
docker build -t cas-so101-robot robot/
```

Start it (arm on `/dev/ttyACM0`; `run.sh` maps it to `/dev/LeRobotFollower` inside):

```bash
robot/run.sh                  # driver + controllers only
xhost +local:                 # once, if RViz should open on the Jetson's monitor
robot/run.sh /dev/ttyACM0 ros2 launch so_arm101_moveit_config demo.launch.py hardware_type:=real
```

**Before executing any motion**, compare the arm in RViz with the physical arm: the zero
pose comes from the arm's LeRobot calibration and may differ from the model's zero pose.
Keep a hand near the power switch for the first moves.
