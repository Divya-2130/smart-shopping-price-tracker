import requests
from django.conf import settings

BASE_URL = f"https://{settings.RAPIDAPI_HOST}"


def _headers():
    return {
        "x-rapidapi-key": settings.RAPIDAPI_KEY,
        "x-rapidapi-host": settings.RAPIDAPI_HOST,
        "Content-Type": "application/json",
    }


def search_products(query: str, country: str = "US"):
    url = f"{BASE_URL}/search"
    params = {"query": query, "country": country}

    response = requests.get(url, headers=_headers(), params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    raw_products = data.get("data", {}).get("products", [])
    return [_format_result(item) for item in raw_products]


def get_current_price(asin: str, country: str = "US"):
    url = f"{BASE_URL}/product-details"
    params = {"asin": asin, "country": country}

    response = requests.get(url, headers=_headers(), params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    price_str = str(data.get("data", {}).get("product_price", "0"))
    return float(price_str.replace("$", "").replace(",", "")) if price_str else 0.0


def _format_result(item: dict) -> dict:
    price_str = str(item.get("product_price", "0"))
    return {
        "name": item.get("product_title", "Unknown product"),
        "seller": "Amazon",
        "price": float(price_str.replace("$", "").replace(",", "") or 0),
        "image_url": item.get("product_photo", ""),
        "product_link": item.get("product_url", ""),
        "external_id": item.get("asin", ""),
    }