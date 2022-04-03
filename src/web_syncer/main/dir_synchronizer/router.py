from typing import List
from fastapi import APIRouter, Depends

from src.file_syncer.main.dir_reader.directory_model import DirectoryChangesModel
from src.file_syncer.main.dir_synchronizer.dir_synchronizer_api import (
    DirSynchronizerApi,
)
from src.web_syncer.main.dir_synchronizer.dependencies import get_dir_sync_api

files_router = APIRouter()


@files_router.post("/sync")
async def dir_sync(
    changes: DirectoryChangesModel, api: DirSynchronizerApi = Depends(get_dir_sync_api)
):
    return api.sync(changes)


@files_router.get("/changes")
async def list_changes(
    api: DirSynchronizerApi = Depends(get_dir_sync_api),
) -> List[DirectoryChangesModel]:
    return api.list_changes()
