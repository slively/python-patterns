import argparse
from src.file_syncer.main.dir_reader.dir_reader_ctrl import DirReaderCtrl
from src.file_syncer.main.utils.common_args import add_dir_arg, add_sync_dir_arg
from src.utils.main.cli_utils import BaseCliCommand


class DiffCommand(BaseCliCommand):
    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        add_dir_arg(parser)
        add_sync_dir_arg(parser, required=True)

    def run(self, args: argparse.Namespace) -> None:
        dir_files = DirReaderCtrl(args.dir).read_directory()
        sync_dir_files = DirReaderCtrl(args.sync_dir).read_directory()
        print(dir_files.diff(sync_dir_files))
