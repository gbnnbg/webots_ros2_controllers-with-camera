import rclpy
from rclpy.node import Node
import time
import smach
import smach_ros

class SmachTestNode(Node):
    def __init__(self, name):
        super().__init__(name)
        self.get_logger().info("启动 demo 节点")

# 定义状态 Foo
class Foo(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])
        self.counter = 0

    def execute(self, userdata):
        print('Executing state FOO')
        time.sleep(2)
        if self.counter < 10:
            self.counter += 1
            return 'outcome1'
        else:
            return 'outcome2'

# 定义状态 Bar
class Bar(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome2'])

    def execute(self, userdata):
        print('Executing state BAR')
        time.sleep(2)
        return 'outcome2'

# main
def main(args=None):
    rclpy.init(args=args) # 初始化 ros
    node = SmachTestNode("execute_smach_test")

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['outcome4', 'outcome5'])

    # Open the container
    with sm:
    # Add states to the container
        smach.StateMachine.add('FOO', Foo(), 
            transitions={'outcome1':'BAR', 'outcome2':'outcome4'})
        smach.StateMachine.add('BAR', Bar(), 
            transitions={'outcome2':'FOO'})

    # Create and start the introspection server
    sis = smach_ros.IntrospectionServer('my_smach_introspection_server', sm, '/SM_ROOT')
    sis.start()

    # Execute SMACH plan
    outcome = sm.execute()

    # Wait for ctrl-c to stop the application
    rclpy.spin(node)
    sis.stop()

if __name__ == '__main__':
    main()
