import argparse
from src.embedded_project.main.dir_reader.dir_reader_ctrl import DirReaderCtrl
from src.embedded_project.main.utils.common_args import add_dir_arg
from src.embedded_project.main.worker.worker import Worker
from src.utils.logger_utils import forwarded_logging

forwarded_logging()


def run() -> None:
    parser = argparse.ArgumentParser(description="Example embedded project daemon.")
    add_dir_arg(parser)
    args = parser.parse_args()

    dir_reader_api = DirReaderCtrl(args.dir)
    worker = Worker(
        stop_timeout_seconds=5.0, loop_delay_seconds=3.0, api=dir_reader_api
    )
    worker.start()


if __name__ == "__main__":
    run()
