from ninja import Schema
from datetime import datetime

class UserSimpleSchema(Schema):
    id: int
    username: str

class UserSchema(UserSimpleSchema):
    first_name: str
    email: str
    date_joined: datetime

class UserRegisterSchema(Schema):
    username: str
    first_name: str
    email: str
    password1: str
    password2: str