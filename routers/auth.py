from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import (
    OAuth2PasswordRequestForm
)

from usecases.auth import UsecaseAuth

from database.db_dependencies import Session

from dto.auth import AuthRequestDTO, AuthTokenDTO

auth = APIRouter()

@auth.post("/token")
async def login_user(
    login_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends()
) -> AuthTokenDTO:
    authenticated = await UsecaseAuth(session).uc_authenticate(
        AuthRequestDTO(username=login_form.username, password=login_form.password, role=login_form.scopes)
    )

    acess_token = await UsecaseAuth(session).uc_create_access_token(authenticated, login_form.scopes)
    return acess_token



