import requests

resp = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
top_stories = resp.json()
top_50 = top_stories[0:50]

for item_id in top_50:
    url = 'https://hacker-news.firebaseio.com/v0/item/{}.json'.format(item_id)
    resp = requests.get(url)
    story = resp.json()
    print(story['title'])
