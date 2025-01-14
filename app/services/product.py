from sqlmodel import Session

from app.infras.scraping import scrape_web_content_on_amazon_content
from app.infras.searchapi import search_products_on_external_source
from app.llms.openai import generate_product_information, generate_manufacture
from app.repositories.product import ProductRepository


class ProductService:
    def __init__(self, session: Session):
        self.repository = ProductRepository(session)

    def get_products(self, query: str):
        results = self.repository.search_products_by_name(query)
        return [
            {
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "reviews": product.reviews,
                "manufacture": (
                    {
                        "id": product.manufacture.id,
                        "name": product.manufacture.name,
                        "address": product.manufacture.address,
                        "phone": product.manufacture.phone,
                        "email": product.manufacture.email,
                    }
                    if product.manufacture
                    else None
                ),
                "category": product.category,
                "id": product.id,
                "rating": product.rating,
                "spec": product.spec,
            }
            for product in results
        ]

    def sync_external_info(self, query: str):
        external_results = search_products_on_external_source(query)

        for result in external_results:
            manufacture_name = result.brand or result.media

            if (
                manufacture_name
                and (
                    manufacture := self.repository.get_manufacture_by_name(
                        manufacture_name
                    )
                )
                is None
            ):
                manufacture_dict = generate_manufacture(manufacture_name)
                manufacture = self.repository.add_manufacture(
                    name=manufacture_name,
                    address=manufacture_dict.get("address"),
                    phone=manufacture_dict.get("phone"),
                    email=manufacture_dict.get("email"),
                )

            if self.repository.get_product_by_name(result.title) is not None:
                continue

            scraped_data = scrape_web_content_on_amazon_content(url=result.link)
            product_dict = generate_product_information(
                dict(
                    name=scraped_data.title or result.title,
                    description=scraped_data.about_product or "",
                    price=result.extracted_price or "",
                )
            )
            if not product_dict:
                continue
            manufacture = self.repository.get_manufacture_by_name(manufacture_name)
            self.repository.add_product(
                name=scraped_data.title or result.title,
                description=product_dict.get("description"),
                category=product_dict.get("category"),
                price=result.extracted_price or product_dict.get("price"),
                spec=product_dict.get("spec", {}),
                rating=result.rating,
                reviews=result.reviews,
                manufacture_id=manufacture.id if manufacture else None,
            )
