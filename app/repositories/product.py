from uuid import UUID

from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from app.models.product import Manufacture, Product


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_manufacture_by_name(self, name: str) -> Manufacture | None:
        statement = select(Manufacture).where(Manufacture.name == name)
        return self.session.exec(statement).first()

    def add_manufacture(self, name: str, address: str, phone: str, email: str):
        result = Manufacture(
            name=name,
            address=address,
            phone=phone,
            email=email,
        )
        self.session.add(result)
        self.session.commit()
        return result

    def search_products_by_name(self, search_term: str):
        statement = (
            select(Product)
            .options(joinedload(Product.manufacture))
            .where(Product.name.contains(search_term))
        )
        return self.session.exec(statement).all()

    def get_product_by_name(self, name: str) -> Product | None:
        statement = select(Product).where(Product.name == name)
        return self.session.exec(statement).first()

    def add_product(
        self,
        name: str,
        description: str,
        category: str,
        spec: dict,
        price: float | None,
        rating: float | None = None,
        reviews: int | None = None,
        manufacture_id: UUID | None = None,
    ):
        product = Product(
            name=name,
            description=description,
            category=category,
            price=price,
            spec=spec,
            rating=rating,
            reviews=reviews,
            manufacture_id=manufacture_id,
        )
        self.session.add(product)
        self.session.commit()
        return product
