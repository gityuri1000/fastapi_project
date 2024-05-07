from typing import List

from dto.base import BaseDTO

class AddedAssetBaseDTO(BaseDTO):
    title: str

class AddedAssetRequestDTO(AddedAssetBaseDTO):
    pass

class AddedAssetResponseDTO(AddedAssetBaseDTO):
    pass

class AddedAssetResponseAllDTO(BaseDTO):
    assets: List["AddedAssetResponseDTO"]
