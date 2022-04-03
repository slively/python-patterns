import os
from src.web_syncer.main.config import get_config
from src.web_syncer.main.dir_synchronizer.router import files_router
from fastapi import FastAPI
from pathlib import Path
import uvicorn  # type: ignore


def create_app(sync_dir: str = "./tmp") -> FastAPI:
    Path(sync_dir).mkdir(parents=True, exist_ok=True)
    app = FastAPI()
    app.include_router(files_router)
    return app


def run() -> None:
    config = get_config()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    uvicorn.run(
        "src.web_syncer.main.main:create_app",
        host="127.0.0.1",
        port=config.port,
        log_level=config.log_level,
        reload=config.hot_reload,
        reload_dirs=[dir_path],
    )


if __name__ == "__main__":
    run()
