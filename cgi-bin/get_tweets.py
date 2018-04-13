from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas as pd

consumer_key = "RG9fMy5hJmWKq67MGtpo5788d"
consumer_secret = "tvoUhIqxryMDq3vtrQq4mDRQAB0UbSb2wvsN0FBErrZ8k5A8Vd"
access_token = "824278184-NBgqJkudyWcO5TC7lLFeTwzJPnaPvUQ4gnONrody"
access_secret = "VfhqUndZfwmjb5CSClQST9yuapuiZwDMyepWvhR6IjDvt"

data_array = []

class StdOutListener(StreamListener):

	def on_data(self, data):
		data = json.loads(data)
		if not data['is_quote_status'] and not data['in_reply_to_status_id']:
			data_array.append((data['id_str'], data['text']))
			# if len(data['text'].split()) < 12:
			print data['text']
		return True

	def on_error(self, status):
		print status


if __name__ == "__main__":

	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	stream = Stream(auth, l)

	stream.filter(track=['forgiveness'])

	# path = './data/hello_tweets.txt'

	# data = []
	# f = open(path, 'r')
	# for line in f:
	# 	try:
	# 		tweet = json.loads(line)
	# 		data.append(tweet)
	# 	except:
	# 		continue