from fastapi import APIRouter

from database import Products
from schemas import productSchemas

router = APIRouter()


@router.get("/product")
async def get_product():
    product = Products.find_one({"type": "product"})
    del product["_id"]
    return {"status": "success", "data": product}


@router.post("/product")
async def update_product(product: productSchemas.ProductBaseSchema):
    existing_one = Products.find_one(
        {"product_name": product.product_name, "product_module": product.product_module}
    )
    if not existing_one:
        Products.insert_one(product.model_dump())
    else:
        Products.update_one(
            {
                "product_name": product.product_name,
                "product_module": product.product_module,
            },
            {"$set": product.model_dump()},
        )
    return {"status": "success"}
