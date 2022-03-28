import argparse
from queue import Queue
from typing import Any
from src.embedded_project.main.dir_reader.dir_change_event_api import (
    DirChangeEventApi,
    DirChangeEventQueue,
)
from src.embedded_project.main.dir_reader.dir_reader_ctrl import DirReaderCtrl
from src.embedded_project.main.dir_reader.dir_reader_worker_bad import (
    BadDirReaderWorker,
)
from src.embedded_project.main.dir_reader.file_model import FileModel
from src.embedded_project.main.dir_synchronizer.dir_synchronizer_ctrl import (
    DirSynchronizerCtrl,
)
from src.embedded_project.main.dir_synchronizer.dir_synchronizer_worker import (
    DirSynchronizerWorker,
)
from src.embedded_project.main.utils.common_args import add_dir_arg
from src.embedded_project.main.dir_reader.dir_reader_worker import DirReaderWorker
from src.utils.logger_utils import forwarded_logging

forwarded_logging()


def parse_args() -> Any:
    parser = argparse.ArgumentParser(description="Example embedded project daemon.")
    add_dir_arg(parser)
    parser.add_argument(
        "--sync_dir", help="Local directory to sync changes to.", required=False
    )
    parser.add_argument(
        "--stop_timout",
        help="Number of seconds to wait for workers to exit.",
        default=5.0,
        type=float,
    )
    parser.add_argument(
        "--dir_poll_interval",
        help="Number of seconds to wait while polling for directory changes.",
        default=3.0,
        type=float,
    )
    return parser.parse_args()


def bad_run() -> None:
    args = parse_args()
    worker = BadDirReaderWorker(args.dir)
    worker.start()


def run() -> None:
    args = parse_args()
    dir_reader_api = DirReaderCtrl(args.dir)
    event_api = DirChangeEventApi()

    if args.sync_dir is not None:
        queue: Queue[FileModel] = Queue()
        event_api = DirChangeEventQueue(queue)
        dir_synchronizer_api = DirSynchronizerCtrl(dir=args.sync_dir)
        DirSynchronizerWorker(
            stop_timeout_seconds=args.stop_timout, api=dir_synchronizer_api, queue=queue
        ).start()

    DirReaderWorker(
        stop_timeout_seconds=args.stop_timout,
        loop_delay_seconds=args.dir_poll_interval,
        api=dir_reader_api,
        event_api=event_api,
    ).start()


if __name__ == "__main__":
    run()
