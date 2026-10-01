from sqlalchemy import Integer, String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(180), index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float)
    tags: Mapped[str] = mapped_column(String(300), default="")
