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
        
    async def user_create(
        self,
        data: UserStructure
    ) -> bool:
        if await db.user_create(data) == True:
            # TODO update 
            # Логирование
            return True
        else:
            return False
        
    async def user_info(
        self,
        id: int
    ) -> Union[UserStructure, None]:

        rs = await db.user_info(id)
        if rs:
            return rs
        else:
            return None
        
    async def user_delete(
        self,
        id: int
    ) -> bool:

        rs = await db.user_delete(id)
        if rs:
            return rs
        else:
            return False