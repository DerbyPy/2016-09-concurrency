from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent_demo import URLFetcher


class ConcurrentFuturesURLFetcher(URLFetcher):
    def setup_concurrency(self):
        self.pool = ThreadPoolExecutor(self.concurrency)
        self.futures = []

    def load_stories(self, item_ids):
        for item_id in item_ids:
            future = self.pool.submit(self.fetch_item, item_id)
            self.futures.append(future)

    def process_stories(self):
        for future in as_completed(self.futures):
            story = future.result()
            if story is not None:
                self.process_item(story)


ConcurrentFuturesURLFetcher().run()
