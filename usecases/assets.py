from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from orm.assets import AssetsRepositoryORM

from schemas.assets import SAddedAssetsResponse

class UsecaseAssets:
    
    async def uc_select_assets(cls, session: AsyncSession) -> SAddedAssetsResponse:

        users = await AssetsRepositoryORM.select_assets(session=session)

        if not users:
            raise HTTPException(
                "You have no users yet",
                status_code=status.HTTP_409_CONFLICT
            )
        
        return users