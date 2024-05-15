from typing import Annotated, List

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from sqlalchemy.ext.asyncio import AsyncSession

from config.jwt import jwt_settings

from orm.auth import AuthRepositoryORM

from dto.auth import (
    AuthResponseDTO,
    AuthRequestDTO,
    AuthTokenDTO,
    AuthUsername
)

from usecases.base import AbstractUseCase

class UsecaseAuth(AbstractUseCase):

    oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl="/auth/token",
        scopes={"admin": "User with root permissions", "regular": "Regular user acess"}
    )


    def __init__(self, session: AsyncSession) -> None:
        self.orm = AuthRepositoryORM(session)

    async def uc_authenticate(self, authenticating: AuthRequestDTO) -> AuthResponseDTO:
        if len(authenticating.role) != 1:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Must be selected one role always"
            )

        authenticated = await self.orm.authenticate(authenticating)

        if not authenticated:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        
        return authenticated
    
    async def uc_create_access_token(self, data: AuthResponseDTO, security_scopes: List[str]) -> AuthTokenDTO:
        to_encode = {"sub": data.username, "scopes": security_scopes}
        expire = datetime.now(timezone.utc) + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM)
        
        return AuthTokenDTO(
            access_token=encoded_jwt,
            token_type="bearer"
        )
    
    @classmethod
    async def uc_verify_token(self, security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]) -> AuthUsername:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM])
            username: str = payload.get("sub")
            scopes: list = payload.get("scopes", [])

            if username is None:
                raise credentials_exception
            
        except JWTError:
            raise credentials_exception
        
        for scope in scopes:
            if scope not in security_scopes.scopes:
                raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": "Bearer-scope"},
            )
                
        return username
        
        