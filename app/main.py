from typing import Optional
from fastapi import FastAPI, Depends, BackgroundTasks
import redis
from .scraper import CatalogueScraper
from .storage import JSONStorage
from .authentication import authenticate
from .notification import ConsoleNotification
from .cache import RedisCache
from .taskmanager import scraper_task_manager
app = FastAPI()

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.post("/scrape", dependencies=[Depends(authenticate)])
async def scrape_products(max_pages: Optional[int] = None, proxy: Optional[str] = None):
    storage = JSONStorage("data/products.json")
    notification = ConsoleNotification()
    cache = RedisCache(redis_client)
    scraper = CatalogueScraper(base_url="https://dentalstall.com/shop", max_pages=max_pages, proxy=proxy, storage=storage, notification=notification, cache=cache)
    
    total_pages = 119
    pages_to_scrape = min(total_pages, max_pages) if max_pages else total_pages

    for page in range(1, pages_to_scrape + 1):
        print(f"Queuing scraping job for page {page}")
        await scraper_task_manager.add_task(scraper, page)

    return {"message": f"Scraping job for {pages_to_scrape} pages has been queued and will be processed in the background."}
