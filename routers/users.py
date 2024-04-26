from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from orm.users import UsersRepositoryORM
from database.db_dependencies import Session

from schemas.users import SUsersResponse, SUser, SUserResponse, SUsername

users = APIRouter(tags=["Users"])

@users.get("/select_all", response_model=SUsersResponse)
async def get_all_users(session: Session = Depends()):
    users = await UsersRepositoryORM.select_users(session)
    users = jsonable_encoder(users)
    return JSONResponse(users, status_code=status.HTTP_200_OK)

@users.get("/select_by_username", response_model=SUserResponse)
async def get_user_by_username(username: Annotated[SUsername, Depends()], session: Session = Depends()):
    user = await UsersRepositoryORM.select_user_by_username(
        session=session,
        username=username
    )
    user = jsonable_encoder(user)
    return JSONResponse(user, status_code=status.HTTP_200_OK)

@users.post("/create", response_model=SUserResponse)
async def create_user(user: Annotated[SUser, Depends()], session: Session = Depends()):

    added = await UsersRepositoryORM.create_user(
        session,
        user=user
    )

    added = jsonable_encoder(added)
    return JSONResponse(added, status_code=status.HTTP_201_CREATED)

@users.delete("/delete")
async def remove_user(user: Annotated[SUser, Depends()], session: Session = Depends()):
    removed = await UsersRepositoryORM.delete_user(
        session,
        user=user
    )

    removed = jsonable_encoder(removed)
    return JSONResponse(removed, status_code=status.HTTP_200_OK)

@users.put("/deactivate", response_model=SUserResponse)
async def deactivate_user(username: Annotated[SUsername, Depends()], session: Session = Depends()):
    deactivated = await UsersRepositoryORM.deactivate_user(
        session=session,
        username=username
    )

    deactivated = jsonable_encoder(deactivated)
    return JSONResponse(deactivated, status_code=status.HTTP_200_OK)

@users.put("/activate", response_model=SUserResponse)
async def activate_user(username: Annotated[SUsername, Depends()], session: Session = Depends()):
    activated = await UsersRepositoryORM.activate_user(
        session,
        username=username
    )

    activated = jsonable_encoder(activated)
    return JSONResponse(activated, status_code=status.HTTP_200_OK)
