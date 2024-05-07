import hashlib

from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from orm.users import UsersRepositoryORM

from usecases.base import AbstractUseCase

from dto.users import (
    UserResponseAllDTO, 
    UserResponseDTO,
    UserRequestDTO
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
    
    async def uc_deactivate(self, deactivating: UserRequestDTO) -> UserResponseDTO:
        hashed_password = hashlib.sha256(deactivating.password.encode('utf-8')).hexdigest()
        
        deactivated = await self._uc_select_by_name_with_password_info(deactivating.username)

        if deactivated.password != hashed_password:
            raise HTTPException(
                detail="Enter correct username and password",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        await self.orm.deactivate(deactivating)

        return await self.uc_select_by_name(deactivating.username)
    
    async def uc_activate(self, activating: UserRequestDTO) -> UserResponseDTO:
        hashed_password = hashlib.sha256(activating.password.encode('utf-8')).hexdigest()
        
        activated: UserRequestDTO = await self._uc_select_by_name_with_password_info(activating.username)

        if activated.password != hashed_password:
            raise HTTPException(
                detail="Enter correct username and password",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        await self.orm.activate(activating.username)

        return await self.uc_select_by_name(activating.username)
    
    async def uc_authenticate(self, authenticating: UserRequestDTO) -> UserResponseDTO:
        authenticated = await self.orm.authenticate(authenticating)

        if not authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        return authenticated
    
    async def _uc_select_by_name_with_password_info(self, name: str) -> UserRequestDTO:

        selected = await self.orm._select_by_name_with_password_info(name)

        if not selected:
            raise HTTPException(
                detail="User with this name doesnt exist",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return selected

