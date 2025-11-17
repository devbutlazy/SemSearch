from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    SESSION_NAME: str  # Telethon Session Name
    API_ID: int  # Telegram API ID from core.telegram.org
    API_HASH: str  # Telegram API HASH from core.telegram.org

    CHAT_ID: int  # The target chat id
    STRICTNESS_THRESHOLD: float  # Search strictness threshold

    POSTGRES_HOST: str  # PostgreSQL host
    POSTGRES_PORT: int  # PostgreSQL port
    POSTGRES_DB: str  # Database name
    POSTGRES_USER: str  # Database user
    POSTGRES_PASSWORD: str  # Database password

    @property
    def DB_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def SYNC_DB_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
