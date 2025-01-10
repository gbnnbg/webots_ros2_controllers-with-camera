import rclpy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray

class Kuka_Youbot_Driver:
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot

        # 初始化电机
        self.__right_foward_motor = self.__robot.getDevice('wheel1')
        self.__left_foward_motor = self.__robot.getDevice('wheel2')
        self.__right_back_motor = self.__robot.getDevice('wheel3')
        self.__left_back_motor = self.__robot.getDevice('wheel4')
        self.__camera = self.__robot.getDevice('camera')

        self.__camera.enable(100)
        self.__camera.recognitionEnable(100)  # 启用物体识别功能

        self.__right_foward_motor.setPosition(float('inf'))
        self.__right_foward_motor.setVelocity(0)

        self.__left_foward_motor.setPosition(float('inf'))
        self.__left_foward_motor.setVelocity(0)

        self.__right_back_motor.setPosition(float('inf'))
        self.__right_back_motor.setVelocity(0)

        self.__left_back_motor.setPosition(float('inf'))
        self.__left_back_motor.setVelocity(0)


        self.__arm1 = self.__robot.getDevice("arm1")
        self.__arm2 = self.__robot.getDevice("arm2")
        self.__arm3 = self.__robot.getDevice("arm3")
        self.__arm4 = self.__robot.getDevice("arm4")
        self.__arm5 = self.__robot.getDevice("arm5")
        self.__finger_left = self.__robot.getDevice("finger_left")
        self.__finger_right = self.__robot.getDevice("finger_right")

        self.__arm1sensor = self.__robot.getDevice("arm1sensor")
        self.__arm2sensor = self.__robot.getDevice("arm2sensor")
        self.__arm3sensor = self.__robot.getDevice("arm3sensor")
        self.__arm4sensor = self.__robot.getDevice("arm4sensor")
        self.__arm5sensor = self.__robot.getDevice("arm5sensor")

        self.__arm5sensor.enable(100)
        self.__arm4sensor.enable(100)
        self.__arm3sensor.enable(100)
        self.__arm2sensor.enable(100)
        self.__arm1sensor.enable(100)


        # 初始化距离传感器
        self.__ds_L = self.__robot.getDevice('ds_L')
        self.__ds_R = self.__robot.getDevice('ds_R')
        self.__ds_L.enable(100)
        self.__ds_R.enable(100)

        rclpy.init(args=None)
        self.__node = rclpy.create_node('Kuka_Youbot_Driver')
        # self.__node.create_subscription(Twist, 'cmd_vel', self.__cmd_vel_callback, 1)
        self.__robot_speed_publisher = self.__create_robot_speed_publisher
        self.__arm_position_publisher = self.__create_arm_position_publisher

        # 速度限制
        self.__max_speed = 14.0  # 设置速度上限

    def __create_robot_speed_publisher(self, forward_speed, angular_speed):
     """
     创建并发布机器人速度信息
     """
     msg = Float32MultiArray()
     msg.data = [forward_speed, angular_speed]  # 通过参数接收速度数据
    
     # 创建发布器
     publisher = self.__node.create_publisher(Float32MultiArray, 'robot_speed', 1)
     publisher.publish(msg)

    def __create_arm_position_publisher(self):
        """
     创建并发布机械臂关节位置信息
      """
        msg = Float32MultiArray()
        positions = [
          self.__arm1sensor.getValue(),
          self.__arm2sensor.getValue(),
          self.__arm3sensor.getValue(),
          self.__arm4sensor.getValue(),
          self.__arm5sensor.getValue(),
        ]
        msg.data = positions
    
    # 创建发布器
        publisher = self.__node.create_publisher(Float32MultiArray, 'arm_position', 1)
        publisher.publish(msg)


    # def __cmd_vel_callback(self, twist):
    #     self.__target_twist = twist

    def activate_arm(self):


        self.__arm1.setPosition(0.2)
        self.__arm2.setPosition(-0.7)
        self.__arm3.setPosition(-0.7)
        self.__arm4.setPosition(-0.3)
        self.__arm5.setPosition(0.0)
        self.__finger_left.setPosition(0.025)
        self.__finger_right.setPosition(0.025)

        start_time = self.__robot.getTime()
        while self.__robot.getTime() - start_time < 2:
            self.__robot.step(100)

        self.__finger_left.setVelocity(0.05)
        self.__finger_left.setPosition(0.0)
        self.__finger_right.setVelocity(0.05)
        self.__finger_right.setPosition(0.0)

        start_time = self.__robot.getTime()
        while self.__robot.getTime() - start_time < 2:
            self.__robot.step(100)

        self.__arm1.setPosition(0.0)
        self.__arm2.setPosition(0.0)
        self.__arm3.setPosition(0.0)
        self.__arm4.setPosition(0.0)
        self.__arm5.setPosition(0.0)

        start_time = self.__robot.getTime()
        while self.__robot.getTime() - start_time < 2:
            self.__robot.step(100)

        # positonvalue1 = self.__arm1sensor.getValue()
        # positonvalue2 = self.__arm2sensor.getValue()
        # positonvalue3 = self.__arm3sensor.getValue()
        # positonvalue4 = self.__arm4sensor.getValue()
        # positonvalue5 = self.__arm5sensor.getValue()

        # print(f"Current position: {positonvalue1}")
        # print(f"Current position: {positonvalue2}")
        # print(f"Current position: {positonvalue3}")
        # print(f"Current position: {positonvalue4}")
        # print(f"Current position: {positonvalue5}")

        self.__arm_position_publisher()
        

    def limit_speed(self, speed):
        """
        限制速度在 [-self.__max_speed, self.__max_speed] 范围内
        """
        return max(-self.__max_speed, min(self.__max_speed, speed))

    def set_motor_velocity(self, forward_speed, angular_speed, turn_speed):
        """
        设置电机速度，确保速度受上限约束
        """
        # 限制输入速度
        forward_speed = self.limit_speed(forward_speed)
        angular_speed = self.limit_speed(angular_speed)
        turn_speed = self.limit_speed(turn_speed)

        s = 0.158
        d = 0.228

        command_motor_left_foward = forward_speed + angular_speed - (d + s) * turn_speed
        command_motor_right_foward = forward_speed - angular_speed + (d + s) * turn_speed
        command_motor_left_back = forward_speed - angular_speed - (d + s) * turn_speed
        command_motor_right_back = forward_speed + angular_speed + (d + s) * turn_speed

        # 限制各轮速度
        command_motor_left_foward = self.limit_speed(command_motor_left_foward)
        command_motor_right_foward = self.limit_speed(command_motor_right_foward)
        command_motor_left_back = self.limit_speed(command_motor_left_back)
        command_motor_right_back = self.limit_speed(command_motor_right_back)

        # 设置电机速度
        self.__right_foward_motor.setVelocity(command_motor_right_foward)
        self.__left_foward_motor.setVelocity(command_motor_left_foward)
        self.__right_back_motor.setVelocity(command_motor_right_back)
        self.__left_back_motor.setVelocity(command_motor_left_back)

        self.__robot_speed_publisher(forward_speed, angular_speed)

    def step(self):
        rclpy.spin_once(self.__node, timeout_sec=0)

        # 障碍物检测
        left_distance = self.__ds_L.getValue()
        right_distance = self.__ds_R.getValue()

        if right_distance < 930:
            # 右侧有障碍
            forward_speed = 0
            angular_speed = -10
            self.set_motor_velocity(forward_speed, angular_speed, 0)
            self.__robot.step(2000)  # 转1秒
            return  # 提前返回，规避障碍物后继续下一步
        elif left_distance < 930:
            # 左侧有障碍
            forward_speed = 0
            angular_speed = 10
            self.set_motor_velocity(forward_speed, angular_speed, 0)
            self.__robot.step(2000)  # 转1秒
            return  # 提前返回，规避障碍物后继续下一步

        # 摄像头识别
        objects = self.__camera.getRecognitionObjects()

        if objects:
            # 仅处理第一个物体
            obj = objects[0]
            obj_id = obj.getId()
            obj_size = obj.getSize()
            obj_position = obj.getPosition()  # 获取相对摄像头的位置

            obj_size_list = list(obj_size)
            obj_position_list = list(obj_position)

            # 打印物体信息
            print(f"Object ID: {obj_id}")
            print(f"Object Size: {obj_size_list}")
            print(f"Object Position (relative): {obj_position_list}")

            # 提取物体的相对位置
            x, y, _ = obj_position

            # 目标位置为 x=0.5, y=0
            target_x = 0.41
            target_y = 0.1

            # 计算位置偏差
            error_x = -(target_x - x)
            error_y = -(target_y - y)

            # 控制机器人运动
            if math.fabs(error_x) > 0.01 or math.fabs(error_y) > 0.01:  # 容忍误差范围
                forward_speed = error_x * 10  # 调整前进速度
                angular_speed = -error_y * 10  # 调整角速度
                self.set_motor_velocity(forward_speed, angular_speed, 0)
            else:
                # 如果抵达目标位置，则停止机器人
                self.set_motor_velocity(0, 0, 0)
                print("Target reached. Robot stopped.")
                self.activate_arm()
        else:
            # 如果未检测到物体，停止机器人
            self.set_motor_velocity(0, 0, 0)
            print("No object detected. Robot stopped.")
