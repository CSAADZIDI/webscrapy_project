from dataclasses import dataclass

@dataclass
class Book:
    id: int
    title: str
    price: float
    stock: int
    rating: int
    category: str
    description: str
    upc: str
    product_type: str
    price_excl_tax: float
    price_incl_tax: float
    tax: float
    number_of_reviews: int
    availability: str
    image_url: str
    product_page_url: str
