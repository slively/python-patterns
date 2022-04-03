import argparse
from typing import Optional

from pydantic import BaseModel


class Config(BaseModel):
    hot_reload: bool
    log_level: str
    port: int
    sync_dir: str

_config: Optional[Config] = None

def get_config() -> Config:
    global _config
    if _config is not None:
        return _config

    parser = argparse.ArgumentParser(description="Run the web server.")
    parser.add_argument(
        "--hot_reload", help="activate hot reloading.", action="store_true"
    )
    parser.add_argument(
        "--log_level",
        help="Level of logging.",
        default="info",
        type=str,
    )
    parser.add_argument(
        "--port",
        help="server port.",
        default=8080,
        type=int,
    )
    parser.add_argument(
        "--sync_dir", help="Directory to sync.", type=str, required=True
    )
    args = parser.parse_args()
    _config = Config.parse_obj(args.__dict__)
    return _config 
