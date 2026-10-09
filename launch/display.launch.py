import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('robot_diferencial_pkg')
    urdf_path = os.path.join(pkg_share, 'urdf', 'robot.urdf.xacro')
    
    # NUEVO: Ruta al archivo de configuración de RViz
    rviz_config_path = os.path.join(pkg_share, 'config', 'visor.rviz')

    robot_description_content = Command(['xacro ', urdf_path])
    
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content}]
    )

    node_joint_state_publisher = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen'
    )

    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path] # NUEVO: Cargar configuración
    )

    return LaunchDescription([
        node_robot_state_publisher,
        node_joint_state_publisher,
        node_rviz
    ])