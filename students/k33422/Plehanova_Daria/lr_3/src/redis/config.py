from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(
        env_prefix='rd_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    @property
    def url(self) -> RedisDsn:
        return f"redis://{self.host}:{self.port}/0"


settings = Settings()
