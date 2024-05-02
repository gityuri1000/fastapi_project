import hashlib

from fastapi import HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from orm.users import UsersRepositoryORM

from schemas.users import (
    SUsersResponse, 
    SUserResponse,
    SUsername, 
    SUser
)

class UsecaseUsers:
    
    @classmethod
    async def uc_select_users(cls, session: AsyncSession) -> SUsersResponse:
        users = await UsersRepositoryORM.select_users(session=session)

        if not users:
            raise HTTPException(
                "You have no users yet",
                status_code=status.HTTP_409_CONFLICT
            )
        
        return users
    
    @classmethod
    async def uc_select_by_username(
        cls, session: AsyncSession, 
        username: SUsername
        ) -> SUserResponse:

        user = await UsersRepositoryORM.select_user_by_username(
            session, username
        )

        if not user:
            raise HTTPException(
                detail="User with this name doesnt exist",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return user
    
    @classmethod
    async def _uc_select_by_username_with_password_info(
        cls, session: AsyncSession, 
        username: SUsername
        ) -> SUser:

        user = await UsersRepositoryORM._select_user_by_username_with_password_info(
            session, username
        )

        if not user:
            raise HTTPException(
                detail="User with this name doesnt exist",
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        return user
    
    @classmethod
    async def uc_create_user(
        cls, session: AsyncSession,
        user: SUser
        ) -> SUserResponse:

        user = await UsersRepositoryORM.create_user(session, user)

        if not user:
            raise HTTPException(
                detail="This user already exits",
                status_code=status.HTTP_409_CONFLICT
            )
        
        return user 
    
    @classmethod
    async def uc_deactivate_user(
        cls, session: AsyncSession,
        user: SUser
        ) -> SUserResponse:
        hashed_password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()
        
        deactivated_user = await cls._uc_select_by_username_with_password_info(
            session=session,
            username=SUsername(username=user.username)
        )

        if deactivated_user.password != hashed_password:
            raise HTTPException(
                detail="Enter correct username and password",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        await UsersRepositoryORM.deactivate_user(
            session=session,
            user=user
        )

        return await cls.uc_select_by_username(
            session=session,
            username=SUsername(username=user.username)
        )
    
    @classmethod
    async def uc_activate_user(
        cls, session: AsyncSession,
        user: SUser
        ) -> SUserResponse:
        hashed_password = hashlib.sha256(user.password.encode('utf-8')).hexdigest()
        
        activated_user = await cls._uc_select_by_username_with_password_info(
            session=session,
            username=SUsername(username=user.username)
        )

        if activated_user.password != hashed_password:
            raise HTTPException(
                detail="Enter correct username and password",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        await UsersRepositoryORM.activate_user(
            session=session,
            user=user
        )

        return await cls.uc_select_by_username(
            session=session,
            username=SUsername(username=user.username)
        )

