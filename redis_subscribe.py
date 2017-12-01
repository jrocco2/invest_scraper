import redis
import time

r = redis.StrictRedis()
p = r.pubsub()
p.subscribe('economic_calendar')

print("Waiting for updates from 'economic_calendar'")
while True:
     message = p.get_message()
     if message:
             print(str(message['data']))
     time.sleep(0.001)