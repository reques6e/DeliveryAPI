import jwt

from config import Config

class Manager():
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