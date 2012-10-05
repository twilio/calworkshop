from twilio.rest import TwilioRestClient

TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''

TO_NUMBER = ''       # Your verified phone number
FROM_NUMBER = ''     # Your Twilio phone number
TWIML_URL = 'http://twimlets.com/message?Message=Hello+World'

client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
client.calls.create(to=TO_NUMBER, from_=FROM_NUMBER, url=TWIML_URL)

