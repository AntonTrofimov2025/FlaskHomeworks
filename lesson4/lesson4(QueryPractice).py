import random
from datetime import datetime
from decimal import Decimal
from sqlalchemy import create_engine, String, Integer, CheckConstraint, Numeric, ForeignKey, DateTime, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship, validates

from faker import Faker


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


class TimestampMixin:
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)


class User(Base):
    __tablename__ = 'users'
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(CheckConstraint('age >= 18 AND age <= 60'))

    orders: Mapped[list['Order']] = relationship(back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User(id={self.id}, name={self.name}, age={self.age})>'


class Order(Base, TimestampMixin):
    __tablename__ = 'orders'
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship(back_populates='orders')

    @validates('amount')
    def validate_amount(self, key, amount):
        if amount <= 0:
            raise ValueError('Amount must be positive')
        return amount

    def __repr__(self):
        return f'<Order(id={self.id}, amount={self.amount}, user_id={self.user_id})>'

engine = create_engine('sqlite:///users_orders.db')

with engine.begin() as conn:
    Base.metadata.create_all(conn)

LocalSession = sessionmaker(bind=engine)

fake = Faker()

with LocalSession() as session:
    # users = [User(name=fake.name(), age=random.randint(18, 60)) for _ in range(30)]
    #
    # session.add_all(users)
    # session.flush()
    #
    # orders = [Order(amount=Decimal(random.randint(10, 100)) ,user_id=random.choice(users).id) for _ in range(60)]
    # session.add_all(orders)

    session.commit()
    query = select(User, Order).join(Order, User.id == Order.user_id)
    # result = session.execute(query).all()
    # for line1, line2 in result:
    #     print(line1, line2)
    result = session.execute(query).all()
    print(*result, sep='\n')

# with LocalSession() as session:
#     subquery = session.execute()

