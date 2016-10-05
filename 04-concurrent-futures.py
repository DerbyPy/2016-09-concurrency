from concurrent.futures import ProcessPoolExecutor, as_completed
from concurrent_demo import URLFetcher

import requests


def fetch_item(item_id):
    try:
        url = 'https://hacker-news.firebaseio.com/v0/item/{}.json'.format(item_id)
        resp = requests.get(url, timeout=2)
        return resp.json()
    except Exception as e:
        pass


class ConcurrentFuturesURLFetcher(URLFetcher):
    concurrency = 50

    def setup_concurrency(self):
        self.pool = ProcessPoolExecutor(self.concurrency)
        self.futures = []

    def load_stories(self, item_ids):
        for item_id in item_ids:
            future = self.pool.submit(fetch_item, item_id)
            self.futures.append(future)

    def process_stories(self):
        for future in as_completed(self.futures):
            story = future.result()
            if story is not None:
                self.process_item(story)


ConcurrentFuturesURLFetcher().run()
