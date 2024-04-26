from typing import Sequence, List, Union, Literal
from pydantic import BaseModel, Field, UUID4

OwnerUsername = str

class SAddedAssetBase(BaseModel):
    title: str
    owner: OwnerUsername

class SAddedAsset(SAddedAssetBase):
    pass

class SAddedAssetResponse(SAddedAssetBase):
    id: int = Field(gt=0)

class SAddedAssetsResponse(BaseModel):
    assets: List[Union[SAddedAsset, None]]
