from typing import TypeVar, Generic

from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel

from abc import ABC, abstractmethod

T = TypeVar("T", bound=BaseModel)
V = TypeVar("V", bound=BaseModel)

class AbstractUseCase(ABC, Generic[T]): ...
    