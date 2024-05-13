import json
import requests
import time
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from typing import List, Dict
from .storage import Storage
from .notification import Notification
from .cache import Cache

class Scraper(ABC):
    def __init__(self, base_url: str, max_pages: int = None, proxy: str = None, storage: Storage = None, notification: Notification = None, cache: Cache = None):
        self.base_url = base_url
        self.max_pages = max_pages
        self.proxy = proxy
        self.storage = storage
        self.notification = notification
        self.cache = cache

    @abstractmethod
    def scrape(self) -> List[Dict]:
        pass

class CatalogueScraper(Scraper):
    def scrape(self) -> List[Dict]:
        products = []
        page_count = 1

        while True:
            if page_count == 1:
                url = self.base_url
            else:
                url = f"{self.base_url}/page/{page_count}/"

            response = self._fetch_page(url)

            if response is None or (self.max_pages and page_count > self.max_pages):
                break

            soup = BeautifulSoup(response.content, "html.parser")
            product_elements = soup.select("ul.products li.product")

            for product_element in product_elements:
                product_image = product_element.select_one("a > img")
                product_title = product_image["alt"].split(" - ")[0] if product_image else ""

                price_element = product_element.select_one("span.price bdi")
                if price_element:
                    price_text = price_element.text.strip().replace("₹", "").replace(",", "")
                    if "Starting at:" in price_text:
                        price_text = price_text.split("Starting at:")[1].strip()
                    product_price = float(price_text) if price_text else 0.0
                else:
                    product_price = 0.0

                if product_image:
                    product_image_url = product_image.get("data-lazy-src") or product_image.get("src")
                else:
                    product_image_url = ""

                add_to_cart_button = product_element.select_one(".addtocart-buynow-btn a[data-product_id]")
                product_id = add_to_cart_button["data-product_id"] if add_to_cart_button else ""

                # Check if the product exists in the cache
                cached_product = self.cache.get(product_id) if self.cache else None

                if cached_product:
                    cached_product = json.loads(cached_product)
                    if cached_product["product_price"] == product_price:
                        # Skip updating the product if the price hasn't changed
                        continue
                    else:
                        print(f"Product price changed for {product_title}. Old price: {cached_product['product_price']}, New price: {product_price} on page {page_count}.")
                        # Update the cache with the latest product data
                        if self.cache:
                            self.cache.set(product_id, json.dumps(cached_product))

                product = {
                    "product_id": product_id,
                    "product_title": product_title,
                    "product_price": product_price,
                    "product_image_url": product_image_url,
                }
                products.append(product)

                # Update the cache with the latest product data
                if self.cache:
                    self.cache.set(product_id, json.dumps(product))

            # Status update notification after each page
            if self.notification:
                message = f"Scraping completed. {len(products)} products scraped and updated in the database till page {page_count}."
                self.notification.send(message)

            page_count += 1

            # Save the scraped products to the storage for each page
            if self.storage:
                self.storage.save(products)

        return products

    def _fetch_page(self, url: str, retry_count: int = 3, retry_delay: int = 5) -> requests.Response:
        while retry_count > 0:
            try:
                response = requests.get(url, proxies={"http": self.proxy, "https": self.proxy})
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException:
                retry_count -= 1
                time.sleep(retry_delay)
        return None