#!/usr/bin/env python3
"""Put one object into Gazebo and into MoveIt's planning scene, from one set of numbers.

Gazebo gives the object physics, MoveIt gives it collision geometry. Neither tells the
other, so an object spawned by hand exists only for the one that knows about it: MoveIt
plans straight through a Gazebo-only object, and there is nothing to grasp for an
RViz-only one. This spawns both at the same pose.

Run it with the workspace sourced, while the sim and MoveIt are up:

  python3 spawn_object.py cube                          # 4 cm cube at x=0.18
  python3 spawn_object.py pen --shape cylinder --size 0.004 0.14 --xyz 0.18 0 0.002
  python3 spawn_object.py cube --scene-only             # no physics: see MoveIt avoid it

The arm stands at the world origin and reaches towards +x, so x = 0.15..0.20, y = 0 is
in front of it. Gazebo's world frame and MoveIt's `base_link` coincide there, which is
why the same numbers work for both.
"""
import argparse
import subprocess
import sys

import rclpy
from moveit_msgs.msg import CollisionObject, PlanningScene
from rclpy.node import Node
from shape_msgs.msg import SolidPrimitive

SDF = """<?xml version="1.0"?>
<sdf version="1.9">
  <model name="{name}">
    <pose>{x} {y} {z} 0 0 0</pose>
    <link name="link">
      <inertial>
        <mass>{mass}</mass>
        <inertia><ixx>{i}</ixx><iyy>{i}</iyy><izz>{i}</izz>
                 <ixy>0</ixy><ixz>0</ixz><iyz>0</iyz></inertia>
      </inertial>
      <collision name="collision">
        <geometry>{geom}</geometry>
        <surface><friction><ode><mu>{mu}</mu><mu2>{mu}</mu2></ode></friction></surface>
      </collision>
      <visual name="visual">
        <geometry>{geom}</geometry>
        <material><diffuse>0.1 0.4 0.9 1</diffuse></material>
      </visual>
    </link>
  </model>
</sdf>
"""


def geometry(shape, size):
    """SDF geometry plus the matching MoveIt primitive."""
    if shape == "box":
        primitive = SolidPrimitive(type=SolidPrimitive.BOX, dimensions=list(size))
        return f"<box><size>{size[0]} {size[1]} {size[2]}</size></box>", primitive
    radius, length = size[0], size[1]
    primitive = SolidPrimitive(type=SolidPrimitive.CYLINDER, dimensions=[length, radius])
    return f"<cylinder><radius>{radius}</radius><length>{length}</length></cylinder>", primitive


def spawn_in_gazebo(name, sdf):
    """ros_gz_sim's create node takes the model as a string, like the arm's own spawn."""
    result = subprocess.run(
        ["ros2", "run", "ros_gz_sim", "create", "-name", name, "-string", sdf],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.exit(f"Gazebo spawn failed:\n{result.stdout}{result.stderr}")


def add_to_planning_scene(name, frame, xyz, primitive):
    rclpy.init()
    node = Node("spawn_object")
    publisher = node.create_publisher(PlanningScene, "/planning_scene", 10)

    obj = CollisionObject(id=name, operation=CollisionObject.ADD)
    obj.header.frame_id = frame
    obj.primitives = [primitive]
    obj.primitive_poses = [_pose(xyz)]

    scene = PlanningScene(is_diff=True)
    scene.world.collision_objects = [obj]

    # move_group has to be subscribed before the diff goes out, or it is lost.
    for _ in range(50):
        if publisher.get_subscription_count() > 0:
            break
        rclpy.spin_once(node, timeout_sec=0.1)
    else:
        node.get_logger().warn("nobody subscribed to /planning_scene — is move_group running?")

    publisher.publish(scene)
    rclpy.spin_once(node, timeout_sec=0.5)
    node.destroy_node()
    rclpy.shutdown()


def _pose(xyz):
    from geometry_msgs.msg import Pose

    pose = Pose()
    pose.position.x, pose.position.y, pose.position.z = xyz
    pose.orientation.w = 1.0
    return pose


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("name")
    parser.add_argument("--shape", choices=["box", "cylinder"], default="box")
    parser.add_argument("--size", type=float, nargs="+", default=[0.04, 0.04, 0.04],
                        help="box: x y z — cylinder: radius length")
    parser.add_argument("--xyz", type=float, nargs=3, default=[0.18, 0.0, 0.02],
                        help="centre of the object; z is half its height to stand on the ground")
    parser.add_argument("--mass", type=float, default=0.02)
    parser.add_argument("--mu", type=float, default=1.5, help="friction; grasps in Gazebo need a lot of it")
    parser.add_argument("--frame", default="base_link", help="MoveIt planning frame")
    parser.add_argument("--scene-only", action="store_true", help="MoveIt only, no physics object")
    parser.add_argument("--gazebo-only", action="store_true", help="physics only, invisible to MoveIt")
    args = parser.parse_args()

    expected = 3 if args.shape == "box" else 2
    if len(args.size) != expected:
        sys.exit(f"--size needs {expected} values for a {args.shape}")

    geom, primitive = geometry(args.shape, args.size)

    if not args.scene_only:
        x, y, z = args.xyz
        inertia = args.mass * max(args.size) ** 2 / 6
        spawn_in_gazebo(args.name, SDF.format(name=args.name, x=x, y=y, z=z, mass=args.mass,
                                              i=inertia, geom=geom, mu=args.mu))
        print(f"Gazebo: {args.name} at {args.xyz}")

    if not args.gazebo_only:
        add_to_planning_scene(args.name, args.frame, args.xyz, primitive)
        print(f"MoveIt: {args.name} in frame {args.frame}")


if __name__ == "__main__":
    main()
