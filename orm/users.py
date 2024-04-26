import hashlib

from fastapi import HTTPException, status

from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_factory
from database.models import Users

from schemas.assets import SAddedAsset
from schemas.users import (
    SUser,
    SUserBase,
    SUserResponse, 
    SUsersResponse,
    SUsername,
)

class UsersRepositoryORM:
    
    @classmethod
    async def create_user(cls, session: AsyncSession, user: SUser) -> SUserResponse:
        hashed_password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()
        
        if await cls.select_user_by_username(
                session=session, 
                username=SUsername(username=user.username)
            ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )

        stmt = Users(
            username=user.username,
            password=hashed_password
        )

        session.add(stmt)
        await session.flush()
        await session.refresh(stmt)

        return SUserResponse(
            id=stmt.id, 
            username=stmt.username,
            is_active=stmt.is_active,
            assets=[]
        )

    @classmethod
    async def deactivate_user(cls, session: AsyncSession, username: SUsername) -> SUserResponse:


        stmt = (
            update(Users).
            where(Users.username == username.username).
            values(is_active = 0)
        )

        await session.execute(stmt)

        response = await cls.select_user_by_username(session=session, username=username)

        return response

    @classmethod
    async def activate_user(cls, session: AsyncSession, username: SUsername) -> SUserResponse:
        stmt = (
            update(Users).
            where(Users.username == username.username).
            values(is_active = 1)
        )

        await session.execute(stmt)

        response = await cls.select_user_by_username(session=session, username=username)

        return response
    
    @classmethod
    async def delete_user(cls, session: AsyncSession, user: SUser) -> SUserResponse:
        hashed_password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()

        stmt = (
            delete(Users).
            where(Users.username == user.username).
            where(Users.password == hashed_password)
        )

        await session.execute(stmt)

        return SUser(username=user.username, password=hashed_password)

    @classmethod
    async def select_users(cls, session: AsyncSession) -> SUsersResponse:
        users = []

        stmt = select(Users).options(selectinload(Users.assets))
        result = await session.scalars(stmt)
        
        for row in result:
            row.__dict__.pop("_sa_instance_state")

            assets = [SAddedAsset(**asset.__dict__) for asset in row.__dict__["assets"]]

            users.append(SUserResponse(
                id=row.__dict__["id"],
                username=row.__dict__["username"],
                is_active=row.__dict__["is_active"],
                assets=assets
                )
            )

        return SUsersResponse(users=users)
        
    @classmethod
    async def select_user_by_username(cls, session: AsyncSession, username: SUsername) -> SUserResponse:
        stmt = (
            select(Users).options(selectinload(Users.assets)).
            where(Users.username == username.username)
        )

        result = await session.scalars(stmt)
        result = result.first()

        if not result:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User doesn't exist",
            )

        return SUserResponse(
            id=result.id,
            username=result.username,
            is_active=result.is_active,
            assets=result.assets
        )

