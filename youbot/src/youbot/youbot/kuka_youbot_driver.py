import rclpy
from geometry_msgs.msg import Twist


class Kuka_Youbot_Driver:
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot

        self.__right_foward_motor = self.__robot.getDevice('wheel1')
        self.__left_foward_motor = self.__robot.getDevice('wheel2')
        self.__right_back_motor = self.__robot.getDevice('wheel3')
        self.__left_back_motor = self.__robot.getDevice('wheel4')
        self.__camera = self.__robot.getDevice('camera')

        self.__camera.enable(100)
        self.__camera.getImage
        

        self.__right_foward_motor.setPosition(float('inf'))
        self.__right_foward_motor.setVelocity(0)

        self.__left_foward_motor.setPosition(float('inf'))
        self.__left_foward_motor.setVelocity(0)

        self.__right_back_motor.setPosition(float('inf'))
        self.__right_back_motor.setVelocity(0)

        self.__left_back_motor.setPosition(float('inf'))
        self.__left_back_motor.setVelocity(0)


        self.__target_twist = Twist()

        rclpy.init(args=None)
        self.__node = rclpy.create_node('Kuka_Youbot_Driver')
        self.__node.create_subscription(Twist, 'cmd_vel', self.__cmd_vel_callback, 1)

    def __cmd_vel_callback(self, twist):
        self.__target_twist = twist

    def step(self):
        rclpy.spin_once(self.__node, timeout_sec=0)

        forward_speed = self.__target_twist.linear.x
        angular_speed = self.__target_twist.angular.z

        command_motor_left_foward = forward_speed + angular_speed 
        command_motor_right_foward = forward_speed - angular_speed
        command_motor_left_back = forward_speed - angular_speed
        command_motor_right_back = forward_speed + angular_speed

        self.__right_foward_motor.setVelocity(command_motor_right_foward)
        self.__left_foward_motor.setVelocity(command_motor_left_foward)
        self.__right_back_motor.setVelocity(command_motor_right_back)
        self.__left_back_motor.setVelocity(command_motor_left_back)