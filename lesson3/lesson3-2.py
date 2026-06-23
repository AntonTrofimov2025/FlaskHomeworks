# from sqlalchemy import create_engine, String, ForeignKey
# from sqlalchemy.orm import sessionmaker, mapped_column, DeclarativeBase, Mapped
#
# engine = create_engine('sqlite:///sqlalchemy_lesson3-2.db')
# LocalSession = sessionmaker(bind=engine)
#
# class Base(DeclarativeBase):
#     pass
#
# class User(Base):
#     __tablename__ = 'users'
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     first_name: Mapped[str] = mapped_column(String(100))
#     last_name: Mapped[str] = mapped_column(String(100))
#     age: Mapped[int]
#
#
# class Address(Base):
#     __tablename__ = 'addresses'
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     city: Mapped[str] = mapped_column(String(100))
#     street: Mapped[str] = mapped_column(String(100))
#     house: Mapped[str] = mapped_column(String(100))
#     # user_id: Mapped[str] = mapped_column(ForeignKey(User.id, ondelete='CASCADE'))
#     user_id: Mapped[str] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
#
# with engine.begin() as conn:
#     Base.metadata.create_all(conn)
#


from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import sessionmaker, mapped_column, DeclarativeBase, Mapped, relationship

engine = create_engine('sqlite:///sqlalchemy_lesson3-2.db')
LocalSession = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int]
    addresses: Mapped[list['Address']] = relationship(back_populates='user',
                                                      cascade='all, delete-orphan')

    def __repr__(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, age={self.age})"


class Address(Base):
    __tablename__ = 'addresses'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String(100))
    street: Mapped[str] = mapped_column(String(100))
    house: Mapped[str] = mapped_column(String(100))
    # user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    user: Mapped[User] = relationship(back_populates='addresses')

    def __repr__(self):
        return f"<Address(id={self.id}, city={self.city}, street={self.street}, house={self.house}, user_id={self.user_id})>"

with engine.begin() as conn:
    Base.metadata.create_all(conn)


with LocalSession() as session:
    user1 = User(first_name='John', last_name='Wick', age=40, addresses=[Address(city='SPB', street='Dvinskaya', house=123),
                                                                         Address(city='Paris', street='Eleseyskaya', house=223)])
    user2 = User(first_name='Bob', last_name='Marley', age=40, addresses=[Address(city='Moskow', street='OhotniyRyad', house=3),
                                                                         Address(city='Berlin', street='Brandenburger Tor', house=1)])
    session.add(user1)
    session.add(user2)
    session.commit()

print(user1.addresses)
print(user1)