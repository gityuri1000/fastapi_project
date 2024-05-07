from typing import TypeVar, Generic

from abc import ABC, abstractmethod

from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=BaseModel)
V = TypeVar("V", bound=BaseModel)

class AbstractORM(ABC, Generic[T]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    