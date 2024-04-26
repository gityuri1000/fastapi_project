import hashlib

from typing import List

from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_factory
from database.models import AddedAssets

from schemas.assets import SAddedAsset, SAddedAssetResponse, SAddedAssetsResponse


class AssetsRepositoryORM:
    
    @classmethod
    async def select_assets(cls, session: AsyncSession) -> List[SAddedAssetResponse]:
        assets = []

        stmt = (
            select(AddedAssets)
        )

        result = await session.scalars(stmt)

        for row in result:
            row.__dict__.pop("_sa_instance_state")
            assets.append(SAddedAsset(
                id=row.__dict__["id"],
                title=row.__dict__["title"],
                owner=row.__dict__["owner"]
                )
            )

        return SAddedAssetsResponse(assets=assets)
              

    @classmethod
    async def create_asset(cls, session: AsyncSession, asset: SAddedAsset) -> SAddedAsset:
        stmt = AddedAssets(
            title=asset.title,
            owner=asset.owner
        )

        session.add(stmt)

        return asset