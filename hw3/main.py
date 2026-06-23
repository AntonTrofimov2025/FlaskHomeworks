# Задача 1.
# Создайте экземпляр движка для подключения к SQLite базе данных в памяти.

# Задача 2.
# Создайте сессию для взаимодействия с базой данных, используя созданный движок.

# Задача 3.
# Определите модель продукта Product со следующими типами колонок:
# ● id: числовой идентификатор
# ● name: строка (макс. 100 символов)
# ● price: числовое значение с фиксированной точностью
# ● in_stock: логическое значение

# Задача 4.
# Определите связанную модель категории Category со следующими типами колонок:
# ● id: числовой идентификатор
# ● name: строка (макс. 100 символов)
# ● description: строка (макс. 255 символов)

# Задача 5.
# Установите связь между таблицами Product и Category с помощью колонки category_id.

from decimal import Decimal
from sqlalchemy import create_engine, String, Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

engine = create_engine('sqlite:///:memory:')

LocalSession = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    in_stock: Mapped[bool]
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))

    category: Mapped['Category'] = relationship(back_populates='products')

    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price}, in_stock={self.in_stock}, category_id={self.category_id})>"

class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))

    products: Mapped[list[Product]] = relationship(back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Category(name={self.name}, description={self.description})>"

with engine.begin() as conn:
    Base.metadata.create_all(conn)

with LocalSession() as session:
    category_1 = Category(name='Dairy', description="It's all about milk products :)")
    category_2 = Category(name='Groceries', description="Here you'll find all our groceries!")

    product_1 = Product(name='milk', price=129.99, in_stock=True)
    product_2 = Product(name='Rice', price=59.99, in_stock=False)

    category_1.products.append(product_1)
    category_2.products.append(product_2)

    session.add(category_1)
    session.add(category_2)

    session.commit()

print(category_1)
print(category_1.products)
print(category_2)
print(category_2.products)

