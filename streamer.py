#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import requests
import json
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('mytwitter.cfg')
#Variables that contains the user credentials to access Twitter API 
access_token = config.get('TwitterCodes','accesstoken')
access_token_secret = config.get('TwitterCodes','accesstokensecret')
consumer_key = config.get('TwitterCodes','consumerkey')
consumer_secret = config.get('TwitterCodes','consumerkeysecret')
splunk_server=config.get('Splunk','server')
splunk_hec=config.get('Splunk','HECToken')
headers=headers = {'Authorization': 'Splunk '+splunk_hec}
#This is a basic listener that just prints received tweets to stdout.

def sendtoHEC(mydata):
	print mydata
	mydata={"event":mydata}
	r = requests.post('https://'+splunk_server+':8088/services/collector', data=json.dumps(mydata), headers=headers, verify=False)
	print r
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
	sendtoHEC(data)
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    #stream.filter(track=['python', 'javascript', 'ruby'])
    stream.filter(follow=['724335346826113024'])
