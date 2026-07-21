from datetime import datetime
from sqlalchemy import Column, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    store_name = Column(Text, default="")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(Text, nullable=False)
    cost_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, nullable=False)
    product_name = Column(Text, nullable=False)
    quantity = Column(Integer, nullable=False)
    sell_price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=False)
    profit = Column(Float, nullable=False)
    created_at = Column(Text, default=lambda: datetime.now().isoformat())
