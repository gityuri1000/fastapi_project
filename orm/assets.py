import hashlib

from typing import List

from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_factory
from database.models import AddedAssets

from schemas.assets import SAddedAsset, SAddedAssetsResponse, SAddedAssetResponse


class AssetsRepositoryORM:
    
    @classmethod
    async def select_assets(cls, session: AsyncSession) -> SAddedAssetsResponse:
        assets = []

        stmt = (
            select(AddedAssets)
        )

        result = (await session.scalars(stmt)).all()

        for row in result:
            assets.append(SAddedAssetResponse(
                id=row.id,
                title=row.title,
                owner=row.owner
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