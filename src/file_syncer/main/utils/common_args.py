import argparse


def add_dir_arg(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--dir", help="The root directory for the dir reader api.", required=True
    )
