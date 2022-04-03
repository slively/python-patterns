import argparse
from typing import Optional


_args: Optional[argparse.Namespace] = None


def parse_args() -> argparse.Namespace:
    global _args
    if _args is not None:
        return _args

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
        "--sync_dir", help="Directory to sync.", type=str, required=True
    )
    _args = parser.parse_args()
    return _args
