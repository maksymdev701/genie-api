from pydantic import BaseModel


class PromptBaseSchema(BaseModel):
    products: str
    plans: str
    module: str
    prompt_name: str
    order: int
