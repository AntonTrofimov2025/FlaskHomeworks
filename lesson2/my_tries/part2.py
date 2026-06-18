from datetime import datetime

from pydantic import BaseModel, Field, ValidationError, EmailStr, HttpUrl, field_validator, ConfigDict, field_serializer


class Product(BaseModel):
    name: str
    description: str | None = Field(default=None, description="The description of the product")
    price: float = Field(gt=0, description="The price must be greater than zero")
    in_stock: bool = Field(default=True, alias="available")

try:
    product = Product(name="MakaroniMitKäse", price=-10)
except ValidationError as e:
    print(e)
    print(e.json()) # Converts into JSON
    print(e.errors()) # Converts into Python Dictionary

class User(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="The name of the user")
    age: int = Field(..., ge=18, le=99, description="Age must be between 18 and 99")

    # email: EmailStr
    # homepage: HttpUrl
print()
# ------------------------------------------------------------------------------------------------

class User(BaseModel):
    name: str
    age: int
    email: EmailStr

    @field_validator('email')
    def check_email_domain(cls, value: EmailStr):
        allowed_domains = ['example.com', 'test.com']
        if value.split('@')[-1] not in allowed_domains:
            raise ValueError(f"Email must be from one of the following domains: {', '.join(allowed_domains)}")
        return value

try:
    user_valid = User(name="Alice", age=30,
                      email="alice@example.com")
    print(f"Valid user: {user_valid}")
    user = User(name="Anton", age=35, email="xixi@google.com")
except ValueError as e:
    print(e.json())

print()
# -----------------------------------------------------------------------------------------------------------

class User(BaseModel):
    username: str
    email: EmailStr

    @field_validator('username')
    def check_username(cls, value: str):
        if not value.isalpha():
            raise ValueError("Only chars are allowed!!")
        return value

    @field_validator('email')
    def check_email(cls, value: EmailStr):
        if not value.endswith(".com"):
            raise ValueError("The email must end with .com!!")
        return value

try:
    user_valid = User(username="Tony", email="tony@msn.com")
    print(user_valid)
    user = User(username="Anya", email="anya@hallo.msn")
except ValueError as e:
    print(e)

# Config example

from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    date: datetime

    @field_serializer('date')
    def dt_serialize(self, value: datetime) -> str:
        return value.strftime('%d-%m-%Y %H:%M')


    # VERY GOOD STYLE :)
    model_config = ConfigDict(str_strip_whitespace=True, str_min_length=1,validate_assignment=True,
                              ) # json_encoders OLD BAD STYLE: json_encoders={datetime: lambda dt: dt.strftime('%d-%m-%Y %H:%M')}

    # OLD STYLE, BAD
    # class Config:
    #     str_strip_whitespace = True
    #     str_min_length = 1
    #     validate_assignment = True

user = User(name="Kate", age=36, date=datetime.now())
print(user)
print()
print(user.model_dump_json()) # Дампим наш объект модели в JSON :)

# -------------------------------------------------------------------------------------------------------------

class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime = datetime.now()

    model_config = ConfigDict(str_min_length=2, str_strip_whitespace=True)

    @field_serializer('created_at')
    def dt_serialize(self, value: datetime):
        return value.strftime("%Y-%m-%d %H:%M")

user = User(first_name="John", last_name="Doe", email="doe@example.com")
print(user)

print(user.model_dump_json())


