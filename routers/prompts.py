from fastapi import APIRouter
from bson.objectid import ObjectId
from pymongo import ASCENDING
import openai

from database import Prompts, Products
from schemas.promptSchemas import PromptBaseSchema, RunPromptSchema
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


@router.get("/names")
async def get_prompt_from_products(product_name: str, product_module: str):
    product = Products.find_one(
        {"product_name": product_name, "product_module": product_module}
    )
    pipeline = [
        {"$match": {"product_id": product["_id"]}},
        {
            "$lookup": {
                "from": "products",
                "localField": "product_id",
                "foreignField": "_id",
                "as": "populated_product",
            }
        },
        {"$unwind": "$populated_product"},
        {"$sort": {"order": ASCENDING}},
        {
            "$project": {
                "_id": 0,
                "prompt_name": 1,
            }
        },
    ]
    prompts = Prompts.aggregate(pipeline)
    return {"status": "success", "data": list(prompts)}


@router.post("/run")
async def run_prompt(info: RunPromptSchema):
    product = Products.find_one(
        {"product_name": info.product_name, "product_module": info.product_module}
    )
    prompt = Prompts.find_one(
        {"product_id": product["_id"], "prompt_name": info.prompt_name}
    )
    print(prompt)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are CodeGenie that helps people with code.",
            },
            {
                "role": "user",
                "content": f"{prompt['prompt']}\n\n++++++++++++++++++++\n\n{info.code}\n\n++++++++++++++++++++",
            },
        ],
    )
    reply = completion.choices[0].message.content
    return {"status": "success", "msg": reply}
