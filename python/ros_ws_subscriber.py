from __future__ import print_function
import roslibpy
import os

WS_HOST = os.getenv('WS_HOST', 'localhost')
WS_PORT = os.getenv('WS_PORT', '9090')
TOPIC_NAME = os.getenv('TOPIC_NAME', 'example_topic')

client = roslibpy.Ros(host=WS_HOST, port=int(WS_PORT))
client.run()

listener = roslibpy.Topic(client, '/'+TOPIC_NAME, 'std_msgs/String')
listener.subscribe(lambda message: print('Heard publisher: ' + message['data']))

try:
    while True:
        pass
except KeyboardInterrupt:
    client.terminate()