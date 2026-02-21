from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=f"{BASE_DIR}/.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "12345"
    name: str = "testTask"


    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class CorsSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CORS_",
        env_file=f"{BASE_DIR}/.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    origins: str = '["*"]'
    methods: str = '["*"]'
    headers: str = '["*"]'
    credentials: bool = True


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        env_file=f"{BASE_DIR}/.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: str = "12345"


class JWTSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="JWT_",
        env_file=f"{BASE_DIR}/.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    secret_key: str = 'change-me-in-production'
    algorithm: str = 'HS256'
    access_expire_minutes: int = 15
    refresh_expire_days: int = 7



class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    cors: CorsSettings = CorsSettings()
    redis: RedisSettings = RedisSettings()
    jwt: JWTSettings = JWTSettings()


settings = Settings()