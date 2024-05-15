from typing import List, Literal

from datetime import datetime

from dto.base import BaseDTO

class AddedAssetBaseDTO(BaseDTO):
    figi: str
    title: str
    amount: int
    asset_type: Literal["share", "bond"]

class AddedAssetRequestDTO(AddedAssetBaseDTO):
    pass

class AddedAssetResponseDTO(AddedAssetBaseDTO):
    price: int
    last_update: datetime

class AddedAssetResponseAllDTO(BaseDTO):
    assets: List["AddedAssetResponseDTO"]
