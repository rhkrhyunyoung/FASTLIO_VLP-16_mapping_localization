# FASTLIO_velodyne16_mapping-localization
This repository is a modified version of hku-mars/FAST_LIO (ROS2)
Optimized for broader LiDAR compatibility and localization capabilities.

Removed Livox SDK Dependency: Original FAST_LIO requires Livox drivers even when using Velodyne LiDARs.
This version has been modified to build and run seamlessly using Velodyne drivers only
Without needing the Livox-related environment.

Integrated Localization (ROS2): Ported and integrated the localization feature from FAST_LIO_LOCALIZATION (ROS1) into the ROS2 environment.

# How to Run
1. Mapping

``` ros2 launch fast_lio mapping.launch.py config_file:=velodyne.yaml```
   <img width="1617" height="607" alt="img" src="https://github.com/user-attachments/assets/c800e2be-fe2c-49bc-b3f8-baf85aa3185b" />
2. Save Map(map_file_path is in config/velodyne.yaml)

``` ros2 service call /map_save std_srvs/srv/Trigger {}```
   <img width="416" height="285" alt="image" src="https://github.com/user-attachments/assets/d7cbc202-58b7-4ccb-a1d3-daa8f775e8a8" />
   <img width="405" height="285" alt="image" src="https://github.com/user-attachments/assets/4ad02e13-0f27-49f2-a5c3-edb079f2979b" />

3. Localization

``` ros2 launch fast_lio localization.launch.py map:=/path/to/your/map_result/my_fast_lio_map.pcd```

<img width="472" height="460" alt="image" src="https://github.com/user-attachments/assets/a9c0bc14-c01a-42d6-b417-a379445d696f" />

# Workspace Structure
```lidar_ws/
└── src/
    ├── FAST_LIO/
    ├── velodyne/
    ├── microstrain_inertial/
    └── pcd2pgm/
```

# Configuration Files
Mapping: FAST_LIO/config/velodyne.yaml

Localization: FAST_LIO/config/velodyne_localization.yaml

# TF
![frames_2026-03-13_15 42 59-1_page-0001](https://github.com/user-attachments/assets/1397234c-ee03-4b1b-88f7-780e7f8d0b98)
Global Frame: odom

Local/Body Frame: base_link

For the odom → base_link → sensor_frame structure required by Nav2
The tf structure is organized through localization.yaml modification.

# pcd2pgm
  ros2 launch pcd2pgm pcd2pgm_launch.py
  <img width="833" height="586" alt="image" src="https://github.com/user-attachments/assets/e180e249-a60c-4c7d-b30e-176c1269b154" />

# Nav2
  <img width="683" height="639" alt="image" src="https://github.com/user-attachments/assets/d65a8045-4e80-48d7-916f-6a95006cf193" />
  nav2+localizatioin
<img width="602" height="613" alt="image" src="https://github.com/user-attachments/assets/28be2e0c-30d5-47df-9db9-96253747f7b5" />

# cmd_vel topic
  ros2 topic echo /cmd_vel
  
