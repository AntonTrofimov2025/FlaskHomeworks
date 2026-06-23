from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

engine = create_engine('sqlite:///sqlalchemy_test.db')
LocalSession = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    # id = Column(Integer, primary_key=True, autoincrement=True)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int]


with engine.begin() as conn:
    Base.metadata.create_all(conn)

with LocalSession() as session:
    new_user_1 = User(first_name='John', last_name='Doe', age=23)
    new_user_2 = User(first_name='Bob', last_name='Marley', age=45)
    session.add(new_user_1)
    session.add(new_user_2)

    session.commit()

