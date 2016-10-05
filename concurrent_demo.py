import requests


class URLFetcher():
    max_stories = 500
    concurrency = 200
    requests_timeout = 2

    def __init__(self):
        self.errors = []

    def run(self):
        self.setup_concurrency()

        resp = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
        top_stories = resp.json()
        trimmed_stories = top_stories[0:self.max_stories]

        self.load_stories(trimmed_stories)
        self.process_stories()
        self.print_errors()

    def process_stories(self):
        pass

    def print_errors(self):
        print('Errors')
        for error in self.errors:
            print(error)

    def fetch_item(self, item_id):
        try:
            url = 'https://hacker-news.firebaseio.com/v0/item/{}.json'.format(item_id)
            resp = requests.get(url, timeout=self.requests_timeout)
            return resp.json()
        except Exception as e:
            self.errors.append((item_id, str(e)))

    def process_item(self, data):
        print(data['title'])
