from pydantic import BaseModel, Field
import uuid


class PromptBaseSchema(BaseModel):
    products: str
    plans: str
    module: str
    prompt_name: str
    order: int
    prompt: str
