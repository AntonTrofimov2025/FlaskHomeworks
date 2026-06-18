import json

from pydantic import BaseModel, EmailStr, ValidationError

class Address(BaseModel):
    city: str
    street: str
    house_number: int

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
             "house_number": 123
             }
            }"""

try:
    user = User.model_validate_json(json_string, strict=True)
    print(user)
    with open('json_res.json', "w", encoding="utf-8") as file:
        json.dump(user.model_dump_json(), file)
except ValidationError as e:
    print(f"ValidationError: {e}")\

print()
print("Дампим модель обратно в JSON: ")
print(user.model_dump_json())

class User(BaseModel):
    name: str
    age: int

    def greet(self):
        return f"Hello, my name is {self.name} and I'm {self.age} years old."

    def __str__(self):
        return f'Name: {self.name}, Age: {self.age} years old'

user = User(name="Anton", age=35)
print(user.greet())
print(user)

class User(BaseModel):
    username: str
    email: EmailStr

    def __str__(self):
        return f"Name: {self.username}, Email: {self.email}"

class Admin(User):
    access_level: int = 10

    def __str__(self):
        return f"Admin: {self.username}, Email: {self.email}, Access level: {self.access_level}"

    def promote_user(self, user: User):
        print(f"Promoting {self.username} to higher privileges")
        return Admin(username=user.username, email=user.email, access_level=self.access_level + 1)

user = User(username="Anton", email="xixi@gmail.com")
print(user)

admin = Admin(username='admin_user', email='admin@example.com')
print(admin)
promoted_user = admin.promote_user(user)
print(promoted_user)