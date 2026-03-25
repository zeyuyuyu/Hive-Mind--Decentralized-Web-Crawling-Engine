import asyncio
import aiohttp
from collections import deque
from typing import Deque, Set, Dict

class DistributedTaskScheduler:
    def __init__(self, num_workers: int):
        self.num_workers = num_workers
        self.task_queue: Deque[str] = deque()
        self.in_progress: Set[str] = set()
        self.results: Dict[str, str] = {}

    async def add_task(self, url: str):
        self.task_queue.append(url)
        await self.schedule_tasks()

    async def schedule_tasks(self):
        while len(self.in_progress) < self.num_workers and self.task_queue:
            url = self.task_queue.popleft()
            self.in_progress.add(url)
            asyncio.create_task(self.process_task(url))

    async def process_task(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
                self.results[url] = content
        self.in_progress.remove(url)
        await self.schedule_tasks()

    async def run(self):
        await asyncio.gather(*[self.schedule_tasks() for _ in range(self.num_workers)])
        return self.results

if __:
    scheduler = DistributedTaskScheduler(num_workers=10)
    urls = ['https://example.com', 'https://google.com', 'https://github.com']
    for url in urls:
        asyncio.create_task(scheduler.add_task(url))
    results = asyncio.run(scheduler.run())
    for url, content in results.items():
        print(f'URL: {url}, Content: {content[:100]}...')