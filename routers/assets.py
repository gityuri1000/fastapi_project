from typing import Annotated, List

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from orm.assets import AssetsRepositoryORM
from database.db_dependencies import Session

from schemas.assets import SAddedAssetsResponse, SAddedAsset

assets = APIRouter(tags=["Assets"])

@assets.get("/select_all", response_model=SAddedAssetsResponse)
async def get_all_users(session: Session = Depends()):
    assets = await AssetsRepositoryORM.select_assets(session)
    
    assets = jsonable_encoder(assets)
    return JSONResponse(assets, status_code=status.HTTP_200_OK)

@assets.post("/create")
async def create_user(asset: Annotated[SAddedAsset, Depends()], session: Session = Depends()):
    added = await AssetsRepositoryORM.create_asset(
        session=session,
        asset=asset
    )

    added = jsonable_encoder(added)
    return JSONResponse(added, status_code=status.HTTP_201_CREATED)