from decimal import Decimal
from sqlalchemy import create_engine, String, Numeric, ForeignKey, select, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

# Задача 1: Наполнение данными
# Добавьте в базу данных следующие категории и продукты
# Добавление категорий: Добавьте в таблицу categories следующие категории:
#
# Название: "Электроника", Описание: "Гаджеты и устройства."
#
# Название: "Книги", Описание: "Печатные книги и электронные книги."
#
# Название: "Одежда", Описание: "Одежда для мужчин и женщин."
#
# Добавление продуктов: Добавьте в таблицу products следующие продукты, убедившись, что каждый продукт связан с соответствующей категорией:
#
# Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника
#
# Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника
#
# Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги
#
# Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда
#
# Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда

engine = create_engine('sqlite:///hw4_db.db')

LocalSession = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(255))

    products: Mapped[list['Product']] = relationship(back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, description={self.description})>"

class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2))
    in_stock: Mapped[bool] = mapped_column(default=True)
    category_id: Mapped[int] = mapped_column(ForeignKey(Category.id, ondelete='CASCADE'))

    category: Mapped['Category'] = relationship(back_populates='products')

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, in_stock={self.in_stock}, category_id={self.category_id})>"

with engine.begin() as conn:
    Base.metadata.create_all(conn)

with LocalSession() as session:
    categories = [Category(name='Electronics', description='Gadgets and devices'),
                  Category(name='Books', description='Printed and E-Books'),
                  Category(name='Clothes', description='Clothes for men/women')]

    products_electronics = [Product(name='Smartphone', price=Decimal('299.99')),
                            Product(name='Laptop', price=Decimal('499.99'))]

    products_books = Product(name='Science fiction novel', price=Decimal('15.99'))
    products_clothes = [Product(name='Jeans', price=Decimal('40.50')),
                        Product(name='T-Shirt', price=Decimal('20.00'))]

    categories[0].products.extend(products_electronics)
    categories[1].products.append(products_books)
    categories[2].products.extend(products_clothes)

    session.add_all(categories)
    session.commit()

    query = select(Category, Product).join(Product, Category.id == Product.category_id)

    result = session.execute(query).all()

    for line in result:
        print(line)

    query = select(Product).where(Product.name == 'Smartphone')
    product = session.execute(query).scalar()
    product.price = Decimal('349.99')
    session.commit()

    print(product, sep='\n')

    query = select(Category.name, func.count(Product.id).label('products_in_category')
                   ).join(Product).group_by(Category.id, Category.name)
    result = session.execute(query).all()
    print()
    print(*(f"Category: {row.name}, Count: {row.products_in_category}" for row in result), sep='\n')

    query = select(Category.name, func.count(Product.id).label('products_in_category')
                   ).join(Product).group_by(Category.id, Category.name
                                            ).having(func.count(Product.id) > 1)
    result = session.execute(query).all()
    print()
    print(*(f"Category: {row.name}, Count: {row.products_in_category}" for row in result), sep='\n')
    for category in categories:
        session.delete(category)
    session.commit()

