from pydantic import BaseModel
import requests


from config import get_settings


settings = get_settings()


class OrganicResult(BaseModel):
    title: str
    link: str
    brand: str | None = None
    media: str | None = None
    rating: float | None = None
    reviews: int | None = None
    price: str | None = None
    extracted_price: float | None = None
    original_price: str | None = None
    attributes: list | None = None
    thumbnail: str | None = None


def search_products_on_external_source(query: str, engine: str = "amazon_search"):
    url = "https://www.searchapi.io/api/v1/search"
    params = {
        "engine": engine,
        "q": query,
        "api_key": settings.searchapi_key,
    }

    response = requests.get(url, params=params)

    if not response.ok:
        response.raise_for_status()

    organic_results = response.json().get("organic_results", [])
    validated_results = [OrganicResult(**result) for result in organic_results]
    return validated_results
