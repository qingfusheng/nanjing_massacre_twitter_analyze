import os
import time

import requests
import json

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
  'Accept': '*/*',
  'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
  'x-guest-token': '',
  'x-twitter-client-language': 'zh-cn',
  'x-twitter-active-user': 'yes',
  'x-csrf-token': '25ea9d09196a6ba850201d47d7e75733',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
  'Referer': 'https://twitter.com/',
  'Connection': 'keep-alive',
}
query_string = "nanjingmassacre"
params = [
    ['cursor', ''],
    ['q', query_string],
    ('include_profile_interstitial_type', '1'),
    ('include_blocking', '1'),
    ('include_blocked_by', '1'),
    ('include_followed_by', '1'),
    ('include_want_retweets', '1'),
    ('include_mute_edge', '1'),
    ('include_can_dm', '1'),
    ('include_can_media_tag', '1'),
    ('skip_status', '1'),
    ('cards_platform', 'Web-12'),
    ('include_cards', '1'),
    ('include_ext_alt_text', 'true'),
    ('include_quote_count', 'true'),
    ('include_reply_count', '1'),
    ('tweet_mode', 'extended'),
    ('include_entities', 'true'),
    ('include_user_entities', 'true'),
    ('include_ext_media_color', 'true'),
    ('include_ext_media_availability', 'true'),
    ('send_error_codes', 'true'),
    ('simple_quoted_tweet', 'true'),
    ('tweet_search_mode', 'live'),
    ('count', '20'),
    ('query_source', 'typed_query'),
    ('pc', '1'),
    ('spelling_corrections', '1'),
    ('ext', 'mediaStats,highlightedLabel'),
]

if __name__ == "__main__":
    file_dir = "./filter/"
    tweet_url = 'https://twitter.com/i/api/2/search/adaptive.json'
    url_token = "https://api.twitter.com/1.1/guest/activate.json"
    try:
        os.mkdir(file_dir)
    except Exception as error:
        print(error)
    number = 0
    max_try = 10
    cursor_first = ""
    cursor_current = ""
    while True:
        print("adaptive-"+str(number))
        token = json.loads(requests.post(url_token, headers=headers).text)['guest_token']
        headers["x-guest-token"] = token
        response = requests.get(tweet_url, headers=headers, params=params)
        root = json.loads(response.text)
        tweets = root['globalObjects']['tweets']
        if not tweets:
            max_try -= 1
            cursor_temp = params[0][1]
            params[0][1] = cursor_first
            temp_root = json.loads(requests.get(tweet_url, headers=headers, params=params).text)
            if temp_root['globalObjects']['tweets']:
                params[0][1] = cursor_temp
                continue
            time.sleep(3)
            print("爬取错误，正在进行第"+str(10-max_try)+"次尝试")
            if max_try == 0:
                print("爬虫结束")
                break
            continue
        print(tweets[list(tweets.keys())[0]]["created_at"])
        with open(file_dir+str(number)+".json", "w", encoding="utf-8") as f:
            number += 1
            f.write(response.text)
        Next = root.get('timeline', {}).get('instructions', [])
        if len(Next) > 1:
            if number == 0:
                cursor_first = Next[-1].get('replaceEntry', {}).get('entry', {}).get('content', {}).get('operation', {}).get(
                'cursor', {}).get('value', '')
            params[0][1] = Next[-1].get('replaceEntry', {}).get('entry', {}).get('content', {}).get('operation', {}).get(
                'cursor', {}).get('value', '')
        else:
            if number == 0:
                cursor_first = Next[-1].get('replaceEntry', {}).get('entry', {}).get('content', {}).get('operation', {}).get(
                'cursor', {}).get('value', '')
            params[0][1] = Next[0].get('addEntries', {}).get('entries', [{}])[-1].get('content', {}).get('operation', {}).get(
                'cursor', {}).get('value', '')
        if not params[0][1]:
            params[0][1] = ''
    print("*************************DONE*************************")
    print("共爬取到"+str(number)+"个json文件，每个文件大致含有10~30条数据")
