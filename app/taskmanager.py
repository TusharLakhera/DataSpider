import asyncio
from .scraper import CatalogueScraper
class ScraperTaskManager:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.is_running = False

    async def add_task(self, scraper: CatalogueScraper, page_number: int):
        await self.queue.put((scraper, page_number))
        if not self.is_running:
            self.is_running = True
            asyncio.create_task(self.process_queue())

    async def process_queue(self):
        while not self.queue.empty():
            scraper, page_number = await self.queue.get()
            try:
                await scraper.scrape(page_number)
            finally:
                self.queue.task_done()
        self.is_running = False

scraper_task_manager = ScraperTaskManager()