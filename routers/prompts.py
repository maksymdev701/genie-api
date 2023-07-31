from fastapi import APIRouter

from database import Prompts

router = APIRouter()


@router.get("/")
async def get_prompts():
    prompts = list(Prompts.find({}))
    print(prompts)
    return {"status": "success"}


# @router.post("")
# async def add_prompt():
