from typing import Sequence, List, Union, Literal
from pydantic import BaseModel, Field, UUID4

from schemas.assets import SAddedAsset

class SUserBase(BaseModel):
    username: str

class SUsername(SUserBase):
    pass

class SUser(SUserBase):
    password: str

class SUserResponse(SUserBase):
    id: UUID4
    is_active: Literal[0, 1]
    assets: List[Union[SAddedAsset, None]]

class SUsersResponse(BaseModel):
    users: Sequence[SUserResponse]