import requests
from bs4 import BeautifulSoup
import hashlib
import json
import time
from datetime import datetime
from random import randint
from typing import List, Dict

class WebCrawler:
    def __init__(self, start_urls: List[str], max_depth: int = 3, delay: float = 1.0):
        self.start_urls = start_urls
        self.max_depth = max_depth
        self.delay = delay
        self.visited_urls = set()
        self.crawl_queue = start_urls.copy()
        self.data = {}

    def crawl(self):
        while self.crawl_queue and len(self.visited_urls) < self.max_depth:
            url = self.crawl_queue.pop(0)
            if url not in self.visited_urls:
                self.visited_urls.add(url)
                try:
                    response = requests.get(url)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    content = soup.get_text()
                    hash_value = hashlib.sha256(content.encode()).hexdigest()
                    self.data[url] = {
                        'content': content,
                        'hash': hash_value,
                        'timestamp': datetime.now().isoformat()
                    }
                    for link in soup.find_all('a'):
                        href = link.get('href')
                        if href and href.startswith('http'):
                            self.crawl_queue.append(href)
                except:
                    pass
                time.sleep(self.delay)

    def save_data(self, filename: str):
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)

if __name__ == '__main__':
    start_urls = ['https://www.example.com', 'https://www.google.com', 'https://www.github.com']
    crawler = WebCrawler(start_urls, max_depth=3, delay=2.0)
    crawler.crawl()
    crawler.save_data('crawl_data.json')