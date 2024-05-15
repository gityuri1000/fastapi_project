from typing import List

from sqlalchemy import select, update, func

from orm.base import AbstractORM

from database.models import AddedAssets

from dto.auth import AuthUsername
from dto.result import InstrumentID
from dto.added_assets import (
    AddedAssetResponseAllDTO,
    AddedAssetResponseDTO
)

class ResultRepositoryORM(AbstractORM):

    async def select_all_assets(self, loggined_user: AuthUsername) -> AddedAssetResponseAllDTO:
        stmt = (
            select(AddedAssets).
            where(AddedAssets.owner == loggined_user)
        )

        res = (await self.session.execute(stmt)).scalars().all()

        assets = [AddedAssetResponseDTO.model_validate(row, from_attributes=True) for row in res]

        return AddedAssetResponseAllDTO(assets=assets)

    async def select_all_figi(self, loggined_user: AuthUsername) -> List[InstrumentID]:
        stmt = (
            select(AddedAssets).
            where(AddedAssets.owner == loggined_user)
        )

        assets = (await self.session.execute(stmt)).scalars().all()

        return [row.figi for row in assets]

    async def change_asset_price(self, figi: InstrumentID, new_price: int) -> None:
        stmt = (
            update(AddedAssets).
            where(AddedAssets.figi == figi).
            values(
                price = new_price,
                last_update = func.now()
            )
        )

        await self.session.execute(stmt)
    

            