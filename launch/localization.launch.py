import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # 1. 경로 설정
    package_path = get_package_share_directory('fast_lio')
    default_config_path = os.path.join(package_path, 'config')
    default_rviz_config_path = os.path.join(package_path, 'rviz', 'fastlio.rviz')
    
    # URDF 파일 경로 (사용자님 시스템의 절대 경로)
    urdf_file_path = '/home/ams7725/yunjae/Gazebo/DROK_CK/src/drok_gazebo/urdf/drok_gazebo.urdf'
    
    # 2. URDF 파일 읽기
    if os.path.exists(urdf_file_path):
        with open(urdf_file_path, 'r') as infp:
            robot_desc = infp.read()
    else:
        robot_desc = ""
        print("Warning: URDF file not found at", urdf_file_path)

    # 3. 인자 정의 (명칭을 'map'으로 통일)
    map_path = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time')

    declare_map_cmd = DeclareLaunchArgument(
        'map',
        default_value='/home/ams7725/yunjae/maps/map.pcd',
        description='Full path to the PCD map file'
    )
    
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time', 
        default_value='false',
        description='Use simulation clock if true'
    )

    # 4. 노드 설정
    # FAST-LIO 노드
    fast_lio_node = Node(
        package='fast_lio',
        executable='fastlio_mapping',
        name='fastlio_mapping',
        parameters=[
            os.path.join(default_config_path, 'velodyne_localization.yaml'),
            {'pcd_path': map_path, 'use_sim_time': use_sim_time}
        ],
        output='screen'
    )

    # Robot State Publisher (로봇 모델 표시)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'robot_description': robot_desc, 'use_sim_time': use_sim_time}]
    )

    # Joint State Publisher
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # RViz2 노드
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', default_rviz_config_path],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # Static TF: base_link -> velodyne (YAML의 extrinsic_T: [0, 0, 0.04] 반영)
    static_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_base_to_lidar',
        arguments=['0', '0', '0.04', '0', '0', '0', '1', 'base_link', 'velodyne']
    )

    return LaunchDescription([
        declare_map_cmd,
        declare_use_sim_time_cmd,
        fast_lio_node,
        rviz_node,
        robot_state_publisher_node,
        joint_state_publisher_node,
        static_tf_node
    ])
