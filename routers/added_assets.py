from typing import Annotated

from fastapi import APIRouter, Depends, status
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

@added_assets.get("/select_all", response_model=AddedAssetResponseAllDTO)
async def get_all_assets(loggined_user: Annotated[AuthUsername, Depends(UsecaseAuth.verify_token)], session: Session = Depends()):
    assets = await UsecaseAddedAssets(session).uc_select_all(loggined_user)
    
    assets = jsonable_encoder(assets)
    return JSONResponse(assets, status_code=status.HTTP_200_OK)

@added_assets.post("/add", response_model=AddedAssetResponseDTO)
async def add_asset(loggined_user: Annotated[AuthUsername, Depends(UsecaseAuth.verify_token)], asset: Annotated[AddedAssetRequestDTO, Depends()], session: Session = Depends()):
    added = await UsecaseAddedAssets(session).uc_add(loggined_user, asset)

    added = jsonable_encoder(added)
    return JSONResponse(added, status_code=status.HTTP_201_CREATED)