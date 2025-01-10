import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import smach
import smach_ros

# State definitions
class Ready(smach.State):
    def __init__(self, node):
        smach.State.__init__(self, outcomes=['to_searching'])
        self.node = node

    def execute(self, userdata):
        while rclpy.ok():
            rclpy.spin_once(self.node)
            # 检查 robot_speed 的前进速度是否不为 0
            if self.node.robot_speed[0] != 0:
                return 'to_searching'
            # 如果条件未满足，继续等待，避免状态返回 None
        return None


class Searching(smach.State):
    def __init__(self, node):
        smach.State.__init__(self, outcomes=['to_terrain', 'to_pullup', 'to_searching'])
        self.node = node

    def execute(self, userdata):
        rclpy.spin_once(self.node)
        forward_speed, angular_speed = self.node.robot_speed
        if forward_speed == 0 and angular_speed in [10, -10]:
            return 'to_terrain'
        elif forward_speed == 0 and angular_speed == 0:
            return 'to_pullup'
        elif forward_speed != 0:
            return 'to_searching'


class Terrain(smach.State):
    def __init__(self, node):
        smach.State.__init__(self, outcomes=['to_searching'])
        self.node = node

    def execute(self, userdata):
        rclpy.spin_once(self.node)
        if self.node.robot_speed[0] != 0:
            return 'to_searching'


class PullUp(smach.State):
    def __init__(self, node):
        smach.State.__init__(self, outcomes=['to_mission_complete'])
        self.node = node

    def execute(self, userdata):
        rclpy.spin_once(self.node)
        if self.node.arm_position:
            return 'to_mission_complete'


class MissionComplete(smach.State):
    def __init__(self, node):
        smach.State.__init__(self, outcomes=[])
        self.node = node

    def execute(self, userdata):
        self.node.get_logger().info("Mission complete!")
        return None


# Node definition
class RobotStateMachine(Node):
    def __init__(self):
        super().__init__('robot_state_machine')

        # Subscribers
        self.create_subscription(Float32MultiArray, 'robot_speed', self.robot_speed_callback, 10)
        self.create_subscription(Float32MultiArray, 'arm_position', self.arm_position_callback, 10)

        # Shared variables
        self.robot_speed = [0.0, 0.0]  # Initialize with default values
        self.arm_position = []  # Initialize as empty list

    def robot_speed_callback(self, msg):
        self.robot_speed = msg.data

    def arm_position_callback(self, msg):
        self.arm_position = msg.data


# Main state machine setup
def main():
    rclpy.init()
    node = RobotStateMachine()

    sm = smach.StateMachine(outcomes=[])
    with sm:
        smach.StateMachine.add('READY', Ready(node), transitions={'to_searching': 'SEARCHING'})
        smach.StateMachine.add('SEARCHING', Searching(node), transitions={'to_terrain': 'TERRAIN',
                                                                          'to_pullup': 'PULLUP',
                                                                          'to_searching': 'SEARCHING'})
        smach.StateMachine.add('TERRAIN', Terrain(node), transitions={'to_searching': 'SEARCHING'})
        smach.StateMachine.add('PULLUP', PullUp(node), transitions={'to_mission_complete': 'MISSION_COMPLETE'})
        smach.StateMachine.add('MISSION_COMPLETE', MissionComplete(node), transitions={})

    # SMACH introspection server for visualization
    sis = smach_ros.IntrospectionServer('smach_server', sm, '/SM_ROOT')
    sis.start()

    try:
        # Execute SMACH plan
        sm.execute()
    except KeyboardInterrupt:
        node.get_logger().info("State Machine interrupted.")
    finally:
        sis.stop()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
