__author__ = 'Peter Bolch'

#!/usr/bin/env python
# encoding: utf-8
"""
* 	Twitter Api Connection Class
*   provides so far connections to the following services offered by twitter:
*   ratelimit
*   get a bearer token
*   search
*   get a tweet by id
*   twitter streaming api
*   filter streaming api
"""

import base64
import json
# Doc for rauth: https://rauth.readthedocs.org/en/latest/  and http://requests.readthedocs.org/
import rauth
import requests


class TwitterApiConnector:

    def __init__(self, consumer_key, consumer_secret, token_key, token_secret):
        self.c_key = consumer_key
        self.c_secret = consumer_secret
        self.t_key = token_key
        self.t_secret = token_secret
        self.bearer_token = self._get_bearer_token()

    def get_rate_limit(self):
        session = rauth.OAuth2Session(self.c_key, self.c_secret, access_token=self.bearer_token)
        tweet = session.get('https://api.twitter.com/1.1/application/rate_limit_status.json')
        #print(json.loads(tweet.text))
        print(tweet.request.headers)
        return json.loads(tweet.text)

    def _get_bearer_token(self):
        service = rauth.OAuth2Service(name='Peters App',
                                      client_id=self.c_key,
                                      client_secret=self.c_secret,
                                      access_token_url='https://api.twitter.com/oauth2/token')

        bearer_raw = service.get_raw_access_token(
            params={'grant_type': 'client_credentials', 'Content-Length': '29', 'Accept-Encoding': 'gzip'})
        bearer = json.loads(bearer_raw.content)
        bearer_t = bearer['access_token']
        #print(bearer_t)
        return bearer_t

    # todo: this possibly doesnt work. dont know why
    def invalidate_bearer_token(self):
        temp_token = self.c_key + ':' + self.c_secret
        # base64 encode the token
        base64_encoded_bearer_token = base64.b64encode(temp_token)
        para = {'Host': 'api.twitter.com',
                'User-Agent': 'something',
                'Authorization': 'Basic ' + base64_encoded_bearer_token + '',
                'Accept': '*/*',
                'Content-Type': 'application/x-www-form-urlencoded'
        }
        datat = 'access_token=' + self.bearer_token
        r = requests.post('https://api.twitter.com/oauth2/invalidate_token', data=datat, headers=para)
        print("header")
        print(r.request.headers)
        print(r.request.body)
        print(r.text)

    def search_twitter(self, search_params):
        session = rauth.OAuth2Session(self.c_key, self.c_secret, access_token=self.bearer_token)
        tweet = session.get('https://api.twitter.com/1.1/search/tweets.json',
                            params=search_params)
        #print(json.loads(tweet.text))
        return json.loads(tweet.text)

    def get_a_tweet(self, tweet_id):
        session = rauth.OAuth2Session(self.c_key, self.c_secret, access_token=self.bearer_token)
        tweet = session.get('https://api.twitter.com/1.1/statuses/show.json',
                            params={'id': tweet_id, 'include_entities': 'true'})
        return json.loads(tweet.text)

    def twitter_stream(self):
        url = "https://stream.twitter.com/1.1/statuses/sample.json"

        session = rauth.OAuth1Session(self.c_key, self.c_secret, self.t_key, self.t_secret)

        while True:
            t = session.get(url, stream=True)
            try:
                for line in t.iter_lines():
                    # filter out keep-alive new lines

                    if line:
                        print(json.loads(line))
            except KeyboardInterrupt:
                print('End')
                continue
            except:
                print('an error occured')
                raise

    def filter_stream(self, filter_params={}):
        url = "https://stream.twitter.com/1.1/statuses/filter.json"
        session = rauth.OAuth1Session(self.c_key, self.c_secret, self.t_key, self.t_secret)

        while True:
            t = session.post(url, stream=True, data=filter_params)
            print(t.request.body)
            try:
                for line in t.iter_lines():
                    if line:
                        print(json.loads(line))
            except KeyboardInterrupt:
                print('End')
                #continue
            except:
                print('an error occured')
                raise

if __name__ == '__main__':

    CONSUMERKEY = 'tvsYifyhgSBZXZKAw89Pw'
    CONSUMERSECRET = 'Ilhf89DeJoVZCbsv8h3lVGJ4ad03FQJNHMF0UFQNo'
    TOKENKEY = '905717030-oDPf2iSbUhMH2bS7eccJT92zSKzGlpIoMC5Jthou'
    TOKENSECRET = '62iqak9Sshg3q6rEIm1Ed9AQ7eCONX95rPtLkp817DI'
    twitter = TwitterApiConnector(CONSUMERKEY, CONSUMERSECRET, TOKENKEY, TOKENSECRET)
    #twitter.grab_stream()
    print(twitter.get_a_tweet(383598356075122688))
    print(twitter.search_twitter({'q': '#iphone', 'include_entities': 'true'}))