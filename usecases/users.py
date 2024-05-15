import hashlib

from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from orm.users import UsersRepositoryORM

from usecases.base import AbstractUseCase

from dto.users import (
    UserResponseAllDTO, 
    UserResponseDTO,
    UserRequestDTO,
)

class UsecaseUsers(AbstractUseCase):
    def __init__(self, session: AsyncSession) -> None:
        self.orm = UsersRepositoryORM(session)
    
    async def uc_select_all(self) -> UserResponseAllDTO:
        selected = await self.orm.select_all()

        if not selected:
            raise HTTPException(
                "You have no users yet",
                status_code=status.HTTP_409_CONFLICT
            )
        
        return selected
    
    async def uc_select_by_name(self, name: str) -> UserResponseDTO:
        selected = await self.orm.select_by_name(name)

        if not selected:
            raise HTTPException(
                detail="User with this name doesnt exist",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return selected
    
    async def uc_create(self, creating: UserRequestDTO) -> UserResponseDTO:

        if await self.orm.select_by_name(creating.username):

            raise HTTPException(
                detail="This user already exits",
                status_code=status.HTTP_409_CONFLICT
            )
            
        created = await self.orm.create(creating)
        
        return created 
    
    async def uc_deactivate(self, username: str) -> UserResponseDTO:        
        
        await self.uc_select_by_name(username)

        return await self.orm.deactivate(username)
    
    async def uc_activate(self, username: str) -> UserResponseDTO:        
        
        await self.uc_select_by_name(username)

        return await self.orm.activate(username)
    
    async def _uc_select_by_name_with_password_info(self, name: str) -> UserRequestDTO:
        selected = await self.orm._select_by_name_with_password_info(name)

        if not selected:
            raise HTTPException(
                detail="User with this name doesnt exist",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return selected

