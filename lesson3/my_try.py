import logging

from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

logging.basicConfig(level=logging.INFO, filename='my_try.log', filemode='w')
logger = logging.getLogger('sqlalchemy.engine')

# engine = create_engine('sqlite:///another_db.db')
engine = create_engine('sqlite:///:memory:')

LocalSession = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    age: Mapped[int]

    addresses: Mapped[list['Address']] = relationship(back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(first_name={self.first_name}, last_name={self.last_name}, age={self.age})>"

class Address(Base):
    __tablename__ = 'addresses'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String(100))
    street: Mapped[str] = mapped_column(String(100))
    house: Mapped[int]
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete='CASCADE'))

    user: Mapped[User] = relationship(back_populates='addresses')

    def __repr__(self):
        return f"<Address(city={self.city}, street={self.street}, house={self.house}, user_id={self.user_id})>"

with engine.begin() as conn:
    Base.metadata.create_all(conn)

with LocalSession() as session:
    user_1 = User(first_name='Tony', last_name='Quark', age=45)
    user_2 = User(first_name='Johny', last_name='Cage', age=35)

    address_1 = Address(city='SPB', street='Obuhovskiy', house=13)
    address_2 = Address(city='Berlin', street='Reveler Strasse', house=45)

    user_1.addresses.extend([address_1, address_2])

    session.add(user_1)
    session.add(user_2)

    session.commit()

print(user_1)
print(user_1.addresses)
print(user_2)

