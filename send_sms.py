from twilio.rest import TwilioRestClient

TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''

TO_NUMBER = ''       # Your verified phone number
FROM_NUMBER = ''     # Your Twilio phone number
BODY = 'Hello World' # SMS message

client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
client.sms.messages.create(to=TO_NUMBER, from_=FROM_NUMBER, body=BODY)
