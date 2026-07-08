

# FASTLIO_velodyne16_mapping+localization
This repository presents a robust, ROS2-native solution for LiDAR-based Simultaneous Localization and Mapping (SLAM) and Localization, primarily leveraging the enhanced FAST-LIO algorithm. It is a significant modification and extension of the original hku-mars/FAST_LIO (ROS2) project, with key optimizations for broader LiDAR compatibility and seamless integration with ROS2 Navigation2 (Nav2).

The core objective was to transition a powerful LiDAR odometry and mapping system into a production-ready localization module capable of operating within a pre-built map, while maintaining full compatibility with the Nav2 stack for autonomous navigation.

# KeyFeatures, Enhancemaents
1. Velodyne-Native FAST-LIO Integration (ROS2):

- Dependency Removal: The original FAST_LIO imposed a dependency on Livox SDK, even when utilizing Velodyne LiDARs. This version has been meticulously modified to build and run flawlessly with Velodyne drivers exclusively, eliminating the need for any Livox-specific environment.

- Enhanced Compatibility: Optimized to process standard sensor_msgs/msg/PointCloud2 from Velodyne LiDARs, ensuring broader hardware compatibility.

2. Integrated Localization Capability (ROS2):

- Porting from ROS1: The localization feature, originally found in the ROS1-based FAST_LIO_LOCALIZATION, has been successfully ported and deeply integrated into the ROS2 FAST-LIO framework.

- Map Loading & Relocalization: Enables the system to load a pre-existing PCD map and perform accurate relocalization within that map.

- Dynamic TF Adjustment: Implemented robust logic for initial pose estimation via /initialpose (from RViz2) to align the robot's starting position with the loaded map.

3. ROS2 Navigation2 (Nav2) Full Stack Integration:

- Standardized TF Structure: Crucially, the TF (Transform) tree has been re-architected to conform to the standard map -> odom -> base_link -> sensor_frame hierarchy required by Nav2. This was achieved through significant modifications in laserMapping.cpp and configuration adjustments.

- AMCL Replacement: FAST-LIO now directly provides high-precision localization, effectively replacing AMCL in the Nav2 stack.

- Optimized Costmap Configuration: nav2_params.yaml has been fine-tuned to properly utilize PointCloud2 data from Velodyne LiDARs for local and global costmaps, including aggressive filtering for ground noise and dynamic obstacle avoidance.

4. Gazebo Simulation Environment:

- A custom Gazebo world and a tracked vehicle URDF model (DROK_CK) are provided, allowing for realistic simulation and testing of the SLAM and Localization functionalities.

- Physics Tuning: Extensive work on drok_gazebo.urdf to optimize track friction (mu) and joint limits (max_angular_speed, max_linear_speed), mitigating simulation instabilities like robot shaking and drifting.

# System Architecture & TF Hierarchy
This project implements aNav2-compatible TF tree structureby integrating FAST-LIO's global localization with the robot's local odometry. To prevent the "Multiple Parents" issue in the TF tree, anInverse Transform Calculationlogic was implemented inlaserMapping.cpp.

TF Tree Hierarchy:
- map(Global Frame): Drift-free global reference provided by FAST-LIO.
- odom(Odometry Frame): Smooth, continuous local reference provided by wheel encoders/IMU.
- base_link(Robot Base): The physical center of the robot.
- sensors(vlp16_link,imu_link, etc.): Attached tobase_linkvia static transforms.
<img width="1580" height="690" alt="image" src="https://github.com/user-attachments/assets/dbaa7b4f-2887-4126-8910-07d42acf8056" />

[frames_2026-07-08_16.30.16.pdf](https://github.com/user-attachments/files/29790044/frames_2026-07-08_16.30.16.pdf)

Transformation Logic (Inverse Calculation)
Unlike standard mapping nodes that directly publishodom→base_link, this implementation follows theAMCL-style localization approach:
- Input: FAST-LIO calculates the high-accuracy pose ofmap→base_link.
- Input: The robot's internal system (Wheels/IMU) providesodom→base_link.
- Output: The node calculates and publishes themap→odomtransform using the following inverse logic:
```
T_map_odom = T_map_base * T_odom_base^-1
```
- Benefit: This ensures a single parent forbase_linkwhile allowing Nav2's local planners to use smooth odometry and global planners to use accurate map-based localization.

Nav2 Integration Requirements
- Localization Mode: Enabled vialocalization.yamlto use a pre-built PCD map.
- Global Frame: Set tomapin Nav2 params.
- Robot Base Frame: Set tobase_link.
- Odometry Topic: typically/Odometry(published by FAST-LIO, referenced to themapframe for stability).

# Workspace Structure
```
your_ros2_workspace/
└── src/
    ├── fast_lio/              # Modified FAST-LIO package
    ├── drok_gazebo/           # Custom Gazebo robot model and world
    ├── map/                   # (Optional) Directory for generated maps
    ├── velodyne/              # (Optional) Velodyne ROS2 drivers
    ├── microstrain_inertial/  # (Optional) IMU drivers
    └── pcd2pgm/               # Utility to convert PCD maps to PGM for Nav2
```

# How to Run
1. Mapping

``` ros2 launch fast_lio mapping.launch.py config_file:=velodyne.yaml```
   <img width="1617" height="607" alt="img" src="https://github.com/user-attachments/assets/c800e2be-fe2c-49bc-b3f8-baf85aa3185b" />
   
2. Save Map(map_file_path is in config/velodyne.yaml)

``` ros2 service call /map_save std_srvs/srv/Trigger {}```
   <img width="416" height="285" alt="image" src="https://github.com/user-attachments/assets/d7cbc202-58b7-4ccb-a1d3-daa8f775e8a8" />
   <img width="405" height="285" alt="image" src="https://github.com/user-attachments/assets/4ad02e13-0f27-49f2-a5c3-edb079f2979b" />

3. Localization

``` ros2 launch fast_lio localization.launch.py map:=/path/to/your/map_result/my_fast_lio_map.pcd use_sim_time:=true```

<img width="472" height="460" alt="image" src="https://github.com/user-attachments/assets/a9c0bc14-c01a-42d6-b417-a379445d696f" />

4. Nav2 Stack Integration
``` ros2 launch nav2_bringup navigation_launch.py \
    use_sim_time:=true \
    autostart:=true \
    amcl:=false \
    map:=/path/to/your/2d_map.yaml \
    params_file:=/path/to/my_nav2_params.yaml
```

<img width="683" height="639" alt="image" src="https://github.com/user-attachments/assets/d65a8045-4e80-48d7-916f-6a95006cf193" />
  nav2+localizatioin
<img width="602" height="613" alt="image" src="https://github.com/user-attachments/assets/28be2e0c-30d5-47df-9db9-96253747f7b5" />
<img width="1920" height="1080" alt="스크린샷 2026-05-14 19-10-34" src="https://github.com/user-attachments/assets/97634a6a-3af0-4f15-898a-6171f7e8e262" />

# Configuration Files
Mapping: fast_lio/config/velodyne.yaml

Localization: fast_lio/config/velodyne_localization.yaml

Nav2 Parameters: /path/to/my_nav2_params.yaml (customized for FAST-LIO integration)

Gazebo Robot URDF: drok_gazebo/urdf/drok_gazebo_copy.urdf (or similar name)

<img width="1280" height="720" alt="img1 daumcdn" src="https://github.com/user-attachments/assets/36f29c00-3de7-4ca8-95cc-bb9a26093a02" />

# topics
```
ros2 topic echo /cmd_vel
```
```
ros2 run tf2_ros tf2_echo map base_link
```
