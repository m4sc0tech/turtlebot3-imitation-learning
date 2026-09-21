import rclpy
import numpy as np
import joblib
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped


class TurtleBot3Inference(Node):

    def __init__(self):
        super().__init__('turtlebot3_inference')
        bundle = joblib.load('/home/matias/turtlebot3_ws/turtlebot3_model.pkl')
        self.model = bundle['model']
        self.scaler_X = bundle['scaler_X']
        self.scaler_y = bundle['scaler_y']

        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10)
        self.cmd_pub = self.create_publisher(
            TwistStamped, '/cmd_vel', 10)

        self.get_logger().info('Inference node ready.')

    def scan_callback(self, msg):
        ranges = np.array(msg.ranges).reshape(1, -1)
        ranges = np.nan_to_num(ranges, posinf=10.0, neginf=0.0, nan=0.0)

        X_scaled = self.scaler_X.transform(ranges)
        y_scaled = self.model.predict(X_scaled)
        y_pred = self.scaler_y.inverse_transform(y_scaled)

        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = 'turtlebot3_inference'
        cmd.twist.linear.x = float(y_pred[0][0])
        cmd.twist.angular.z = float(y_pred[0][1])
        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleBot3Inference()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
