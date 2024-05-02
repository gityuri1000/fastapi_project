from typing import Sequence, List, Union, Literal
from pydantic import BaseModel, ConfigDict, UUID4

from schemas.assets import SAddedAssetResponse

class SUserBase(BaseModel):
    username: str

class SUsername(SUserBase):
    pass

class SUser(SUserBase):
    password: str

class SUserResponse(SUserBase):
    id: UUID4
    is_active: Literal[0, 1]
    assets: List[Union[SAddedAssetResponse, None]]

class SUsersResponse(BaseModel):
    users: Sequence[SUserResponse]