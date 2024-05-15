from typing import Annotated

from fastapi import APIRouter, Depends, status, Security
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from usecases.added_assets import UsecaseAddedAssets
from usecases.auth import UsecaseAuth

from database.db_dependencies import Session

from dto.auth import AuthUsername
from dto.added_assets import (
    AddedAssetResponseAllDTO, 
    AddedAssetResponseDTO,
    AddedAssetRequestDTO,
)

added_assets = APIRouter(tags=["Addded Assets"])

assets_scopes = ["admin", "regular"]

@added_assets.get("/select_all", response_model=AddedAssetResponseAllDTO)
async def get_all_assets(loggined_user: Annotated[AuthUsername, Security(UsecaseAuth.uc_verify_token, scopes=assets_scopes)], session: Session = Depends()):
    assets = await UsecaseAddedAssets(session).uc_select_all(loggined_user)
    
    assets = jsonable_encoder(assets)
    return JSONResponse(assets, status_code=status.HTTP_200_OK)

@added_assets.get("/select_by_title", response_model=AddedAssetResponseDTO)
async def get_asset_by_title(loggined_user: Annotated[AuthUsername, Security(UsecaseAuth.uc_verify_token, scopes=assets_scopes)], title: str, session: Session = Depends()):
    user = await UsecaseAddedAssets(session).uc_select_by_name(loggined_user, title)

    user = jsonable_encoder(user)
    return JSONResponse(user, status_code=status.HTTP_200_OK)

@added_assets.post("/add", response_model=AddedAssetResponseDTO)
async def add_asset(loggined_user: Annotated[AuthUsername, Security(UsecaseAuth.uc_verify_token, scopes=assets_scopes)], asset: Annotated[AddedAssetRequestDTO, Depends()], session: Session = Depends()):
    added = await UsecaseAddedAssets(session).uc_add(loggined_user, asset)

    added = jsonable_encoder(added)
    return JSONResponse(added, status_code=status.HTTP_201_CREATED)

@added_assets.post("/delete", response_model=AddedAssetResponseDTO)
async def delete_asset(loggined_user: Annotated[AuthUsername, Security(UsecaseAuth.uc_verify_token, scopes=assets_scopes)], title: str, session: Session = Depends()):
    deleted = await UsecaseAddedAssets(session).uc_delete(loggined_user, title)

    deleted = jsonable_encoder(deleted)
    return JSONResponse(deleted, status_code=status.HTTP_200_OK)