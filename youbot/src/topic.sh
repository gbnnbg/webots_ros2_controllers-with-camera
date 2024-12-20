ros2 topic pub /cmd_vel geometry_msgs/Twist  "linear: { x: 5 }" -t 10
ros2 topic pub /cmd_vel geometry_msgs/Twist  "linear: { x: 0 }" -t 2
ros2 topic pub /cmd_vel geometry_msgs/Twist '{linear: {x: 0, y: 0, z: 0}, angular: {x: 0, y: 14, z: 0}}' -t 1
ros2 topic pub /cmd_vel geometry_msgs/Twist  "linear: { x: 0 }" -t 2
ros2 topic pub /cmd_vel geometry_msgs/Twist  "linear: { x: 10 }" -t 7
ros2 topic pub /cmd_vel geometry_msgs/Twist  "linear: { x: 0 }" -t 2
ros2 topic pub /cmd_vel geometry_msgs/Twist '{linear: {x: 0, y: 0, z: 0}, angular: {x: 0, y: -8, z: 0}}' -t 3
ros2 topic pub /cmd_vel geometry_msgs/Twist  "linear: { x: 0 }" -t 2
ros2 topic pub /cmd_vel geometry_msgs/Twist  "linear: { x: 3 }" -t 5
ros2 topic pub /cmd_vel geometry_msgs/Twist  "linear: { x: 0 }" -t 1
