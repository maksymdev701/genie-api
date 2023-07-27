from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import configs
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
app.include_router(configs.router, prefix="/api/config", tags=["Configurator"])


@app.get("/healthchecker")
async def healthchecker():
    return {"status": "success"}
