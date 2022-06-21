import requests
from urllib import parse
import json
import time

url = "https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q={}&count=20&query_source=typed_query&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2CvoiceInfo&cursor={}"
url_token = 'https://api.twitter.com/1.1/guest/activate.json'
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
q = '(from:{}) until:{} since:{}'


def formate_time2time_stamp(time_):
    return int(time.mktime(time.strptime(time_, "%Y-%m-%d")))


def time_stamp2formate_time(time_):
    return time.strftime("%Y-%m-%d", time.localtime(int(time_)))


def q_list_get(from_, since, until):
    since_p = formate_time2time_stamp(since)
    until_p = formate_time2time_stamp(until)
    step = 60 * 60 * 24
    while (since_p < until_p):
        next = since_p + step
        yield q.format(from_, time_stamp2formate_time(next), time_stamp2formate_time(since_p))
        since_p = next


def get_token():
    token = json.loads(requests.post(url_token, headers=headers).text)['guest_token']
    headers['x-guest-token'] = token


if __name__ == "__main__":
    from_ = 'twitter'  # 用户名
    since = '2020-01-01'  # 开始时间
    until = '2021-01-01'  # 结束时间

    num = 0
    tweet_list = []
    get_token()
    for q_ in q_list_get(from_, since, until):
        print(q_)
        print("********************8888")
        try:
            cursor = ''
            while True:
                if num > 500:
                    get_token()
                    num = 0
                num += 1

                res = requests.get(url.format(parse.quote(q_), parse.quote(cursor)), headers=headers)
                with open("adaptive.json", "w", encoding="utf-8") as f:
                    f.write(res.text)
                root = json.loads(res.text)
                tweets = root['globalObjects']['tweets']
                if not tweets:
                    break
                for i in tweets.values():
                    tweet_list.append(i['full_text'])
                    # print(i['full_text'])

                next = root.get('timeline', {}).get('instructions', [])
                print(next)
                print(len(next))
                if len(next) > 1:
                    cursor = next[-1].get('replaceEntry', {}).get('entry', {}).get('content', {}).get('operation',{}).get('cursor', {}).get('value', '')
                    print("len(next) > 1", cursor)
                else:
                    cursor = next[0].get('addEntries', {}).get('entries', [{}])[-1].get('content', {}).get('operation',{}).get('cursor', {}).get('value', '')
                    print("len(next) == 1", cursor)
                if not cursor:
                    cursor = ''
            exit()
        except Exception as e:
            print(e)

    with open('out.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(tweet_list, ensure_ascii=False))