# Lab 2 — MoveIt and picking (session 8)

Status: `mock_components` ✅ · `gazebo` ✅ (plan & execute moves the arm in Gazebo) ·
marker dragging ✅ (*Approx IK Solutions*, preset in the course RViz config) · `real` 🚧

`ros2_so_arm` ships a MoveIt config for the SO-100 only, but its helper code already
expects an `so_arm101_moveit_config` package. The course provides that package,
adapted from the SO-100 one:

- same joint names, planning group `manipulator`, gripper group `gripper`;
- planning tip `gripper_frame_link` — the point between the fingers, handy for picking;
- named poses `zero`, `extended`, `rest`, `open`, `closed`, kept inside the SO-101 limits;
- `demo.launch.py` with `hardware_type:=mock_components | gazebo | real`.
  For Gazebo it reuses `so_arm_gz` (the SO-101 controller launch in `ros2_so_arm`
  has no Gazebo mode) and adds the gripper controller.

Only the **follower** arm is needed for MoveIt; the leader is just for teleoperation.

## Build

The package comes with this repo, so the build in lab 1 already includes it.

## Run it

Stop any Gazebo that is still running (Ctrl+C) first.

```bash
# fastest check: MoveIt + RViz, no physics
ros2 launch so_arm101_moveit_config demo.launch.py hardware_type:=mock_components

# with Gazebo
ros2 launch so_arm101_moveit_config demo.launch.py hardware_type:=gazebo
```

In RViz, drag the marker at the gripper, then *Plan & Execute* in the MotionPlanning
panel. Or pick a named pose under *Goal State* (e.g. `extended`) and execute.

The SO-101 has 5 joints, so most combinations of gripper position *and* tilt are
unreachable and exact IK fails while dragging the marker. The course RViz config
therefore ticks *Approx IK Solutions* (Planning tab): the goal follows the marker as
closely as the arm allows. This only affects RViz — in your own code, MoveIt still
tries to reach the exact pose you ask for, so choose poses the arm can reach
(e.g. gripper pointing down, turned towards the object). Named poses always work.

## Pick an object in simulation 🚧

Start the Gazebo demo above and add objects in Gazebo with the **Resource Spawner**
(Gazebo menu ⋮ top right → *Resource Spawner*). Where things are: the arm stands on
the ground at the world origin and reaches towards **+x** (e.g. an object at
x = 0.2, y = 0 on the floor is in reach). MoveIt plans in the same `world` frame, so
Gazebo and MoveIt coordinates are identical. (`so_arm_gz` has `x/y/z` launch arguments,
but the SO-101 model ignores them.)

Pick it by hand in RViz — for each step choose the planning group and goal, then
*Plan & Execute*:

1. group `gripper` → `open`
2. group `manipulator` → marker ~5 cm above the object, gripper pointing down
3. marker straight down, jaws around the object
4. group `gripper` → `closed`
5. group `manipulator` → up: does the object come along?

Objects added in Gazebo are **not** in MoveIt's planning scene: RViz doesn't show them
and MoveIt plans as if they weren't there. To add one by hand: MotionPlanning panel →
*Scene Objects* → pick a shape, set the same size and x/y/z as in Gazebo (select the
object in Gazebo → *Component Inspector* → Pose). In code, adding the object to the
planning scene and attaching it to the gripper (with the allowed touch links) is part
of the pick lab.

---
