ros2 version:jazzy
ubuntu version:24.04
webots version:2023b\2024a
robot:kuka youbot
1. Open a terminal in the src directory and type colcon build.
2. Copy the protos folder in the src/youbot directory to src/install/youbot/share/youbot
3. Enter the following command：source install/local_setup.bash
4. Enter the following command to start the simulation: ros2 launch youbot robot_launch.py
5. Could use teleop_keyboard to control the robot movement.
6. Use the following command to view the camera data：ros2 topic echo /camera/image_color
7. Open a new terminal in the src directory and enter the following command source install/local_setup.bash. The state machine file is located in the src/smach_for_youbot/smach_for_youbot directory. Enter python3 smach_for_youbot/smach_for_youbot/smach_search.py ​​to open it
8. Open a new terminal in the src directory and enter the following command source install/local_setup.bash. Then enter ros2 run smach_viewer smach_viewer_gui.py to start the graphical interface of the state machine
9. Open a new terminal in the src directory and enter sh topic.sh to run the script. This script allows the robot to run along the predetermined route and eventually run under the table. You can see the different states of the robot during operation from the graphical page of the state machine.

1.在src目录下打开终端并输入colcon build
2.将位于src/youbot目录下的protos文件夹复制到 youbot/src/install/youbot/share/youbot
3.输入以下命令 source install/local_setup.bash
4.输入以下命令以启动模拟 ros2 launch youbot robot_launch.py
5.可以使用teleop_keyboard控制机器人移动
6.输入以下命令以查看摄像头数据 ros2 topic echo /camera/image_color
7.在src目录下打开一个新的终端，输入以下命令 source install/local_setup.bash。状态机文件位于 src/smach_for_youbot/smach_for_youbot目录。输入 python3 smach_for_youbot/smach_for_youbot/smach_search.py 即可打开
8.在src目录下打开一个新的终端，输入以下命令 source install/local_setup.bash。之后输入 ros2 run smach_viewer smach_viewer_gui.py 以启动状态机的图形界面
9.在src目录下打开一个新的终端，输入 sh topic.sh 即可运行脚本，这个脚本可以让机器人按照既定的路线运行，最终运行至桌子底下。您可以从状态机的图形页面看到机器人在运行时出现的不同状态。
