import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import smach
import smach_ros
from smach_ros import IntrospectionServer
import time

class Searching(smach.State):
    def __init__(self):
        super().__init__(outcomes=['still_searching', 'trying', 'found'])
        self.zero_count = 0

    def execute(self, userdata):
       # node.get_logger().info('Current State: Searching')
        rclpy.spin_once(node)
        twist = node.latest_twist

        if twist:
            if twist.linear.x != 0 or twist.angular.y != 0:
               # node.get_logger().info('Searching: Trying')
                return 'trying'

            if twist.linear.x == 0 and twist.angular.y == 0 and twist.angular.z == 0:
                self.zero_count += 1
                if self.zero_count < 9:
                  #  node.get_logger().info('Searching: still searching')
                    return 'still_searching'
                else:
                  #  node.get_logger().info('Searching: found!')
                    return 'found'
        return 'still_searching'


class WrongWay(smach.State):
    def __init__(self):
        super().__init__(outcomes=['back_to_searching'])

    def execute(self, userdata):
       # node.get_logger().info('Current State: WrongWay')
      #  node.get_logger().info('Wrong Way: back to search')
        time.sleep(1)
        return 'back_to_searching'


class MissionComplete(smach.State):
    def __init__(self):
        super().__init__(outcomes=['end'])

    def execute(self, userdata):
      #  node.get_logger().info('Current State: MissionComplete')
       # node.get_logger().info('Mission Complete: All tasks are done!')
        return 'end'


class CmdVelMonitorNode(Node):
    def __init__(self):
        super().__init__('cmd_vel_monitor')
        self.latest_twist = None
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

    def cmd_vel_callback(self, msg):
        self.latest_twist = msg


# Initialize the ROS node
rclpy.init()
node = CmdVelMonitorNode()

# Create the state machine
sm = smach.StateMachine(outcomes=['end'])

with sm:
    smach.StateMachine.add('SEARCHING', Searching(),
                           transitions={'still_searching': 'WRONG_WAY',
                                        'trying': 'SEARCHING',
                                        'found': 'MISSION_COMPLETE'})
    smach.StateMachine.add('WRONG_WAY', WrongWay(),
                           transitions={'back_to_searching': 'SEARCHING'})
    smach.StateMachine.add('MISSION_COMPLETE', MissionComplete(),
                           transitions={'end': 'end'})

# Create the introspection server
sis = IntrospectionServer('smach_viewer', sm, '/SM_ROOT')
sis.start()

# Execute the state machine
if __name__ == '__main__':
    try:
        sm.execute()
    except KeyboardInterrupt:
        node.get_logger().info('Program interrupted.')
    finally:
        sis.stop()
        rclpy.shutdown()