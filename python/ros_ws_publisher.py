import roslibpy
import time
import os

WS_HOST = os.getenv('WS_HOST', 'localhost')
WS_PORT = os.getenv('WS_PORT', '9090')
TOPIC_NAME = os.getenv('TOPIC_NAME', 'example_topic')
TIME_PERIOD = os.getenv('TIME_PERIOD', '1')
DATA_MSG = os.getenv('DATA_MSG', 'Hello World!')

client = roslibpy.Ros(host=WS_HOST, port=WS_PORT)
client.run()
talker = roslibpy.Topic(client, '/'+TOPIC_NAME, 'std_msgs/String')

while client.is_connected:
    talker.publish(roslibpy.Message({'data': DATA_MSG}))
    print('Sending message...')
    time.sleep(int(TIME_PERIOD))

talker.unadvertise()
client.terminate()