from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from orm.added_assets import AddedAssetsRepositoryORM

from dto.auth import AuthUsername
from dto.added_assets import (
    AddedAssetResponseAllDTO, 
    AddedAssetResponseDTO,
    AddedAssetRequestDTO
)

from usecases.base import AbstractUseCase

class UsecaseAddedAssets(AbstractUseCase):
    def __init__(self, session: AsyncSession) -> None:
        self.orm = AddedAssetsRepositoryORM(session)
    
    async def uc_select_all(self, loggined_user: AuthUsername) -> AddedAssetResponseAllDTO:

        assets = await self.orm.select_all(loggined_user)

        if not assets:
            raise HTTPException(
                "You have no assets yet",
                status_code=status.HTTP_409_CONFLICT
            )
        
        return assets
    
    async def uc_select_by_name(self, owner, title: str) -> AddedAssetResponseDTO:

        selected = await self.orm.select_by_name(title, owner)

        if not selected:
            raise HTTPException(
                detail="Asset with this name doesnt exist",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return selected

    async def uc_add(self, loggined_user: AuthUsername, adding: AddedAssetRequestDTO) -> AddedAssetResponseDTO:

        if await self.orm.select_by_name(adding.title, loggined_user):

            raise HTTPException(
                detail="This user already have asset with that name",
                status_code=status.HTTP_409_CONFLICT
            )
            
        added = await self.orm.add(loggined_user, adding)
        
        return added 

    async def uc_delete(self, loggined_user: AuthUsername, title: str) -> AddedAssetResponseDTO:
        asset = await self.uc_select_by_name(loggined_user, title)

        if not asset:
            raise HTTPException(
                detail="Asset with name doesnt exist",
                status_code=status.HTTP_409_CONFLICT
            )
        
        deleted = await self.orm.delete(loggined_user, title)

        return deleted
