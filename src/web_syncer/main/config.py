from typing import Optional

from pydantic import BaseSettings


class Config(BaseSettings):
    hot_reload: bool = False
    log_level: str = "info"
    port: int = 8080
    sync_dir: str


_config: Optional[Config] = None


def get_config() -> Config:
    global _config
    if _config is not None:
        return _config

    return Config()
