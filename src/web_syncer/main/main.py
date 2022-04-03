import argparse
import os
from src.file_syncer.main.dir_synchronizer.dir_synchronizer_ctrl import (
    DirSynchronizerCtrl,
)
from src.web_syncer.main.config import parse_args
from src.web_syncer.main.directories.router import files_router
from fastapi import FastAPI
from pathlib import Path
import uvicorn


def create_app(sync_dir: str = "./tmp") -> FastAPI:
    Path(sync_dir).mkdir(parents=True, exist_ok=True)
    app = FastAPI()
    app.include_router(files_router)
    return app


def run() -> None:
    args = parse_args()
    if args.hot_reload:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        uvicorn.run(
            "src.web_syncer.main.main:create_app",
            host="127.0.0.1",
            port=args.port,
            log_level=args.log_level,
            reload=args.hot_reload,
            reload_dirs=[dir_path],
        )
    else:
        uvicorn.run(
            create_app(sync_dir=args.sync_dir),
            host="127.0.0.1",
            port=args.port,
            log_level=args.log_level,
        )


if __name__ == "__main__":
    run()
