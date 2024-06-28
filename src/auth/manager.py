import jwt

from auth.models import UserStructure

from typing import Optional, Union

from database import DataBase
from config import Config

db = DataBase()


class UserManager():
    def __init__(self) -> None:
        pass

    @staticmethod
    def jwt_generate(
        payload: dict,
        hash: str = Config.JWT_HASH
    ) -> str:
        return jwt.encode(
            payload=payload,
            key=Config.JWT_SECRET,
            algorithm=hash
        )
    
    @staticmethod
    def jwt_decipher(
        token: str,
        hash: str = Config.JWT_HASH
    ) -> str:
        try:
            return jwt.decode(
                    jwt=token,
                    key=Config.JWT_SECRET,
                    algorithms=[hash]
                )
        except jwt.InvalidTokenError as e:
            return False