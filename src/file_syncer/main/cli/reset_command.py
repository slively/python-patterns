import argparse
from src.file_syncer.main.dir_reader.dir_reader_ctrl import DirReaderCtrl
from src.file_syncer.main.utils.common_args import add_dir_arg
from src.utils.cli_utils import BaseCliCommand


class ResetCommand(BaseCliCommand):
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        add_dir_arg(parser)

    def run(self, args: argparse.Namespace) -> None:
        dir_reader = DirReaderCtrl(args.dir)
        dir_reader.reset()
        print(args.dir + " has been reset.")
