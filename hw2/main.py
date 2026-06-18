"""Разработать систему регистрации пользователя, используя Pydantic для валидации входных данных,
обработки вложенных структур и сериализации. Система должна обрабатывать данные в формате
JSON:
1. Создать классы моделей данных с помощью Pydantic для пользователя и его адреса.
2. Реализовать функцию, которая принимает JSON строку, десериализует её в объекты Pydantic,
валидирует данные, и в случае успеха сериализует объект обратно в JSON и возвращает его.
3. Добавить кастомный валидатор для проверки соответствия возраста и статуса занятости
пользователя.
4. Написать несколько примеров JSON строк для проверки различных сценариев валидации:
успешные регистрации и случаи, когда валидация не проходит (например возраст не
соответствует статусу занятости).

Модели:
● Address: Должен содержать следующие поля:
○ city: строка, минимум 2 символа.
○ street: строка, минимум 3 символа.
○ house_number: число, должно быть положительным.
● User: Должен содержать следующие поля:
○ name: строка, должна быть только из букв, минимум 2 символа.
○ age: число, должно быть между 0 и 120.
○ email: строка, должна соответствовать формату email.
○ is_employed: булево значение, статус занятости пользователя.
○ address: вложенная модель адреса."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, EmailStr, ConfigDict, field_serializer, model_validator, ValidationError


class Address(BaseModel):
    city: str = Field(..., min_length=2, description="City")
    street: str = Field(..., min_length=3, description="Street")
    house_number: int = Field(..., gt=0, description="House number")

    model_config = ConfigDict(validate_assignment=True)

class User(BaseModel):
    name: str = Field(..., min_length=2, description="The name of the user")
    age: int = Field(..., ge=0, le=120, description="The age of the user")
    email: EmailStr = Field(..., description="The email of the user")
    is_employed: bool = Field(..., description="The status of an employment")
    date: datetime = Field(default_factory=lambda: datetime.now(), description="Date of creation")
    address: Address = Field(..., description="Full address")

    model_config = ConfigDict(validate_assignment=True)

    @classmethod
    def validate_json(cls, json_string: str) -> str:
        try:
            json_deserialized = cls.model_validate_json(json_string, strict=True)
            return json_deserialized.model_dump_json()
        except ValidationError as e:
            return e.json()

    @field_validator('name')
    def check_name(cls, value: str):
        if not value.isalpha():
            raise ValueError('The name must contain letters only!!')
        return value

    @model_validator(mode='after')
    def check_age(self):
        if self.age < 18 and self.is_employed:
            raise ValueError("For employment status person must be 18 y.o. at least!!")
        return self

    @field_serializer('date')
    def dt_serialize(self, value: datetime):
        return value.strftime("%Y-%m-%d %H:%M")

johny = """{
             "name": "John",
             "age": 22,
             "email": "john.doe@example.com",
             "is_employed": true,
             "address": {
             "city": "New York",
             "street": "5th Avenue",
             "house_number": 123
             }
            }"""

user_johny = User.validate_json(johny)
print(user_johny)

kenny = """{
             "name": "Kenny",
             "age": 13,
             "email": "kenny@example.com",
             "is_employed": true,
             "address": {
             "city": "Hamburg",
             "street": "Reeperbahn",
             "house_number": 14
             }
            }"""

user_kenny = User.validate_json(kenny)
print(user_kenny)

kate = """{
             "name": "Kate123",
             "age": 36,
             "email": "kate@example.com",
             "is_employed": true,
             "address": {
             "city": "Berlin",
             "street": "Brandenburger Tor",
             "house_number": 1
             }
            }"""

user_kate = User.validate_json(kate)
print(user_kate)

