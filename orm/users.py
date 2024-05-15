import hashlib

from typing import Union

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from orm.base import AbstractORM

from database.models import Users

from dto.users import (
    UserRequestDTO,
    UserResponseDTO, 
    UserResponseAllDTO,
    Username
)

class UsersRepositoryORM(AbstractORM):

    async def select_all(self) -> UserResponseAllDTO:
        stmt = select(Users).options(selectinload(Users.assets))

        res = (await self.session.execute(stmt)).scalars().all()
        
        users = [UserResponseDTO.model_validate(row, from_attributes=True) for row in res]

        return UserResponseAllDTO(users=users)
    
    async def select_by_name(self, name: str) -> Union[UserResponseDTO, None]:
        stmt = (
            select(Users).options(selectinload(Users.assets)).
            where(Users.username == name)
        )

        result = (await self.session.scalars(stmt)).one_or_none()

        if result:

            return UserResponseDTO.model_validate(result)
    
    async def create(self, creating: UserRequestDTO) -> Union[UserResponseDTO, None]:
        hashed_password = hashlib.sha256(creating.password.encode('utf-8')).hexdigest()
        
        stmt = Users(
            username=creating.username,
            password=hashed_password
        )

        self.session.add(stmt)
        await self.session.flush()

        return await self.select_by_name(creating.username)
                
    async def deactivate(self, username: str) -> Union[UserResponseDTO, None]:
        stmt = (
            update(Users).
            where(Users.username == username).
            values(is_active = 0)
        )

        await self.session.execute(stmt)
        return await self.select_by_name(username)

    async def activate(self, username: str) -> Union[UserResponseDTO, None]:
        stmt = (
            update(Users).
            where(Users.username == username).
            values(is_active = 1)
        )

        await self.session.execute(stmt)
        return await self.select_by_name(username)

    async def _select_by_name_with_password_info(self, name: str) -> Union[UserRequestDTO, None]:
        stmt = (
            select(Users).options(selectinload(Users.assets)).
            where(Users.username == name)
        )

        result = (await self.session.scalars(stmt)).first()

        if result:

            return UserRequestDTO.model_validate(result)
