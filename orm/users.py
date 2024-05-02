import hashlib

from typing import Union

from fastapi import status

from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Users

from schemas.assets import SAddedAssetResponse
from schemas.users import (
    SUser,
    SUserResponse, 
    SUsersResponse,
    SUsername,
)

class UsersRepositoryORM:
    
    @classmethod
    async def create_user(cls, session: AsyncSession, user: SUser) -> Union[SUserResponse, None]:
        hashed_password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()
        
        exist: Union[SUserResponse, None] = await cls.select_user_by_username(
            session, 
            SUsername(username=user.username)
            )
        
        if not exist:
            stmt = Users(
                username=user.username,
                password=hashed_password
            )

            session.add(stmt)
            await session.flush()

            return await cls.select_user_by_username(session, SUsername(username=user.username))
                
    @classmethod
    async def deactivate_user(cls, session: AsyncSession, user: SUser) -> None:
        stmt = (
            update(Users).
            where(Users.username == user.username).
            values(is_active = 0)
        )

        await session.execute(stmt)        

    @classmethod
    async def activate_user(cls, session: AsyncSession, user: SUser) -> None:
        stmt = (
            update(Users).
            where(Users.username == user.username).
            values(is_active = 1)
        )

        await session.execute(stmt)

    
    @classmethod
    async def select_users(cls, session: AsyncSession) -> SUsersResponse:
        users = []

        stmt = select(Users).options(selectinload(Users.assets))
        result = (await session.scalars(stmt)).all()
        
        for row in result:

            assets = [SAddedAssetResponse.model_validate(asset) for asset in row.assets]

            users.append(SUserResponse(
                id=row.id,
                username=row.username,
                is_active=row.is_active,
                assets=assets
                )
            )

        return SUsersResponse(users=users)
        
    @classmethod
    async def select_user_by_username(cls, session: AsyncSession, username: SUsername) -> Union[SUserResponse, None]:
        stmt = (
            select(Users).options(selectinload(Users.assets)).
            where(Users.username == username.username)
        )

        result = (await session.scalars(stmt)).first()

        if result:

            assets = [SAddedAssetResponse.model_validate(asset) for asset in result.assets]

            return SUserResponse(
                id=result.id,
                username=result.username,
                is_active=result.is_active,
                assets=assets
            )

    @classmethod
    async def _select_user_by_username_with_password_info(cls, session: AsyncSession, username: SUsername) -> Union[SUser, None]:
        stmt = (
            select(Users).options(selectinload(Users.assets)).
            where(Users.username == username.username)
        )

        result = (await session.scalars(stmt)).first()

        if result:

            return SUser(
                username=result.username,
                password=result.password
            )
