from typing import Union

from sqlalchemy import select, delete, update

from database.models import AddedAssets

from orm.base import AbstractORM

from dto.auth import AuthUsername
from dto.added_assets import (
    AddedAssetRequestDTO, 
    AddedAssetResponseDTO,
    AddedAssetResponseAllDTO
)


class AddedAssetsRepositoryORM(AbstractORM):
    
    async def select_all(self, loggined_user: AuthUsername) -> AddedAssetResponseAllDTO:
        stmt = select(AddedAssets).where(AddedAssets.owner == loggined_user)

        res = (await self.session.execute(stmt)).scalars().all()
        
        assets = [AddedAssetResponseDTO.model_validate(row, from_attributes=True) for row in res]

        return AddedAssetResponseAllDTO(assets=assets)
    
    async def select_by_name(self, name: str, owner: str) -> Union[AddedAssetResponseDTO, None]:
        stmt = (
            select(AddedAssets).
            where(AddedAssets.title == name).
            where(AddedAssets.owner == owner)
        )

        result = (await self.session.scalars(stmt)).one_or_none()

        if result:

            return AddedAssetResponseDTO.model_validate(result)
              

    async def add(self, loggined_user: AuthUsername, asset: AddedAssetRequestDTO) -> AddedAssetRequestDTO:
        stmt = AddedAssets(
            title=asset.title,
            owner=loggined_user
        )

        self.session.add(stmt)

        return asset