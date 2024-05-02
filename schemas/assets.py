from typing import Sequence, List, Union, Literal
from pydantic import BaseModel, ConfigDict, Field, UUID4

OwnerUsername = str

class SAddedAssetBase(BaseModel):
    title: str
    owner: OwnerUsername

class SAddedAsset(SAddedAssetBase):
    pass

class SAddedAssetResponse(SAddedAssetBase):
    id: int = Field(gt=0)

    model_config = ConfigDict(
        from_attributes=True
    )

class SAddedAssetsResponse(BaseModel):
    assets: List[Union[SAddedAssetResponse, None]]
