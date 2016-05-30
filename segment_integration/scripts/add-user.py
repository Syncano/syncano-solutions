import analytics

# replace with your own segment write key
write_key = "ISJSFKGJDSLKJ"

# set your own write key on the segment analytics
analytics.write_key = write_key

# extract user id
user_id = ARGS.get("owner", None)

# add user through segment
analytics.identify(user_id)

# empties the queue and sends the call immediately
analytics.flush()

'''
This will execute whenever you add a new user to syncano
You can see this Trigger set up in the 'Tasks' tab in the
nav bar
'''