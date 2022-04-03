import argparse
import os
from src.file_syncer.main.dir_synchronizer.dir_synchronizer_ctrl import (
    DirSynchronizerCtrl,
)
from src.web_syncer.main.directories.router import FilesRouter
from fastapi import FastAPI
from pathlib import Path
import uvicorn


def create_app(sync_dir: str = "./tmp") -> FastAPI:
    Path(sync_dir).mkdir(parents=True, exist_ok=True)
    app = FastAPI()
    api = DirSynchronizerCtrl(sync_dir)
    fr = FilesRouter(api)
    app.include_router(fr.router)
    return app


def parse_args() -> argparse.Namespace:
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
        "--sync_dir",
        help="Directory to sync.",
        type=str,
        required=True
    )
    return parser.parse_args()


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
