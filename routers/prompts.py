from fastapi import APIRouter

from database import Prompts
from schemas.promptSchemas import PromptBaseSchema

router = APIRouter()


@router.get("/")
async def get_prompts():
    prompts = list(Prompts.find({}))
    print(prompts)
    return {"status": "success"}


@router.post("/")
async def add_prompt(prompt: PromptBaseSchema):
    Prompts.insert_one(prompt.model_dump())
    return {"status": "success"}
