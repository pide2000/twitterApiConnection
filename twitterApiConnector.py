"""
A Twitter Api Connector
"""

__author__ = 'Peter Bolch'

#!/usr/bin/env python
# encoding: utf-8


import base64
import json
# Doc for rauth: https://rauth.readthedocs.org/en/latest/  and http://requests.readthedocs.org/
import rauth
import requests


class TwitterApiConnector:
    """
    Twitter Api Connection Class
    Provides a simple way to connect to the Twitter Api with your credentials. Visit dev.twitter.com to get the
    credentials to access the api's. With your credentials automatically a bearer token is fetched from the twitter
    api. After this you can access the api's simply with the provided methods.

    Attributes:
        consumer_key:   Twitter Consumer Key
        consumer_secret:    Twitter Consumer Secret
        token_key:  Twitter Token Key
        token_secret: Twitter Token Secret

    Returns:
        A TwitterApiConnection Object
    """

    def __init__(self, consumer_key, consumer_secret, token_key, token_secret):

        self.c_key = consumer_key
        self.c_secret = consumer_secret
        self.t_key = token_key
        self.t_secret = token_secret
        self.bearer_token = self._get_bearer_token()



    # todo: provide possibility to add params to restrict to specific endpoints
    def get_rate_limit(self):
        """
        Get your actual rate limits.

        Returns:
            A python dict with your current rate limits of ALL Endpoints

        """
        session = rauth.OAuth2Session(self.c_key, self.c_secret, access_token=self.bearer_token)
        tweet = session.get('https://api.twitter.com/1.1/application/rate_limit_status.json')
        #print(json.loads(tweet.text))
        print(tweet.request.headers)
        return json.loads(tweet.text)



    def _get_bearer_token(self):
        """
        Gets the bearer token with your credentials

        Returns:
            A bearer token as string
        """
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
                'Authorization': 'Basic ' + str(base64_encoded_bearer_token) + '',
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
        """
        Search for tweets using parameters as specified here: https://dev.twitter.com/docs/api/1.1/get/search/tweets

        Args:
            search_params: A Python Dictionary with the search parameters

        Returns:
            A python dict with search results
        """
        session = rauth.OAuth2Session(self.c_key, self.c_secret, access_token=self.bearer_token)
        tweet = session.get('https://api.twitter.com/1.1/search/tweets.json',
                            params=search_params)
        #print(json.loads(tweet.text))
        return json.loads(tweet.text)

    def get_a_tweet(self, tweet_id):
        """
        Search for a specific tweet by tweet_id

        Args:
            tweet_is: the id of the tweet you want to get

        Returns:
            A python dict with result tweet
        """
        session = rauth.OAuth2Session(self.c_key, self.c_secret, access_token=self.bearer_token)
        tweet = session.get('https://api.twitter.com/1.1/statuses/show.json',
                            params={'id': tweet_id, 'include_entities': 'true'})
        return json.loads(tweet.text)

    #todo: give it a callback possibility to call on every received tweet. Add a callback argument
    def twitter_stream(self):
        """
        gets the twitter stream and prints it on the console

        Args:


        Returns:
            nothing
        """
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

    #todo: give it a callback possibility to call on every received tweet. Add a callback argument
    def filter_stream(self, filter_params={'track': '#killertomatoes'}):
        """
        Filter the twitter stream, filter options from https://dev.twitter.com/docs/api/1.1/post/statuses/filter
        Args:
            filter_params: A Python Dictionary with the filter parameters

        Returns:
            prints the results on the console
        """
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

    CONSUMERKEY = ''
    CONSUMERSECRET = ''
    TOKENKEY = ''
    TOKENSECRET = ''
    #twitter = TwitterApiConnector(CONSUMERKEY, CONSUMERSECRET, TOKENKEY, TOKENSECRET)
    #twitter.grab_stream()
    #print(twitter.get_a_tweet())
    #print(twitter.search_twitter({'q': '#iphone', 'include_entities': 'true'}))
    #'include_entities': 0,
    #'stall_warning': 'true'
    #'track': ''
    #print(twitter.filter_stream())