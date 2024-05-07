import hashlib

from typing import Union

from datetime import datetime, timedelta, timezone



from config.jwt import settings

from dto.users import UserResponseDTO
from dto.auth import Token

class UtilsAuth:

    async def get_hash_password(password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    async def complain_passwords(plain_password: str, password: str) -> bool:
        return plain_password == password
    
    
