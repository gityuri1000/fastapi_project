import hashlib

from typing import Union

from sqlalchemy import select

from orm.base import AbstractORM

from database.models import Users

from dto.auth import (
    AuthResponseDTO,
    AuthRequestDTO
)

class AuthRepositoryORM(AbstractORM):

    async def authenticate(self, authenticating: AuthRequestDTO) -> Union[AuthResponseDTO]:
        hash_password = hashlib.sha256(authenticating.password.encode('utf-8')).hexdigest()

        stmt = (
            select(Users).
            where(Users.username == authenticating.username).
            where(Users.password == hash_password).
            where(Users.role == authenticating.role[0])
        )

        authenticated = (await self.session.scalars(stmt)).one_or_none()

        if authenticated:
            return AuthResponseDTO.model_validate(authenticated)
        