from fastapi import FastAPI

from routers.users import users
from routers.assets import assets

from database.db_dependencies import Session, get_session

app = FastAPI()
app.include_router(users, prefix="/users")
app.include_router(assets, prefix="/assets")

app.dependency_overrides[Session] = get_session