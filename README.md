ros2 version:jazzy
ubuntu version:24.04
webots version:2023b\2024a
1.Open a terminal in the src directory and type colcon build.
2.Copy the protos folder into this directory..../youbot/src/install/youbot/share/youbot
3.Enter the following command：source install/local_setup.bash
4.Enter the following command to start the simulation: ros2 launch youbot robot_launch.py
5.Use teleop_keyboard to control the robot movement.
6.Use the following command to view the camera data：ros2 topic echo /camera/image_color


1.在src目录下打开终端并输入colcon build
2.将protos文件夹复制到..../youbot/src/install/youbot/share/youbot
3.输入以下命令install/local_setup.bash
4.输入以下命令以启动模拟ros2 launch youbot robot_launch.py
5.使用teleop_keyboard控制机器人移动
6.输入以下命令以查看摄像头数据ros2 topic echo /camera/image_color
