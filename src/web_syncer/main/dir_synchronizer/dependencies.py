import argparse
from fastapi import Depends
from src.file_syncer.main.dir_synchronizer.dir_synchronizer_api import (
    DirSynchronizerApi,
)
from src.file_syncer.main.dir_synchronizer.dir_synchronizer_ctrl import (
    DirSynchronizerCtrl,
)
from src.web_syncer.main.config import get_config


async def get_dir_sync_api(
    args: argparse.Namespace = Depends(get_config),
) -> DirSynchronizerApi:
    return DirSynchronizerCtrl(args.sync_dir)
