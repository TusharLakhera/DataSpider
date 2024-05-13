# app/models.py

from pydantic import BaseModel

class Product(BaseModel):
    product_id: str
    product_title: str
    product_price: float
    product_image_url: str