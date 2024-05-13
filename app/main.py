from fastapi import FastAPI, Depends
from typing import List
from .models import Product
from fastapi import FastAPI, Depends
from typing import List
import redis
from .models import Product
from .scraper import CatalogueScraper
from .storage import JSONStorage
from .authentication import authenticate
from .notification import ConsoleNotification
from .cache import RedisCache

app = FastAPI()

# Create a Redis client
redis_client = redis.Redis(host='redis', port=6379, db=0)

@app.get("/scrape", dependencies=[Depends(authenticate)], response_model=List[Product])
async def scrape_products(max_pages: int = None, proxy: str = None):
    storage = JSONStorage("data/products.json")
    notification = ConsoleNotification()
    cache = RedisCache(redis_client)
    scraper = CatalogueScraper(base_url="https://dentalstall.com/shop", max_pages=max_pages, proxy=proxy, storage=storage, notification=notification, cache=cache)
    products = scraper.scrape()
    return products