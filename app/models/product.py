from typing import Dict
from uuid import uuid4, UUID

from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel, JSON


class Manufacture(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    address: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    email: str | None = Field(default=None)

    products: list["Product"] = Relationship(back_populates="manufacture")

    __tablename__ = "manufacturers"


class Product(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: str
    category: str
    price: float
    rating: float | None = None
    reviews: int | None = None
    spec: Dict = Field(default_factory=dict, sa_column=Column(JSON))
    manufacture_id: UUID | None = Field(default=None, foreign_key="manufacturers.id")
    manufacture: Manufacture | None = Relationship(back_populates="products")

    __tablename__ = "products"
