from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from usecases.users import UsecaseUsers
from usecases.auth import UsecaseAuth

from database.db_dependencies import Session

from dto.auth import AuthTokenDTO
from dto.users import (
    UserResponseAllDTO,
    UserResponseDTO, 
    UserRequestDTO,
)

users = APIRouter(tags=["Users"])

@users.get("/select_all", response_model=UserResponseAllDTO)
async def get_all_users(session: Session = Depends()):
    users = await UsecaseUsers(session).uc_select_all()

    print(users)
    users = jsonable_encoder(users)
    return JSONResponse(users, status_code=status.HTTP_200_OK)

@users.get("/select_by_username", response_model=UserResponseDTO)
async def get_user_by_username(username: str, session: Session = Depends()):
    user = await UsecaseUsers(session).uc_select_by_name(username)

    user = jsonable_encoder(user)
    return JSONResponse(user, status_code=status.HTTP_200_OK)

@users.post("/create", response_model=UserResponseDTO)
async def create_user(user: Annotated[UserRequestDTO, Depends()], session: Session = Depends()):

    added = await UsecaseUsers(session).uc_create(user)

    added = jsonable_encoder(added)
    return JSONResponse(added, status_code=status.HTTP_201_CREATED)

@users.put("/deactivate", response_model=UserResponseDTO)
async def deactivate_user(user: Annotated[UserRequestDTO, Depends()], session: Session = Depends()):
    deactivated = await UsecaseUsers(session).uc_deactivate(user)

    deactivated = jsonable_encoder(deactivated)
    return JSONResponse(deactivated, status_code=status.HTTP_200_OK)

@users.put("/activate", response_model=UserResponseDTO)
async def activate_user(user: Annotated[UserRequestDTO, Depends()], session: Session = Depends()):
    activated = await UsecaseUsers(session).uc_activate(user)

    activated = jsonable_encoder(activated)
    return JSONResponse(activated, status_code=status.HTTP_200_OK)



    