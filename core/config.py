from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    SESSION_NAME: str  # Telethon Session Name
    API_ID: int  # Telegram API ID from core.telegram.org
    API_HASH: str  # Telegram API HASH from core.telegram.org

    CHAT_ID: int  # The target chat id

    DB_HOST: str  # PostgreSQL host
    DB_PORT: int  # PostgreSQL port
    DB_NAME: str  # Database name
    DB_USER: str  # Database user
    DB_PASS: str  # Database password

    @property
    def DB_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def SYNC_DB_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
