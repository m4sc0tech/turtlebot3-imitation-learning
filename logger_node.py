
import rclpy
import message_filters
from . import csv_writer
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class TurtleBot3Logger(Node):

    def __init__(self):
        super().__init__('turtlebot3_logger')
        self.csv_file, self.csv_writer = csv_writer.open_csv_file(
        'turtlebot3_data.csv'
    )
        scan_sub = message_filters.Subscriber(self, LaserScan, '/scan')
        cmd_vel_sub = message_filters.Subscriber(self, Twist, '/cmd_vel')

        self.ts = message_filters.ApproximateTimeSynchronizer(
        [scan_sub, cmd_vel_sub],
        queue_size=10,
        slop=0.1
        allow_headerless=True
    )
        self.ts.registerCallback(self.sync_callback)

    def sync_callback(self, scan_msg, cmd_vel_msg):
        """Handle a synchronized pair of LaserScan and Twist messages."""
        timestamp = self.get_clock().now().to_msg()
        ranges = scan_msg.ranges
        linear_x = cmd_vel_msg.linear.x
        angular_z = cmd_vel_msg.angular.z

        row = [timestamp.sec, timestamp.nanosec] + list(ranges) + \
            [linear_x, angular_z]
        self.csv_writer.writerow(row)

def main(args=None):
    rclpy.init(args=args)
    node = TurtleBot3Logger()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.csv_file.close()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()      






