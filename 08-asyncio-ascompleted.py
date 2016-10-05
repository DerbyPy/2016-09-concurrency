import asyncio
from aiohttp import ClientSession
import requests

errors = []

async def fetch(url, session):
    try:
        async with session.get(url) as response:
            return await response.json()
    except Exception as e:
        errors.append(str(e))


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        return await fetch(url, session)


async def run(loop):
    resp = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
    top_stories = resp.json()
    tasks = []

    # create instance of Semaphore
    sem = asyncio.Semaphore(50)

    # Create client session that will ensure we dont open new connection
    # per each request.
    async with ClientSession() as session:
        for item_id in top_stories:
            url = 'https://hacker-news.firebaseio.com/v0/item/{}.json'.format(item_id)
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url, session))
            tasks.append(task)

        for coroutine in asyncio.as_completed(tasks):
            data = await coroutine
            if data is not None:
                print(data['title'])


loop = asyncio.get_event_loop()

future = asyncio.ensure_future(run(loop))
loop.run_until_complete(future)

for error in errors:
    print(error)