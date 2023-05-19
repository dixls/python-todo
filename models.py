from sqlalchemy import Integer, String, DateTime, ForeignKey, Column, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
import datetime


class Base(DeclarativeBase):
    pass


item_tag = Table(
    """relationship table for tags to items""",
    Base.metadata,
    Column("item_id", ForeignKey("items.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Item(Base):
    """an item on the to-do list"""

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(), server_default=func.now()
    )
    status: Mapped[int] = mapped_column(Integer, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)
    tags: Mapped[List["Tag"]] = relationship(secondary=item_tag,
                                             back_populates="items")


class Tag(Base):
    """tags that you can give to your items"""

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    color: Mapped[str] = mapped_column(String(255), default="grey", nullable=False)
    items: Mapped[List["Item"]] = relationship(secondary=item_tag,
                                               back_populates="tags")


statuses = ["to-do", "done", "in-progress", "on-hold"]

priorities = ["none", "low", "medium", "high", "urgent"]
