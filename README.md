# SO-101 arm labs — CAS Physical AI & Robotics, Module C

The SO-ARM101 in simulation and on the real arm, with ROS 2 Jazzy. Sessions 2 (URDF/Xacro),
3 (Gazebo + `ros2_control`) and 8 (MoveIt pick).

```
SO-101 arm ──USB── Jetson ──network── RAP cluster
                   driver only        Gazebo, RViz, MoveIt, your nodes
```

The arm is a USB device, so a small driver runs on the computer it is plugged into. Everything
heavy runs on the cluster — you need neither a GPU nor a ROS install on your own laptop.

| Page | What it is |
|---|---|
| [docs/lab1-sim.md](docs/lab1-sim.md) | set up the workspace in the pod, then the arm in Gazebo ✅ |
| [docs/lab2-moveit.md](docs/lab2-moveit.md) | MoveIt: planning, named poses, picking an object |
| [docs/lab3-real.md](docs/lab3-real.md) | the real arm on the Jetson 🚧 |
| [docs/troubleshooting.md](docs/troubleshooting.md) | when something doesn't work |
| [viz/README.md](viz/README.md) | seeing it from your own laptop |

✅ = tested end to end · 🚧 = not tested yet.

| Folder | Contents |
|---|---|
| `so_arm101_moveit_config/` | MoveIt config for the SO-101: SRDF, kinematics, planners, RViz, `demo.launch.py` |
| `setup.sh` | loads ROS and your workspace — one line per terminal |
| `robot/` | the image for the Jetson next to the real arm |
| `tools/` | `latency_test.py`, network measurements between robot and cluster |

The robot model itself (URDF/Xacro, meshes) is not here; it comes from `so_arm101_description` in
[ros2_so_arm](https://github.com/ros-physical-ai/ros2_so_arm).

## Upstream projects

- [ros-physical-ai/ros2_so_arm](https://github.com/ros-physical-ai/ros2_so_arm) — SO-101 model,
  controllers, Gazebo. Our `so_arm101_moveit_config` is derived from its SO-100 MoveIt config.
- [JafarAbdi/feetech_ros2_driver](https://github.com/JafarAbdi/feetech_ros2_driver) — servo driver,
  not available via apt.
- [michaljohnson/cas-so101](https://github.com/michaljohnson/cas-so101) — the full walkthrough
  including preparing and calibrating an arm with LeRobot (lab setup, not needed by students).

**Tested with:** Ubuntu 24.04 laptop · LeRobot v0.6.1 (source, commit `2774d9bd`) · Python 3.12 ·
ROS 2 Jazzy on RAP · `ros2_so_arm` + `feetech_ros2_driver` `main`.
