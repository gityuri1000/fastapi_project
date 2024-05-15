from typing import Annotated

from fastapi import APIRouter, Security, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from database.db_dependencies import Session

from usecases.auth import UsecaseAuth
from usecases.result import UsecaseResult

from dto.auth import AuthUsername
from dto.added_assets import AddedAssetResponseAllDTO
from dto.result import ResultProfileStructureDTO

result = APIRouter(tags=["Result"])

result_scopes = ["admin", "regular"]

@result.post("/update", response_model=AddedAssetResponseAllDTO)
async def update(loggined_user: Annotated[AuthUsername, Security(UsecaseAuth.uc_verify_token, scopes=result_scopes)], session: Session = Depends()):
    assets = await UsecaseResult(session).uc_update(loggined_user)

    assets = jsonable_encoder(assets)
    return JSONResponse(assets, status_code=status.HTTP_200_OK)

@result.post("/structure", response_model=ResultProfileStructureDTO)
async def get_assets_structure(loggined_user: Annotated[AuthUsername, Security(UsecaseAuth.uc_verify_token, scopes=result_scopes)], session: Session = Depends()):
    structure = await UsecaseResult(session).uc_get_assets_structure(loggined_user)

    structure = jsonable_encoder(structure)
    return JSONResponse(structure, status_code=status.HTTP_200_OK)