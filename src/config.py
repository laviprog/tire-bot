from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    BOT_TOKEN: str

    REDIS_HOST: str
    REDIS_PORT: int

    PG_HOST: str
    PG_PORT: int
    PG_NAME: str
    PG_USER: str
    PG_PASSWORD: str

    MAX_RECORDS: int = 10
    OPERATING_MODE: str = "10-20"
    CONTACT_INFORMATION: dict = {
        "phone": "+79684280033",
        "username": "@CyberMot_Top",
        "name": "Cybermoto",
    }

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def PG_URL(self):
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}"


settings = Settings()
