from pydantic import BaseModel, EmailStr, ValidationError
import json

class Address(BaseModel):
    city: str
    street: str
    house_number: str

class User(BaseModel):
    name: str
    age: int
    email: EmailStr
    address: Address

json_string = """{
    "name": "John Doe",
    "age": 22,
    "email": "john.doe@example.com",
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": "123"
    }
}"""

# user1 = User(**json.loads(json_string))
try:
    user1 = User.model_validate_json(json_string, strict=True)
    print(user1)
    with open("json_user1.json", "w", encoding="utf-8") as file:
        json.dump(user1.model_dump_json(), file)
except ValidationError as e:
    print(e)

# -----------------------------------
# user_data = {
#     "name": "John",
#     "age": "1dsd8"
# }
#
# try:
#     user1 = User(**user_data)
#     print(user1)
# except Exception as e:
#     print(e)
# -----------------------------------

# user1 = User(name='John', age=18)
# print(user1)

# -----------------------------------

# class OOPUser:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#
#     @property
#     def name(self):
#         return self.__name
#
#     @name.setter:
#     def name(self, value):
#         if not isinstance(value, str):
#             raise TypeError("name must be a str!")
#
#     @property
#     def age(self):
#         return self.__age
#
#     @name.setter:
#     def age(self, value):
#         if not isinstance(value, int):
#             raise TypeError("age must be a int!")