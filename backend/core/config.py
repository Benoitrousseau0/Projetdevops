from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL_LOCAL: str
    DATABASE_URL_DOCKER: str
    USE_DOCKER: bool = False

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    @property
    def DATABASE_URL(self) -> str:
        return self.DATABASE_URL_DOCKER if self.USE_DOCKER else self.DATABASE_URL_LOCAL

    class Config:
        env_file = ".env"


settings = Settings()
