# Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `TypeError: str \| None is not callable` | Python 3.14 | Use the Python 3.12 env, see [arm preparation](https://github.com/michaljohnson/cas-so101) |
| `Permission denied: '/dev/ttyACM0'` | not in `dialout`, or not logged out yet | add yourself to `dialout`, then log out (not lock) |
| Follower doesn't move / wrong arm reacts | ports swapped | `lerobot-find-port` again |
| `Sender has been blocked for over 5 seconds` | Rerun viewer can't keep up | `--display_compressed_images=true` |
| `No module named 'catkin_pkg'` during colcon build | a Python venv/conda env is active | `deactivate` / `conda deactivate`, or use `setup.sh` |
| `CMake Error: The source directory ".../src/<pkg>" does not exist` | the package was moved; colcon's cache in `build/<pkg>` still points to the old place | `rm -rf build/<pkg> install/<pkg>`, then `colcon build` |
| `Package 'so_arm_gz' not found` | workspace not loaded in this terminal | `source ~/rap/cas/setup.sh so101` |
| RViz shows the arm moving, Gazebo doesn't | a second (old) `move_group` or mock `ros2_control_node` gets the commands; `ros2 node list` warns about duplicate names | stop all launches, `ros2 daemon stop`, check `ros2 node list` is empty, relaunch |
| `ros2 node list` shows nodes that aren't running | the ROS 2 daemon caches old nodes | `ros2 daemon stop` |
| Marker in RViz too big / too small | RViz setting | MotionPlanning → Planning Request → *Interactive Marker Size* (course config: 0.08) |
| `rviz2: could not connect to display` / Gazebo doesn't open | no screen (SSH session) | `export DISPLAY=:0` (done by `setup.sh`) or use the web desktop terminal |
| Every new terminal prints `No such file ... setup.bash` | `~/.bashrc` loads `~/env.sh`, which points to a moved workspace | fix or remove the stale line in that `env.sh` |

---
