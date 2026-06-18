from flask import Flask, request, jsonify
from typing import List
from datetime import datetime
import os

from pydantic import BaseModel, EmailStr, ValidationError, Field, field_validator, ConfigDict

# def func(a: list[str]):
#     return 'Hello'
#
# print(func([1,2,3]))
#
# class MyModel(BaseModel):
#     a: int | float
#     b: List[int]

# --------------------------

class User(BaseModel):

    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(str_min_length = 2, str_strip_whitespace=True,
        json_encoders = {
            datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M')
        })

    # class Config:
    #     str_min_length = 2
    #     str_strip_whitespace = True
    #     json_encoders = {
    #         datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M')
    #     }

user = User(first_name="John", last_name="Doe", email="doe@example.com", created_at=datetime.now())
print(user)
print(user.model_dump_json())

print()
# ----------------------

class User(BaseModel):
    name: str = Field(alias="full_name", max_length=100, min_length=2)
    email: EmailStr

    @field_validator('email')
    def email_validator(cls, email: EmailStr):
        if email.split('.')[-1] != "com":
            raise ValidationError("Invalid email format")
        return email

    @field_validator('name')
    def name_validator(cls, name: str):
        if not name.isalpha():
            raise ValidationError("Invalid name")
        return name

    model_config = ConfigDict(str_strip_whitespace=True)

    # class Config:
    #     str_strip_whitespace = True


try:
    user0 = User(full_name='  SSSS            ', email=" SSS@example.com")
    print(user0)
    user1 = User(full_name='Alice', email="alice@example.com")
    print(user1)
    user2 = User(full_name='John', email="john@example.com")
    print(user2)
except ValidationError as e:
    print(e)

print()
# ----------------------

class User(BaseModel):
    name: str = Field(alias="full_name")
    age: int

json_string = """
            {
            "full_name": "John doe",
            "name": "Alice",
            "age": 22
            }
            """

user1 = User.model_validate_json(json_string)
print(user1)

print(__file__)
print(os.path.dirname(__file__))