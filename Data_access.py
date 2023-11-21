import requests
import json
import pandas as pd
from requests.auth import AuthBase
# Code still in progress, tree structure will be soon added.

def main():
    pass

def finance_access(ticker_symbol, start_date, end_date, output_file, cache_filename=None):
    try:
        with open(cache_filename, 'r') as cache_file:
            cached_data = json.load(cache_file)

            if 'symbol' in cached_data and cached_data['symbol'] == ticker_symbol \
                    and cached_data['start_date'] == start_date and cached_data['end_date'] == end_date:
                print(f"Using cached data for {ticker_symbol} from {cache_filename}")
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(cached_data['data'])
                return
    except:
        print("No cache found.")
        pass

    url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker_symbol}?period1={start_date}&period2={end_date}&interval=1d&events=history"
    response = requests.get(url)

    if response.status_code == 200:
        finance_data = response.text
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(finance_data)
        cache_dict = {
            'symbol': ticker_symbol,
            'start_date': start_date,
            'end_date': end_date,
            'data': finance_data
        }
        save_cache(cache_dict, cache_filename)
        print(f"Stock data for {ticker_symbol} saved to {output_file}")
    else:
        print(f"Failed to fetch data for {ticker_symbol}")

class TwitterAuth(AuthBase):
    def __init__(self, bearer_token):
        self.bearer_token = bearer_token

    def __call__(self, r):
        r.headers['Authorization'] = f"Bearer {self.bearer_token}"
        return r

def twitter_access(bearer_token, search_query, output_file, cache_filename, max_tweets=100):
    try:
        with open(cache_filename, 'r') as cache_file:
            cached_data = json.load(cache_file)
            if 'search_query' in cached_data and cached_data['search_query'] == search_query:
                print(f"Using cached tweets for '{search_query}' from {cache_filename}")
                with open(output_file, 'w', encoding='utf-8') as file:
                    json.dump(cached_data['tweet_data'], file, ensure_ascii=False, indent=4)
                return
    except (FileNotFoundError, json.JSONDecodeError):
        print("No cache found.")
        pass

    url = f"https://api.twitter.com/2/tweets/search/recent?query={search_query}&max_results={max_tweets}"
    response = requests.get(url, auth=TwitterAuth(bearer_token))
    if response.status_code == 200:
        tweet_data = response.json()
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(tweet_data, file, ensure_ascii=False, indent=4)

        cache_dict = {
            'search_query': search_query,
            'tweet_data': tweet_data
        }
        save_cache(cache_dict, cache_filename)
        print(f"Tweets based on '{search_query}' saved to {output_file}")
    else:
        print(f"Failed to fetch tweets. Status code: {response.status_code}")


def reddit_access(client_id, client_secret, user_agent, subreddit, output_file, cache_filename, limit=100):
    try:
        with open(cache_filename, 'r') as cache_file:
            cached_data = json.load(cache_file)
            if 'subreddit' in cached_data and cached_data['subreddit'] == subreddit:
                print(f"Using cached Reddit data from r/{subreddit} from {cache_filename}")
                with open(output_file, 'w', encoding='utf-8') as file:
                    json.dump(cached_data['subreddit_data'], file, ensure_ascii=False, indent=4)
                return
    except (FileNotFoundError, json.JSONDecodeError):
        print("No cache found.")
        pass

    auth_url = 'https://www.reddit.com/api/v1/access_token'
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {'grant_type': 'client_credentials'}
    headers = {'User-Agent': user_agent}
    token_response = requests.post(auth_url, auth=auth, data=data, headers=headers)

    if token_response.status_code != 200:
        print(f"Failed to get OAuth token: {token_response.status_code}")
        return

    token = token_response.json()['access_token']
    subreddit_url = f'https://oauth.reddit.com/r/{subreddit}/new'
    headers = {'Authorization': f'Bearer {token}', 'User-Agent': user_agent}
    params = {'limit': limit}
    subreddit_response = requests.get(subreddit_url, headers=headers, params=params)

    if subreddit_response.status_code == 200:
        subreddit_data = subreddit_response.json()
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(subreddit_data, file, ensure_ascii=False, indent=4)

        cache_dict = {
            'subreddit': subreddit,
            'subreddit_data': subreddit_data
        }
        save_cache(cache_dict, cache_filename)

        print(f"Reddit data from r/{subreddit} saved to {output_file}")
    else:
        print(f"Failed to fetch data from r/{subreddit}. Status code: {subreddit_response.status_code}")



def open_cache(cache_filename):
    try:
        with open(cache_filename, 'r') as cache_file:
            cache_contents = json.load(cache_file)
    except (FileNotFoundError, json.JSONDecodeError):
        cache_contents = {}
    return cache_contents

def save_cache(cache_dict, cache_filename):
    with open(cache_filename, "w") as fw:
        json.dump(cache_dict, fw, ensure_ascii=False, indent=4)


def printTree(tree, prefix = '', bend = '', answer = ''):
    text, left, right = tree
    if left is None  and  right is None:
        print(f'{prefix}{bend}{answer} {text}')
    else:
        print(f'{prefix}{bend}{answer}{text}')
        if bend == '+-':
            prefix = prefix + '| '
        elif bend == '`-':
            prefix = prefix + '  '
        printTree(left, prefix, '+-', "former: ")
        printTree(right, prefix, '`-', "latter:  ")

def isAnswer(tree):
    return tree[1:] == (None, None)

def yes(prompt):
    while True:
        ans = input(prompt).lower()
        if ans in ['yes', 'y', 'yup', 'sure']:
            return True
        elif ans in ['no', 'n', 'nope', 'nah']:
            return False
        else:
            print('Please enter "yes" or "no".')

def display(tree):
    pass

if __name__ == "__main__":
    main()