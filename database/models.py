import uuid
from typing import List

from sqlalchemy import String, Integer, ForeignKey, UUID
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped

from database.engine import async_engine

from dto.users import UserResponseDTO

class Base(DeclarativeBase):
    pass

class Users(Base):

    __tablename__ = "users"

    id = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    username = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)
    is_active = mapped_column(Integer, default=1)
    assets: Mapped[List["AddedAssets"]] = relationship()

    def to_read_model(self) -> UserResponseDTO:
        return UserResponseDTO(
            id=self.id,
            username=self.username,
            is_active=self.is_active,
            assets=self.assets
        )

class Assets(Base):

    __tablename__ = "assets"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String, nullable=False)

class AddedAssets(Base):

    __tablename__ = "added_assets"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String, nullable=False)
    owner = mapped_column(ForeignKey("users.username"))


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
