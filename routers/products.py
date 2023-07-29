from fastapi import APIRouter, Body

from database import Products
from schemas import productSchemas
from serializers.productSerializers import productsEntity

router = APIRouter()


@router.get("/")
async def get_product(product_name: str, product_module: str):
    product = Products.find_one(
        {"product_name": product_name, "product_module": product_module}
    )
    if product:
        del product["_id"]
    return {"status": "success", "data": product}


@router.get("/search")
async def search_product(search_key: str):
    query = {
        "$or": [
            {"product_name": {"$regex": search_key}},
            {"product_module": {"$regex": search_key}},
        ]
    }
    results = Products.find(query, projection={"product_name", "product_module"})
    results = productsEntity(results)
    return {"status": "success", "data": results}


@router.post("/")
async def update_product(product: productSchemas.ProductBaseSchema):
    existing_one = Products.find_one(
        {"product_name": product.product_name, "product_module": product.product_module}
    )
    print(product.source_check)
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
