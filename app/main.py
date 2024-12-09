from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from app.controllers.product import product_router
from app.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
api_router = APIRouter()
api_router.include_router(product_router)
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello World"}
