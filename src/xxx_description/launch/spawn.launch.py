import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import xacro
def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='True')
    world_file_name = 'mai.world'
    pkg_dir = get_package_share_directory('xxx_description')
    world = os.path.join(pkg_dir, 'worlds', world_file_name)


    os.environ["GAZEBO_MODEL_PATH"] = os.path.join(pkg_dir, 'urdf')
    robot_description_path =  os.path.join(pkg_dir,"urdf","xxx.xacro",)
    robot_description = {"robot_description": xacro.process_file(robot_description_path).toxml()}
    
    
    robot_state_publisher_node = Node(package="robot_state_publisher", executable="robot_state_publisher",output="both",parameters=[robot_description],)
    gazebo = ExecuteProcess(cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'],output='screen')
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',arguments=['-topic', robot_description,'-entity', 'coconut'],output='screen')
                        
   
    
    return LaunchDescription([
        gazebo,
        robot_state_publisher_node ,
        spawn_entity,    
    ])