from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    db_url: str | None = None
    # db_echo: bool = False
    db_echo: bool | None = None
    events_api_key: str | None = None
    events_base_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        # env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
