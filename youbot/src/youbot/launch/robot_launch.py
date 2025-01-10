import os
import launch
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.webots_controller import WebotsController


def generate_launch_description():
    package_dir = get_package_share_directory('youbot')
    robot_description_path = os.path.join(package_dir, 'resource', 'youbot.urdf')

    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'youbot.wbt')
    )

    kuka_youbot_driver = WebotsController(
        robot_name='youBot',
        parameters=[
            {'robot_description': robot_description_path},
        ]
    )

    return LaunchDescription([
        webots,
        kuka_youbot_driver,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ])