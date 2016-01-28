from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
ACCOUNT_SID = "AC349af1c35e0c14a3c1f3333dc3b06925" 
AUTH_TOKEN = "bfb3ee950a5dd94ccd238f244a31f2c5" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
client.messages.create(
    to="+19735344648", 
    from_="+15187206160", 
    body="I sent this text from my computer, how cool is that??!"
)
    #media_url="http://farm2.static.flickr.com/1075/1404618563_3ed9a44a3a.jpg", 