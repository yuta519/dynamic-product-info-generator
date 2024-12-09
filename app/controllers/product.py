from fastapi import APIRouter, HTTPException

from fastapi import Depends
from sqlmodel import Session
from app.database import get_session
from app.services.product import ProductService


product_router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@product_router.get("/")
def get_products(query: str, session: Session = Depends(get_session)):
    try:
        service = ProductService(session=session)
        return service.get_products(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@product_router.get("/sync-external-search")
def sync_external_search(query: str, session: Session = Depends(get_session)):
    try:
        service = ProductService(session=session)
        return service.sync_external_info(query)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed syncing all data: {str(e)}"
        )
