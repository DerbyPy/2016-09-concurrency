import json
from tornado import ioloop, httpclient

from concurrent_demo import URLFetcher


class TornadoURLFetcher(URLFetcher):

    def setup_concurrency(self):
        self.http_client = httpclient.AsyncHTTPClient()
        self.responses_seen = 0

    def load_stories(self, item_ids):
        self.items_loaded = len(item_ids)
        print(self.items_loaded)
        self.requests = []
        for item_id in item_ids:
            url = 'https://hacker-news.firebaseio.com/v0/item/{}.json'.format(item_id)
            self.http_client.fetch(url, self.handle_response, method='GET')
        ioloop.IOLoop.instance().start()

    def handle_response(self, response):
        self.responses_seen += 1
        if self.responses_seen == self.items_loaded:
            ioloop.IOLoop.instance().stop()
        if response.body is None:
            self.errors.append(str(response.error))
        else:
            item_data = json.loads(response.body.decode('utf-8'))
            self.process_item(item_data)


TornadoURLFetcher().run()
