import argparse


def add_dir_arg(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--dir", help="The root directory for the dir reader api.", required=True
    )

def add_sync_dir_arg(parser: argparse.ArgumentParser, required: bool = False):
    parser.add_argument(
        "--sync_dir", help="Local directory to sync changes to.", required=required
    )
