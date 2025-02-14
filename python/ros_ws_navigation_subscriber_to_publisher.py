#!/usr/bin/python3
import roslibpy
import os
import json
from datetime import datetime
import rclpy
from rclpy.node import Node
from std_msgs.msg import Header
from geometry_msgs.msg import PointStamped, Point, Pose

WS_HOST = os.getenv('WS_HOST', 'localhost')
WS_PORT = os.getenv('WS_PORT', '9090')
TOPIC_NAME_STRING = os.getenv('TOPIC_NAME_STRING', 'clicked_point_string')
MESSAGE_FORMAT_STRING = os.getenv('MESSAGE_FORMAT_STRING', 'std_msgs/String')
TIME_PERIOD = os.getenv('TIME_PERIOD', '60')

class NavigationSubscriber(Node):
    def __init__(self):
        super().__init__("navigation_node")
        client = roslibpy.Ros(host=WS_HOST, port=int(WS_PORT))
        client.run()
        pub = roslibpy.Topic(client, '/'+TOPIC_NAME_STRING, MESSAGE_FORMAT_STRING, queue_size=10)    
        pub.subscribe(self.on_message)

    def on_message(self, msg):
        print('Heard publisher: {}'.format(msg['data']))

        data = json.loads(msg['data'])
        message = data['message']

        self.publisher = self.create_publisher(
            PointStamped,
            '/'+data['topic_name'],
            1)

        print(str(message))

        msg = PointStamped()
        header = message['header']
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = header['frame_id']
        point = message['point']
        msg.point = Point()
        msg.point.x = point['x']
        msg.point.y = point['y']
        msg.point.z = point['z']

        self.publisher.publish(msg)

if __name__ == '__main__':
    rclpy.init()
    node = NavigationSubscriber()
    try:
        rclpy.spin(node)
    except Exception as e:
        print(e)
    node.destroy_node()
    rclpy.shutdown()