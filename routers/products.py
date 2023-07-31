from fastapi import APIRouter, Body, HTTPException, status
from bson.objectid import ObjectId

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
    results = Products.find(query, projection={"_id", "product_name", "product_module"})
    results = productsEntity(results)
    return {"status": "success", "data": results}


@router.post("/")
async def add_product(product: productSchemas.ProductBaseSchema):
    existing_one = Products.find_one(
        {"product_name": product.product_name, "product_module": product.product_module}
    )
    print(product)
    if existing_one:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product name and product module have conflicts.",
        )
    else:
        Products.insert_one(product.model_dump())
    return {"status": "success"}


@router.patch("/")
async def update_product(product: productSchemas.ProductUpdateSchema):
    print(product.id)
    data = product.model_dump()
    del data["id"]
    existing_one = Products.find_one(
        {"product_name": product.product_name, "product_module": product.product_module}
    )
    if existing_one:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product name and product module have conflicts.",
        )
    else:
        Products.update_one(
            {"_id": ObjectId(product.id)},
            {"$set": data},
        )
    return {"status": "success"}


@router.patch("/update_price")
async def update_price(product: productSchemas.PriceUpdateSchema):
    existing_one = Products.find_one(
        {"product_name": product.product_name, "product_module": product.product_module}
    )
    print(product)
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


@router.get("/names")
async def get_product_names():
    product_names = Products.distinct("product_name")
    return {"status": "success", "data": list(product_names)}
