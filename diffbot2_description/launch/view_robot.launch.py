#!/usr/bin/env python3
#
# Copyright 2020 Open BR
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Get rviz config
    rviz_config = PathJoinSubstitution([
        FindPackageShare('diffbot2_description'), 'rviz/view_robot.rviz'
    ])

    spawn_launch = PathJoinSubstitution([
        FindPackageShare('diffbot2_description'), 'launch/spawn_robot.launch.py'
    ])

    spawn_robot = LaunchConfiguration('spawn_robot')
    namespace = LaunchConfiguration('namespace')

    spawn_robot_arg = DeclareLaunchArgument(
                        name='spawn_robot',
                        default_value='false',
                        description='Flag to spawn the robot or not')

    namespace_arg = DeclareLaunchArgument(
                        name='namespace',
                        default_value='',
                        description='Node namespace')

    # OBS: do not add rviz2 as dependency because it is heavy
    rviz_node = Node(
                    package='rviz2',
                    executable='rviz2',
                    name='rviz',
                    output='screen',
                    namespace=namespace,
                    arguments=['-d', rviz_config])

    spawn_launch_cmd = IncludeLaunchDescription(
                        PythonLaunchDescriptionSource(spawn_launch),
                        condition=IfCondition(spawn_robot))

    launch_description = LaunchDescription()

    launch_description.add_action(spawn_robot_arg)
    launch_description.add_action(namespace_arg)
    launch_description.add_action(rviz_node)
    launch_description.add_action(spawn_launch_cmd)

    return launch_description
