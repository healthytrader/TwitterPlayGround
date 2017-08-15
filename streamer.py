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
weatherkey=config.get('weather','key')
headers=headers = {'Authorization': 'Splunk '+splunk_hec}
#This is a basic listener that just prints received tweets to stdout.

def sendtoHEC(mydata):
	print mydata
	mydata={"event":mydata}
	r = requests.post('https://'+splunk_server+':8088/services/collector', data=json.dumps(mydata), headers=headers, verify=False)
	print r

def getWeather(city,state):
	urlstring="http://api.wunderground.com/api/"+weatherkey+"/conditions/q/"+state+"/"+city+".json"
	print urlstring
	r=requests.get(urlstring)
	print r.content
	return r.content
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
	sendtoHEC(data)
	#get location info
	try:
		location=json.loads(data)	
		location=location['place']['full_name']
		print location
		locationarray=location.split(",")
		print locationarray
		weatherinfo = getWeather(locationarray[0].strip(),locationarray[1].strip())
		weatherinfo=json.loads(weatherinfo)
		weatherinfo=weatherinfo['current_observation']
        	print weatherinfo
		sendtoHEC(weatherinfo)
		print location
	except:
		print "no location data"
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
