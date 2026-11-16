# Lab 1 — workspace and simulation

Set the workspace up once, then session 3 runs the arm in Gazebo.

## Set up the workspace 

### What you need

| Source | What it is | How you get it |
|---|---|---|
| [ros-physical-ai/ros2_so_arm](https://github.com/ros-physical-ai/ros2_so_arm) | SO-101 model, controllers, Gazebo | `git clone` |
| [JafarAbdi/feetech_ros2_driver](https://github.com/JafarAbdi/feetech_ros2_driver) | servo driver; `ros2_so_arm` depends on it, not available via apt | `git clone` |
| this repo | `setup.sh`, the SO-101 MoveIt config (lab 2) | `git clone` |

### 2.1 Where to put it

On RAP only `~/rap` survives a pod restart; the home folder (including `~/.bashrc`)
is reset. Check with `findmnt -T ~/rap` — it must show its own device (e.g. `/dev/vdb`).
Keep the course in its own folder there:

```
~/rap/cas/
├── COLCON_IGNORE          # stops a colcon build started in ~/rap from building this
├── setup.sh -> so101_ws/src/cas-so101/setup.sh    # a link, so git pull updates it
└── so101_ws/
    ├── src/
    │   ├── ros2_so_arm/                   # from GitHub, untouched
    │   ├── feetech_ros2_driver/           # from GitHub, untouched
    │   └── cas-so101/                     # this repo: so_arm101_moveit_config
    ├── build/  install/  log/             # created by colcon, safe to delete
```

colcon finds the packages inside `cas-so101/` by itself; the README and `setup.sh`
next to them are ignored by the build.

### 2.2 Get the code

```bash
mkdir -p ~/rap/cas/so101_ws/src
touch ~/rap/cas/COLCON_IGNORE
cd ~/rap/cas/so101_ws/src
git clone https://github.com/ros-physical-ai/ros2_so_arm.git
git clone https://github.com/JafarAbdi/feetech_ros2_driver.git
git clone https://github.com/michaljohnson/cas-so101.git
ln -sf ~/rap/cas/so101_ws/src/cas-so101/setup.sh ~/rap/cas/setup.sh
```

To get course updates later: `cd ~/rap/cas/so101_ws/src/cas-so101 && git pull`.

What `setup.sh` does, line by line:

| Line | Why |
|---|---|
| `deactivate` / `conda deactivate` | a Python venv or conda env makes colcon and `ros2` use the wrong Python |
| `export DISPLAY=:0` (only if empty) | over SSH there is no screen; this sends Gazebo/RViz windows to the web desktop |
| `source /opt/ros/jazzy/setup.bash` | loads ROS 2 itself |
| `export ROS_DOMAIN_ID=42` | own "channel" for this workspace, so nodes from other projects on the same machine or network don't mix in |
| `source $ws/install/setup.bash` | loads your built packages on top of ROS |
| `rosdep check` | warns if system packages vanished after a pod restart |

### 2.3 Build

```bash
source ~/rap/cas/setup.sh so101
rosdep install --from-paths src --ignore-src -r -y     # system packages the code needs
colcon build --symlink-install
source ~/rap/cas/setup.sh so101                        # again, to load the fresh build
```

`--symlink-install` links Python launch files and configs from `install/` back to
`src/` instead of copying them, so editing a launch file or YAML needs no rebuild.
Only new packages or C++ changes need `colcon build` again.

After moving a workspace to another folder, delete `build/ install/ log/` and rebuild —
they contain absolute paths.

### 2.4 After every pod restart

```bash
source ~/rap/cas/setup.sh so101
```

If it prints `dependencies missing`, run the `rosdep install` line it shows: packages
installed by rosdep live outside `~/rap` and are lost on restart; your build is not.
Every new terminal needs this `source` line too.

---

## Gazebo + ros2_control (session 3)

Gazebo and RViz need a screen: use a terminal in the web desktop, or SSH with
`setup.sh` (which sets `DISPLAY=:0`).

### 3.1 Start Gazebo 

```bash
# terminal 1
source ~/rap/cas/setup.sh so101
ros2 launch so_arm_gz so_arm_gz_bringup.launch.py        # SO-101 is the default arm
```

Gazebo and RViz open with the arm. Press ▶ in Gazebo if the simulation is paused.

### 3.2 Command the joints 

```bash
# terminal 2
source ~/rap/cas/setup.sh so101
ros2 control list_controllers          # joint_state_broadcaster, forward_position_controller
ros2 topic echo /joint_states --once
```

Move the arm — 5 values in radians: shoulder_pan, shoulder_lift, elbow_flex, wrist_flex, wrist_roll:

```bash
ros2 topic pub --once /forward_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.5, -0.5, 0.5, 0.3, 0.0]}"
ros2 topic pub --once /forward_position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.0, 0.0, 0.0, 0.0, 0.0]}"
```

Switch to the trajectory controller, which moves smoothly over a given time instead
of jumping:

```bash
ros2 control load_controller --set-state inactive joint_trajectory_controller
ros2 control switch_controllers --deactivate forward_position_controller --activate joint_trajectory_controller
ros2 topic pub --once /joint_trajectory_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory \
  "{joint_names: [shoulder_pan_joint, shoulder_lift_joint, elbow_flex_joint, wrist_flex_joint, wrist_roll_joint],
    points: [{positions: [0.5, -0.3, 0.3, 0.0, 0.0], time_from_start: {sec: 2}}]}"
```

---
