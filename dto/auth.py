from typing import Literal, List

from pydantic import BaseModel, ConfigDict

AuthUsername = str

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
    role: Literal["admin", "regular"]

class AuthRequestDTO(AuthResponseDTO):
    password: str
    role: List[Literal["admin", "regular"]]
    
