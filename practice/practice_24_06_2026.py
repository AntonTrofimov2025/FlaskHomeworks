# pylint: disable=line-too-long

# Создайте модель Event, которая включает поля:
# ● title (строка),
# ● date (дата и время события),
# ● location (строка).
# Добавьте валидацию, чтобы дата события не была в прошлом.
from datetime import datetime, timedelta

from pydantic import BaseModel, field_validator

import pytest

class Event(BaseModel):
    title: str
    date: datetime
    location: str

    @field_validator('date')
    @classmethod
    def validate_date(cls, value):
        if datetime.now() > value:
            raise ValueError('The date is in the past!')
        return value

def test_date_validation():
    with pytest.raises(ValueError, match='The date is in the past!'):
        Event(date=datetime(year=2026, day=23, month=6), title='Soccer', location='New York')

# Определите модель UserProfile с полями:
# ● username (строка),
# ● password (строка),
# ● email (строка с валидацией email).
# Используйте Field для добавления описаний и настройки валидации пароля (должен быть не менее 8
# символов).

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from decimal import Decimal

class UserProfile(BaseModel):
    username: str = Field(description='Your username')
    password: str = Field(min_length=8, description='Your personal password')
    email: EmailStr

    model_config = ConfigDict(validate_assignment=True)

@pytest.mark.parametrize('password', ['1234567', '2345', 'fjfjf'])
def test_model_user_profile(password):
    with pytest.raises(ValueError):
        UserProfile(username='anton', password=password, email='anton@yahoo.com')

# Разработайте модель Transaction для управления финансовыми операциями.
# Модель должна содержать:
# ● amount (десятичное число),
# ● transaction_type (строка, принимает значения "debit" или "credit"),
# ● currency (строка).

class Transaction(BaseModel):
    amount: Decimal
    transaction_type: str
    currency: str

    @field_validator('transaction_type')
    @classmethod
    def validate_transaction(cls, value):
        if value not in ['debit', 'credit']:
            raise ValueError('Your transaction type must be either debit or credit!')
        return value

@pytest.mark.parametrize('transaction_type', ['abc', 'kredit'])
def test_validate_trans_type(transaction_type):
    with pytest.raises(ValueError, match='Your transaction type must be either debit or credit!'):
        Transaction(amount=Decimal('123.23'), transaction_type=transaction_type, currency='USD')

# Создайте модель Appointment для записи на прием, которая включает patient_name (строка),
# appointment_date (дата и время), и проверку, что запись не может быть установлена ранее, чем
# через 24 часа от текущего момента.

class Appointment(BaseModel):
    patient_name: str
    appointment_date: datetime

    @field_validator('appointment_date')
    @classmethod
    def validate_date(cls, value):
        if datetime.now() + timedelta(hours=24) > value:
            raise ValueError('You have to wait! :D')
        return value

def test_appointment_date_validation():
    with pytest.raises(ValueError, match='You have to wait! :D'):
        Appointment(appointment_date=datetime.now() + timedelta(hours=23), patient_name='johny')

# Создайте экземпляр движка для подключения к MySQL базе данных.

import  os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from dotenv import load_dotenv

current_path = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_path, '..', '.env')

load_dotenv(env_path)
db_url = os.getenv('DB_EDIT_URL')

engine = create_engine(db_url)

def test_our_connection():
    with Session(engine):
        pass

# Напишите код для создания движка SQLAlchemy с подключением к базе данных SQLite,
# который будет располагаться в памяти, и настройте вывод логов всех операций с базой
# данных на экран.

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('sqlalchemy.engine')

engine = create_engine('sqlite:///:memory:')

logger.setLevel(logging.INFO)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50))
    age: Mapped[int]

    posts: Mapped[list['Post']] = relationship(back_populates='user', cascade='all, delete-orphan')
    addresses: Mapped[list['Address']] = relationship(back_populates='user', cascade='all, delete-orphan')

def test_our_class():
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        user_1 = User(username='anton', age=35)

        session.add(user_1)
        session.commit()
        # session.refresh()
        assert user_1.username == 'anton'

# Определите две модели, User и Post, где пользователь может иметь много постов (один
# ко многим). Используйте декларативный базовый класс.

class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete='CASCADE'))

    user: Mapped[User] = relationship(back_populates='posts')

def test_create_post():
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        user_1 = User(username='mary', age=27, posts=[Post(message="Hello, world!"), Post(message='My Name is Mary')])
        session.add(user_1)

        session.commit()
        for post in user_1.posts:
            assert post.user_id == user_1.id

# Определите две модели: User и Address, где User может иметь множество Address.
# Используйте декларативный базовый класс.

class Address(Base):
    __tablename__ = 'addresses'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String(20))
    street: Mapped[str] = mapped_column(String(30))
    house_number: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete='CASCADE'))

    user: Mapped[User] = relationship(back_populates='addresses')

@pytest.mark.parametrize('addresses', [[Address(city='SPB', street='Nevskiy avenue', house_number=27),
                                        Address(city='SPB', street='Liteiniy avenue', house_number=13)],
                                   [Address(city='Berlin', street='Alexander Platz', house_number=45),
                                    Address(city='Barcelona', street='Plaça de Catalunya', house_number=27)]])
def test_user_with_address(addresses):
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        user_address_1 = User(username='Tony',age=27, posts=[Post(message="Hello, world!"),
                                                             Post(message='My Name is Tony')],
                              addresses=addresses)
        session.add(user_address_1)
        session.commit()
        for address in user_address_1.addresses:
            assert address.user_id == user_address_1.id

# Используя ранее определённые модели User и Address, создайте нового пользователя и
# адрес, добавьте их в базу данных с помощью сессии, затем удалите пользователя и
# проверьте изменения.

def test_delete_user():
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        user_to_delete = User(username='Tony',age=27, addresses=[Address(city='Berlin', street='Alexander Platz', house_number=45)])
        session.add(user_to_delete)
        session.commit()
        user_id = user_to_delete.id
        user_address_id = user_to_delete.addresses[0].id
        session.delete(user_to_delete)
        session.commit()
        assert session.get(User, user_id) is None
        assert session.get(Address, user_address_id) is None

