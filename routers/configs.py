from fastapi import APIRouter

from database import Settings

router = APIRouter()


@router.get("/product")
async def get_product():
    product = Settings.find_one({"type": "product"})
    del product["_id"]
    return {"status": "success", "data": product}
