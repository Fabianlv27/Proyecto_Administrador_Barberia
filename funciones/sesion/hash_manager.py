from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashManager:
    @staticmethod
    def crear_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verificar_hash(password_plano: str, password_hasheado: str) -> bool:
        return pwd_context.verify(password_plano, password_hasheado)