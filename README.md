ros2 version:jazzy
ubuntu version:24.04
webots version:2023b\2024a
robot:kuka youbot
1. Open a terminal in the src directory and enter colcon build
2. Enter the following command source install/local_setup.bash
3. Enter the following command to start the simulation ros2 launch youbot robot_launch.py
4. Open a new terminal in the src directory and enter the following command source install/local_setup.bash. The state machine file is located in the src/smach_for_youbot/smach_for_youbot directory. Enter python3 smach_for_youbot/smach_for_youbot/final.py to open
5. Open a new terminal in the src directory and enter the following command source install/local_setup.bash. Then enter ros2 run smach_viewer smach_viewer_gui.py to start the graphical interface of the state machine


1.在src目录下打开终端并输入colcon build
2.输入以下命令 source install/local_setup.bash
3.输入以下命令以启动模拟 ros2 launch youbot robot_launch.py
4.在src目录下打开一个新的终端，输入以下命令 source install/local_setup.bash。状态机文件位于 src/smach_for_youbot/smach_for_youbot目录。输入 python3 smach_for_youbot/smach_for_youbot/final.py 即可打开
5.在src目录下打开一个新的终端，输入以下命令 source install/local_setup.bash。之后输入 ros2 run smach_viewer smach_viewer_gui.py 以启动状态机的图形界面

