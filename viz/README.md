# Seeing it from your own laptop

In the pod, Gazebo and RViz run on the noVNC desktop — `setup.sh` sets `DISPLAY=:0` for you.
The alternative is a viewer on your own laptop that connects over a WebSocket. The same approach
works for the simulation and for the real arm.

We use **[Lichtblick](https://github.com/lichtblick-suite/lichtblick)**, an open-source fork of
Foxglove Studio: same protocol, no account, no cloud.

**In the pod:**
```bash
sudo apt install -y ros-jazzy-foxglove-bridge
ros2 launch foxglove_bridge foxglove_bridge_launch.xml port:=8765
```

**On the laptop:**
```bash
kubectl -n <your-namespace> port-forward deploy/rap-deployment 8765:8765
```

**In Lichtblick:** *Open connection* → *Foxglove WebSocket* → `ws://localhost:8765`

**A view worth having:** a **3D** panel with Fixed Frame `world`, the arm from `/robot_description`
and `/tf`; a **Plot** panel on `/joint_states`.

Note that `foxglove_bridge` is installed with `apt` and therefore disappears when the pod restarts,
while your build in `~/rap` stays.
