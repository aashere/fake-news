import json
import pandas as pd

def parse_query(response):
    extracted_tweet_data = []
    extracted_user_data = []

    res_count = response['response']['meta']['result_count']
    if res_count == 0:
        return None
    tweet_list = response['response']['data']
    user_list = response['response']['includes']['users']

    for tweet_dict in tweet_list:

        tweet_data_dict = {
            'article_id': None,
            'tweet_id': None,
            'tweet_body': None,
            'post_timestamp': None,
            'post_location': None,
            'conversation_id': None,
            'retweet_count': None,
            'reply_count': None,
            'like_count': None,
            'quote_count': None,
            'user_id': None
        }

        tweet_data_dict['article_id'] = response['id']
        if 'id' in tweet_dict:
            tweet_data_dict['tweet_id'] = tweet_dict['id']
        if 'text' in tweet_dict:
            tweet_data_dict['tweet_body'] = tweet_dict['text']
        if 'created_at' in tweet_dict:
            tweet_data_dict['post_timestamp'] = tweet_dict['created_at']
        if 'geo' in tweet_dict:
            tweet_data_dict['post_location'] = tweet_dict['geo']
        if 'conversation_id' in tweet_dict:
            tweet_data_dict['conversation_id'] = tweet_dict['conversation_id'] 
        if 'author_id' in tweet_dict:
            tweet_data_dict['user_id'] = tweet_dict['author_id']      
        if 'public_metrics' in tweet_dict:
            if 'retweet_count' in tweet_dict['public_metrics']:
                tweet_data_dict['retweet_count'] = tweet_dict['public_metrics']['retweet_count']
            if 'reply_count' in tweet_dict['public_metrics']:
                tweet_data_dict['reply_count'] = tweet_dict['public_metrics']['reply_count']
            if 'like_count' in tweet_dict['public_metrics']:
                tweet_data_dict['like_count'] = tweet_dict['public_metrics']['like_count']
            if 'quote_count' in tweet_dict['public_metrics']:
                tweet_data_dict['quote_count'] = tweet_dict['public_metrics']['quote_count']

        extracted_tweet_data.append(tweet_data_dict)

    for user_dict in user_list:
        user_data_dict = {
            'user_id': None,
            'user_timestamp': None,
            'user_nickname': None,
            'username': None,
            'user_location': None,
            'user_followers': None,
            'user_following': None,
            'user_tweet_count': None,
            'user_listed_count': None
        }

        if 'id' in user_dict:
            user_data_dict['user_id'] = user_dict['id']
        if 'name' in user_dict:
            user_data_dict['user_nickname'] = user_dict['name']
        if 'username' in user_dict:
            user_data_dict['username'] = user_dict['username']
        if 'created_at' in user_dict:
            user_data_dict['user_timestamp'] = user_dict['created_at']
        if 'location' in user_dict:
            user_data_dict['user_location'] = user_dict['location']
        if 'public_metrics' in user_dict:
            if 'followers_count' in user_dict['public_metrics']:
                user_data_dict['user_followers'] = user_dict['public_metrics']['followers_count']
            if 'following_count' in user_dict['public_metrics']:
                user_data_dict['user_following'] = user_dict['public_metrics']['following_count']
            if 'tweet_count' in user_dict['public_metrics']:
                user_data_dict['user_tweet_count'] = user_dict['public_metrics']['tweet_count']
            if 'listed_count' in user_dict['public_metrics']:
                user_data_dict['user_listed_count'] = user_dict['public_metrics']['listed_count']
        extracted_user_data.append(user_data_dict)
    
    tweet_df = pd.DataFrame(extracted_tweet_data)
    user_df = pd.DataFrame(extracted_user_data)

    return tweet_df.merge(user_df, how='left', on='user_id')
    
def parse_user_response(response):
    extracted_user_data = []

    user_list = response['response']['data']

    for user_dict in user_list:
        user_data_dict = {
            'user_id': None,
            'user_timestamp': None,
            'user_location': None,
            'user_followers': None,
            'user_following': None,
            'user_tweet_count': None,
            'user_listed_count': None
        }

        if 'id' in user_dict:
            user_data_dict['user_id'] = user_dict['id']
        if 'created_at' in user_dict:
            user_data_dict['user_timestamp'] = user_dict['created_at']
        if 'location' in user_dict:
            user_data_dict['user_location'] = user_dict['location']
        if 'public_metrics' in user_dict:
            if 'followers_count' in user_dict['public_metrics']:
                user_data_dict['user_followers'] = user_dict['public_metrics']['followers_count']
            if 'following_count' in user_dict['public_metrics']:
                user_data_dict['user_following'] = user_dict['public_metrics']['following_count']
            if 'tweet_count' in user_dict['public_metrics']:
                user_data_dict['user_tweet_count'] = user_dict['public_metrics']['tweet_count']
            if 'listed_count' in user_dict['public_metrics']:
                user_data_dict['user_listed_count'] = user_dict['public_metrics']['listed_count']
        extracted_user_data.append(user_data_dict)

    user_df = pd.DataFrame(extracted_user_data)

    return user_df