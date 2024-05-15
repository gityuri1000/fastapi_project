from fastapi import FastAPI

from routers.auth import auth
from routers.users import users
from routers.added_assets import added_assets
from routers.result import result

from database.db_dependencies import Session, get_session

app = FastAPI()
app.include_router(result, prefix="/result")
app.include_router(users, prefix="/users")
app.include_router(added_assets, prefix="/added_assets")
app.include_router(auth, prefix="/auth")

app.dependency_overrides[Session] = get_session
