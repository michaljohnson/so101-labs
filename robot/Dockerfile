# Robot-side image for the SO-101: servo driver + ros2_control, plus MoveIt and
# RViz for local tests. Runs on the Jetson next to the arm; the students' work
# (Gazebo, MoveIt, RViz) runs on RAP.
#
# ros:jazzy-ros-base is published for arm64, so on the Jetson this is a normal
# build, no emulation:   docker build -t cas-so101-robot robot/
FROM ros:jazzy-ros-base

SHELL ["/bin/bash", "-c"]
WORKDIR /ws

# Pin to fixed commits for the course, so an upstream change can't break it mid-term.
ARG SO_ARM_REF=main
ARG FEETECH_REF=main
ARG CAS_REF=main

RUN git clone https://github.com/ros-physical-ai/ros2_so_arm.git src/ros2_so_arm && \
    git -C src/ros2_so_arm checkout "$SO_ARM_REF" && \
    git clone https://github.com/JafarAbdi/feetech_ros2_driver.git src/feetech_ros2_driver && \
    git -C src/feetech_ros2_driver checkout "$FEETECH_REF" && \
    git clone https://github.com/michaljohnson/cas-so101.git src/cas-so101 && \
    git -C src/cas-so101 checkout "$CAS_REF" && \
    touch src/ros2_so_arm/so_arm_gz/COLCON_IGNORE \
          src/ros2_so_arm/so_arm100_description/COLCON_IGNORE

# Only the packages the robot side needs. Skipped: Gazebo (so_arm_gz), the MoveIt
# Setup Assistant and the rqt trajectory GUI, which would pull in a lot for nothing.
# so_arm101_moveit_config exec_depends on so_arm_gz (its gazebo mode), and so_arm_gz on
# so_arm100_description - a COLCON_IGNORE in both (above) hides them from colcon, which
# would otherwise refuse to build the MoveIt config. Its gazebo mode is unusable here,
# mock_components and real are not.
# rmw_zenoh is for the link to RAP later.
ARG PKGS="feetech_ros2_driver so_arm_utils so_arm101_description so_arm101_moveit_config"
RUN apt-get update && rosdep update && \
    rosdep install -y --ignore-src \
      --skip-keys "so_arm_gz moveit_setup_assistant rqt_joint_trajectory_controller" \
      --from-paths src/feetech_ros2_driver src/ros2_so_arm/so_arm_utils \
                   src/ros2_so_arm/so_arm101_description src/cas-so101/so_arm101_moveit_config && \
    apt-get install -y --no-install-recommends ros-jazzy-rmw-zenoh-cpp && \
    rm -rf /var/lib/apt/lists/*

RUN source /opt/ros/jazzy/setup.bash && \
    colcon build --packages-select $PKGS --cmake-args -DCMAKE_BUILD_TYPE=Release && \
    rm -rf build log

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Default: only the driver and controllers (what runs next to the arm in class).
# The arm is expected at /dev/LeRobotFollower, ros2_so_arm's default; run.sh maps it.
CMD ["ros2", "launch", "so_arm101_description", "controllers_bringup.launch.py", "hardware_type:=real"]
