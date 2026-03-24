import asyncio
import random
from typing import List

class DistributedCrawler:
    def __init__(self, nodes: List[str], max_concurrency: int = 100):
        self.nodes = nodes
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def crawl(self, url: str) -> str:
        async with self.semaphore:
            node = random.choice(self.nodes)
            response = await self._fetch_from_node(node, url)
            return response

    async def _fetch_from_node(self, node: str, url: str) -> str:
        # Implement logic to fetch the URL from the specified node
        # This could involve making an HTTP request to the node, or using a distributed protocol like IPFS
        await asyncio.sleep(random.uniform(0.1, 1.0))  # Simulating network delay
        return f'Content from node {node}: {url}'

async def main():
    nodes = ['node1.example.com', 'node2.example.com', 'node3.example.com']
    crawler = DistributedCrawler(nodes)

    urls = ['https://example.com/page1', 'https://example.com/page2', 'https://example.com/page3',
            'https://example.com/page4', 'https://example.com/page5']

    tasks = [crawler.crawl(url) for url in urls]
    results = await asyncio.gather(*tasks)

    for result in results:
        print(result)

if __name__ == '__main__':
    asyncio.run(main())