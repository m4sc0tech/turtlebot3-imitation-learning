import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist 
import pygame



class PS4TeleopNode(Node):
    def __init__(self):
        super().__init__('ps4_teleop_node')

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        pygame.init()
        pygame.joystick.init()

        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            self.get_logger().error('No joystick detected! Check USB connection.')
            raise RuntimeError('No joystick found')

        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.get_logger().info(f'Connected to: {self.joystick.get_name()}')                  


        self.max_linear_speed = 0.21
        self.max_angular_speed = 2.84


        self.deadzone = 0.1 

        self.timer = self.create_timer(0.05, self.timer_callback)


    def apply_deadzone(self, value):
        """Zero out small stick noise near center."""
        if abs(value) < self.deadzone:
            return 0.0

        sign = 1.0 if value > 0 else -1.0
        return sign * (abs(value) - self.deadzone) / (1.0 - self.deadzone) 

    def timer_callback(self):

        pygame.event.pump()

        raw_linear = -self.joystick.get_axis(1)

        raw_angular = -self.joystick.get_axis(3)

        linear = self.apply_deadzone(raw_linear) * self.max_linear_speed
        angular = self.apply_deadzone(raw_angular) * self.max_angular_speed

        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.publisher_.publish(msg)



def main(args = None):
    rclpy.init(args = args)
    node = PS4TeleopNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:

        stop_msg = Twist()
        node.publisher_.publish(stop_msg)
        rclpy.spin_once(node, timeout_sec = 0.1)
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()



if __name__ == '__main__':
    main()
    
