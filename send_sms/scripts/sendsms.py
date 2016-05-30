from twilio.rest import TwilioRestClient
from syncano.models import Object
import syncano

# Make connection to Syncano
syncano.connect(api_key="SYNCANO_API_KEY")
syncano_instance_name = "ENTER_INSTANCE_NAME_HERE"

# Your Twilio Account Sid and Auth Token from twilio.com/user/account
account_sid = "ENTER_YOUR_ACCOUNT_SID_HERE"
auth_token = "ENTER_YOUR_AUTH_TOKEN_HERE"
client = TwilioRestClient(account_sid, auth_token)  # connect with twilio

message_body = ARGS.get('body', None)  # Arg 'body' is passed to CodeBox
media_url = ARGS.get('media_url', None)  # Arg 'media_url' -- gif, jpeg, or png
to_number = ARGS.get('to_number', None)  # Arg 'to_number' is receiving number, ie; "+13475555717"
if to_number is None:
    raise ValueError("You didn't pass to_number")
elif message_body is None and media_url is None:
    raise ValueError("You didn't pass any 'body' or 'media_url'")
from_number = "+12015552508"  # Replace with your Twilio number or shortcode

message = client.messages.create(body=message_body,
                                 media_url=media_url,
                                 to=to_number,
                                 from_=from_number)
message_sid = message.sid  # id of message for looking up with twilio

# We store the message in syncano
stored_message = Object.please.create(class_name="message",
                                      message=message_body,
                                      image_url=media_url,
                                      message_sid=message_sid,
                                      instance_name=syncano_instance_name)
                                      
                                      
'''
NOTE:
If you are simply trying this out with a free twilio account, make sure you verify the number
that you are testing with. For instance, if you want to send a text to this number 345-555-5555,
verify it by going here https://www.twilio.com/user/account/phone-numbers/verified and then clicking
'Verify a number'
Now your 'to_number' will have a working number that you can message

Also, for 'from_number', you can get one here
https://www.twilio.com/user/account/phone-numbers/incoming
Click 'Buy a number' and you will be able to get a number for free with a trial twilio account

Account SID and auth token can be found on twilio's account page
https://www.twilio.com/user/account/settings

Remember that to do any of this, you will have to sign up for a twilio account.
https://www.twilio.com/try-twilio


# Sample usage in python

from syncano.models.base import *
import syncano

syncano.connect(api_key='ACCOUNT_KEY')
CodeBox.please.run(id='INSTALLED CODEBOX ID',
                   instance_name='INSTANCE_NAME',
                   payload={'to_number':'13475558787', 'body': 'hello there', 'media_url': 'http://www.cat.com/cat.png})

'''