from ninja import Schema
from datetime import datetime

class CategorySchema(Schema):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

class CategoryCreationSchema(Schema):
    name: str

class CategoryUpdateSchema(Schema):
    name: str