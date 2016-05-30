import analytics

# merge POST and GET ARGS
GET = ARGS.get("GET",{})
POST = ARGS.get("POST",{})
ARGS.update(GET)
ARGS.update(POST)

# replace with your own segment write key
write_key = "fdslkgjdlksfg"

# set your own write key on the segment analytics
analytics.write_key = write_key

# extract user and event you'd like to track
user_id = ARGS.get("user_id",None)
event_name = ARGS.get("event_name", None)

# send event to segment
analytics.track(user_id, event_name)

# empties the queue and sends event immediately
analytics.flush()

'''
You can run this directly or you can use a webhook in this format

https://api.syncano.io//v1/instances/<instance_name>/webhooks/p/<public link>/
'''