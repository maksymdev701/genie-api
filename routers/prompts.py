from fastapi import APIRouter
from bson.objectid import ObjectId

from database import Prompts, Products
from schemas.promptSchemas import PromptBaseSchema
from serializers.promptsSerializers import promptsEntity

router = APIRouter()


@router.get("/")
async def get_prompts():
    pipeline = [
        {
            "$lookup": {
                "from": "products",
                "localField": "product_id",
                "foreignField": "_id",
                "as": "populated_product",
            }
        },
        {"$unwind": "$populated_product"},
        {
            "$project": {
                "product_name": "$populated_product.product_name",
                "product_module": "$populated_product.product_module",
                "plan": 1,
                "prompt_name": 1,
                "order": 1,
                "prompt": 1,
            }
        },
    ]
    prompts = list(Prompts.aggregate(pipeline))
    print(prompts)
    prompts = promptsEntity(prompts=prompts)
    return {"status": "success", "data": prompts}


@router.post("/")
async def add_prompt(prompt: PromptBaseSchema):
    product = Products.find_one(
        {"product_name": prompt.product, "product_module": prompt.module}
    )
    Prompts.insert_one(
        {
            "product_id": ObjectId(product["_id"]),
            "plan": prompt.plan,
            "prompt_name": prompt.prompt_name,
            "order": prompt.order,
            "prompt": prompt.prompt,
        }
    )
    return {"status": "success"}


@router.patch("/{id}")
async def update_prompt(id: str, prompt: PromptBaseSchema):
    product = Products.find_one(
        {"product_name": prompt.product, "product_module": prompt.module}
    )
    Prompts.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "product_id": ObjectId(product["_id"]),
                "plan": prompt.plan,
                "prompt_name": prompt.prompt_name,
                "order": prompt.order,
                "prompt": prompt.prompt,
            }
        },
    )
    return {"status": "success"}
