import requests
from pydantic import BaseModel
from bs4 import BeautifulSoup


class ScrapedData(BaseModel):
    title: str | None
    price: str | None
    about_product: str | None


def scrape_web_content_on_amazon_content(url: str) -> ScrapedData:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if not response.ok:
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    title = (
        soup.find(id="productTitle").get_text(strip=True)
        if soup.find(id="productTitle")
        else None
    )
    price = (
        soup.find("span", class_="a-offscreen").get_text(strip=True)
        if soup.find("span", class_="a-offscreen")
        else None
    )
    about_product = (
        soup.find(id="feature-bullets").get_text(strip=True)
        if soup.find(id="feature-bullets")
        else None
    )

    return ScrapedData(
        title=title,
        price=price,
        about_product=about_product,
    )
