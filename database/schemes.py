from decimal import Decimal
from typing import Optional, List
from database.config import settings
from sqlalchemy import String, ForeignKey, Numeric, Column, Integer, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id")
    )

    __table_args__ = (
        UniqueConstraint("name", "parent_id"),
    )

    children: Mapped[List["Category"]] = relationship(
        "Category",
        back_populates="parent"
    )

    parent: Mapped[Optional["Category"]] = relationship(
        "Category",
        back_populates="children",
        remote_side=[id]
    )

    @property
    def parent_name(self) -> str | None:
        return self.parent.name if self.parent else None

    @staticmethod
    def _depth_of(cat: Optional["Category"]) -> int:
        if cat is None or cat.parent_id is None:
            return 1
        return 1 + Category._depth_of(cat.parent)

    @validates("parent")
    def validate_parent_depth(self, key, parent: Optional["Category"]):
        if parent is not None and self._depth_of(parent) >= settings.MAX_CATEGORY_DEPTH:
            raise ValueError(
                f"Invalid nesting: tree is limited {settings.MAX_CATEGORY_DEPTH} levels. "
                "You can't make category with more than 2 parents"
            )
        return parent


class Company(Base):
    __tablename__ = 'company'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    adress: Mapped[str] = mapped_column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category: Mapped[Category] = relationship(backref="company")
    latitude: Mapped[Decimal] = mapped_column(
        Numeric(9, 6),
        nullable=False
    )

    longitude: Mapped[Decimal] = mapped_column(
        Numeric(9, 6),
        nullable=False
    )

