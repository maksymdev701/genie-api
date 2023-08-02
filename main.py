from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai

from routers import products, prompts
from config import settings

openai.api_key = settings.OPENAI_API_KEY

app = FastAPI()

origins = [settings.CLIENT_ORIGIN]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(prompts.router, prefix="/api/prompts", tags=["Prompts"])


@app.get("/")
async def health_checker():
    return {"status": "success"}
