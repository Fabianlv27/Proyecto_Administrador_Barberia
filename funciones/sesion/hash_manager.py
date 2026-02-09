from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashManager:
    @staticmethod
    def crear_hash(password: str) -> str:
        print(f"Hashing password: {password}")  # Debug: Ver el password antes de hashear
        return pwd_context.hash(password)

    @staticmethod
    def verificar_hash(password_plano: str, password_hasheado: str) -> bool:
        return pwd_context.verify(password_plano, password_hasheado)