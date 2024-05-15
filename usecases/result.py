from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from usecases.base import AbstractUseCase

from api.tinkoff_api import TinkoffAPI

from dto.auth import AuthUsername
from dto.added_assets import AddedAssetResponseAllDTO
from dto.result import ResultProfileStructureDTO

from orm.result import ResultRepositoryORM

class UsecaseResult(AbstractUseCase):
    def __init__(self, session: AsyncSession) -> None:
        self.orm = ResultRepositoryORM(session)

    async def uc_update(self, loggined_user: AuthUsername) -> AddedAssetResponseAllDTO:
        to_update = await self.orm.select_all_figi(loggined_user)

        if not to_update:
            raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="You have no added instruments yet"
                )

        for instrument_id in to_update:
            price_json = await TinkoffAPI.make_price_request(instrument_id)
            price = await TinkoffAPI.get_price_from_json(price_json)

            if price:
                await self.orm.change_asset_price(instrument_id, price)

        return await self.orm.select_all_assets(loggined_user)
    
    async def uc_get_assets_structure(self, loggined_user: AuthUsername) -> ResultProfileStructureDTO:
        total_sum, share_sum, bond_sum = 0, 0, 0
        percentage_share, percentage_bond = 0, 0

        res = await self.orm.select_all_assets(loggined_user)
        
        for asset in res.assets:
            total_sum += (asset.price * asset.amount)

            if asset.asset_type == "share":
                share_sum += (asset.price * asset.amount)
            elif asset.asset_type == "bond":
                bond_sum += (asset.price * asset.amount)

        if total_sum:
            percentage_share = int((share_sum * 100) / total_sum)
            percentage_bond = 100 - percentage_share

        return ResultProfileStructureDTO(
            total=total_sum,
            share_total=share_sum,
            share_percentage=percentage_share,
            bond_total=bond_sum,
            bond_percentage=percentage_bond
        )