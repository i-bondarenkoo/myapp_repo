from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    db_url: str
    db_echo: bool = False
    events_api_key: str
    events_base_url: str


settings = Settings()
