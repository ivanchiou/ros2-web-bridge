#!/usr/bin/python3
import roslibpy
import json
import time
import os
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped

WS_HOST = os.getenv('WS_HOST', 'localhost')
WS_PORT = os.getenv('WS_PORT', '9090')
TOPIC_NAME = os.getenv('TOPIC_NAME', 'clicked_point')
TOPIC_NAME_STRING = os.getenv('TOPIC_NAME_STRING', 'clicked_point_string')
MESSAGE_FORMAT = os.getenv('MESSAGE_FORMAT', 'geometry_msgs/PointStamped')
MESSAGE_FORMAT_STRING = os.getenv('MESSAGE_FORMAT_STRING', 'std_msgs/String')
TIME_PERIOD = os.getenv('TIME_PERIOD', '60')

class NavigationPublisher(Node):
    def __init__(self):
        super().__init__("navigation_node")
        client = roslibpy.Ros(host=WS_HOST, port=int(WS_PORT))
        client.run()

        pub = roslibpy.Topic(client, '/'+TOPIC_NAME_STRING, MESSAGE_FORMAT_STRING)    
        #pub.subscribe(lambda message: print('Heard publisher: {}'.format(message['data'])))

        i = 1
        while client.is_connected:
            x = 0 + i
            y = 0 + i

            msg = PointStamped()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = "navigation"
            msg.point.x = float(x)
            msg.point.y = float(y)
            msg.point.z = 0.
            msg_dict = { 
                'message': {
                    'header': {
                        'seq': 377284,
                        'stamp': {
                            'sec': msg.header.stamp.sec,
                            'nsec': msg.header.stamp.nanosec,
                        },
                        'frame_id': "navigation"
                    },
                    'point': {
                        'x': msg.point.x,
                        'y': msg.point.y,
                        'z': msg.point.z
                    }
                },
                'message_type': MESSAGE_FORMAT,
                'topic_name': TOPIC_NAME
            }
            pub.publish(roslibpy.Message({'data': json.dumps(msg_dict)}))
            print('Sending message...'+str(i)+'...'+json.dumps(msg_dict))
            i = i + 1
            time.sleep(int(TIME_PERIOD))
            #rate.sleep()
    
        pub.unadvertise()
        client.terminate()

if __name__ == '__main__':
    rclpy.init()
    node = NavigationPublisher()
    try:
        rclpy.spin(node)
    except Exception as e:
        print(e)
    node.destroy_node()
    rclpy.shutdown()