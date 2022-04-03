
from fastapi import APIRouter, Depends

from src.file_syncer.main.dir_reader.directory_model import DirectoryChangesModel
from src.file_syncer.main.dir_synchronizer.dir_synchronizer_api import (
    DirSynchronizerApi,
)
from src.web_syncer.main.directories.dependecies import get_dir_sync_api

files_router = APIRouter()

@files_router.post("/sync")
async def dir_sync(changes: DirectoryChangesModel, api: DirSynchronizerApi = Depends(get_dir_sync_api)):
    return api.sync(changes)

