from pydantic import BaseModel


class PricePlanSchema(BaseModel):
    plan_name: str
    total_wish: int
    price: int
    period: str


class ProductBaseSchema(BaseModel):
    product_name: str
    product_module: str
    module_description: str
    source_check: list[str]
    source_text: str
    source_image: str
    source_url: str
    input_box_title: str
    input_box_description: str
    export_check: list[str]
    export_word: str
    export_pdf: str
    export_text: str
    price_plan: list

    class Config:
        populate_by_name = True
