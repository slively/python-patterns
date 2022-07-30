import argparse
from queue import Queue
from typing import Any, Optional
from src.file_syncer.main.dir_reader.dir_change_event_api import (
    DirChangeEventApi,
    DirChangeEventQueue,
)
from src.file_syncer.main.dir_reader.dir_reader_ctrl import DirReaderCtrl
from src.file_syncer.main.dir_reader.file_model import FileModel
from src.file_syncer.main.dir_synchronizer.dir_synchronizer_api import (
    DirSynchronizerApi,
)
from src.file_syncer.main.dir_synchronizer.dir_synchronizer_ctrl import (
    DirSynchronizerCtrl,
)
from src.file_syncer.main.dir_synchronizer.dir_synchronizer_http import (
    DirSynchronizerHttp,
)
from src.file_syncer.main.dir_synchronizer.dir_synchronizer_worker import (
    DirSynchronizerWorker,
)
from src.file_syncer.main.utils.common_args import add_dir_arg, add_sync_dir_arg
from src.file_syncer.main.dir_reader.dir_reader_worker import DirReaderWorker
from src.utils.main.logger_utils import forwarded_logging

forwarded_logging()


def parse_args() -> Any:
    parser = argparse.ArgumentParser(description="Example embedded project daemon.")
    add_dir_arg(parser)
    add_sync_dir_arg(parser)
    parser.add_argument(
        "--sync_url", help="Url for remote syncing.", required=False, type=str
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


def run() -> None:
    args = parse_args()
    dir_reader_api = DirReaderCtrl(args.dir)
    event_api = DirChangeEventApi()
    dir_synchronizer_api: Optional[DirSynchronizerApi] = None

    if args.sync_dir is not None:
        dir_synchronizer_api = DirSynchronizerCtrl(dir=args.sync_dir)
    elif args.sync_url is not None:
        dir_synchronizer_api = DirSynchronizerHttp(url=args.sync_url)

    if dir_synchronizer_api is not None:
        queue: Queue[FileModel] = Queue()
        event_api = DirChangeEventQueue(queue)
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
