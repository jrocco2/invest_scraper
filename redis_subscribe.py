import redis
import time

r = redis.StrictRedis()
p = r.pubsub()
p.subscribe('economic_calendar')
p.subscribe('earning_calendar')
p.subscribe('market_news')

print("Waiting for updates from 'economic_calendar', 'earning_calendar', 'market_news'")
while True:
     message = p.get_message()
     if message:
             print(str(message['data']))
     time.sleep(0.001)