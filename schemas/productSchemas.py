from pydantic import BaseModel
from bson.objectid import ObjectId


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

    class Config:
        populate_by_name = True
