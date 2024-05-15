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
    
    async def select_by_name(self, title: str, owner: str) -> Union[AddedAssetResponseDTO, None]:
        stmt = (
            select(AddedAssets).
            where(AddedAssets.title == title).
            where(AddedAssets.owner == owner)
        )

        result = (await self.session.scalars(stmt)).one_or_none()

        if result:

            return AddedAssetResponseDTO.model_validate(result)
              

    async def add(self, loggined_user: AuthUsername, asset: AddedAssetRequestDTO) -> AddedAssetRequestDTO:
        stmt = AddedAssets(
            figi=asset.figi,
            title=asset.title,
            amount=asset.amount,
            asset_type=asset.asset_type,
            owner=loggined_user
        )

        self.session.add(stmt)

        return asset
    
    async def delete(self, loggined_user: AuthUsername, title: str) -> AddedAssetRequestDTO:
        deleted = await self.select_by_name(title, loggined_user)

        stmt = (
            delete(AddedAssets).
            where(AddedAssets.title == title).
            where(AddedAssets.owner == loggined_user)
        )

        await self.session.execute(stmt)

        return deleted
    

