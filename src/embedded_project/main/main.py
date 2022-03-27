import argparse
from typing import Any
from src.embedded_project.main.dir_reader.dir_reader_ctrl import DirReaderCtrl
from src.embedded_project.main.dir_reader.dir_reader_worker_bad import (
    BadDirReaderWorker,
)
from src.embedded_project.main.utils.common_args import add_dir_arg
from src.embedded_project.main.dir_reader.dir_reader_worker import DirReaderWorker
from src.utils.logger_utils import forwarded_logging

forwarded_logging()


def parse_args() -> Any:
    parser = argparse.ArgumentParser(description="Example embedded project daemon.")
    add_dir_arg(parser)
    return parser.parse_args()


def bad_run() -> None:
    args = parse_args()
    worker = BadDirReaderWorker(args.dir)
    worker.start()


def run() -> None:
    args = parse_args()
    dir_reader_api = DirReaderCtrl(args.dir)
    worker = DirReaderWorker(
        stop_timeout_seconds=5.0, loop_delay_seconds=3.0, api=dir_reader_api
    )
    worker.start()


if __name__ == "__main__":
    run()
