from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import products
from config import settings

app = FastAPI()

origins = [settings.CLIENT_ORIGIN]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api/config", tags=["Configurator"])


@app.get("/")
async def health_checker():
    return {"status": "success"}
