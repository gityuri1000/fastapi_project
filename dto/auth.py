from typing import Literal

from pydantic import BaseModel, ConfigDict

class AuthBaseDTO(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra="allow"
    )

class AuthTokenDTO(AuthBaseDTO):
    access_token: str
    token_type: Literal["bearer"]

class AuthResponseDTO(AuthBaseDTO):
    username: str

class AuthRequestDTO(AuthResponseDTO):
    password: str

AuthUsername = str