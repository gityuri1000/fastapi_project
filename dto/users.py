from typing import Sequence, List, Literal
from pydantic import UUID4

from dto.base import BaseDTO
from dto.added_assets import AddedAssetResponseDTO

class UserBaseDTO(BaseDTO):
    username: str

class UserRequestDTO(UserBaseDTO):
    password: str

class UserResponseDTO(UserBaseDTO):
    id: UUID4
    is_active: Literal[0, 1]
    assets: List["AddedAssetResponseDTO"]

class UserResponseAllDTO(BaseDTO):
    users: Sequence["UserResponseDTO"]