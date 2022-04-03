import argparse
from src.file_syncer.main.dir_reader.dir_reader_ctrl import DirReaderCtrl
from src.file_syncer.main.utils.common_args import add_dir_arg
from src.utils.main.cli_utils import BaseCliCommand


class ListCommand(BaseCliCommand):
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        add_dir_arg(parser)

    def run(self, args: argparse.Namespace) -> None:
        dir_reader = DirReaderCtrl(args.dir)
        for file in dir_reader.read_directory():
            print(file)
