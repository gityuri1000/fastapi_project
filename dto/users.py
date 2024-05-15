from typing import Sequence, List, Literal
from pydantic import UUID4, ConfigDict

from dto.base import BaseDTO
from dto.added_assets import AddedAssetResponseDTO

Username = str

class UserBaseDTO(BaseDTO):
    username: str

class UserRequestDTO(UserBaseDTO):
    password: str

class UserResponseDTO(UserBaseDTO):
    id: UUID4
    role: Literal["admin", "regular"]
    is_active: Literal[0, 1]
    assets: List["AddedAssetResponseDTO"]

class UserResponseAllDTO(BaseDTO):
    users: Sequence["UserResponseDTO"]