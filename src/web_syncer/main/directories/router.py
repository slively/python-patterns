from fastapi import APIRouter

from src.file_syncer.main.dir_reader.directory_model import DirectoryChangesModel
from src.file_syncer.main.dir_synchronizer.dir_synchronizer_api import (
    DirSynchronizerApi,
)


class FilesRouter:
    def __init__(self, api: DirSynchronizerApi):
        self.api = api
        self.router = APIRouter()
        self.router.add_api_route(path="/sync", endpoint=self.dir_sync, methods=["POST"])

    async def dir_sync(self, changes: DirectoryChangesModel):
        return self.api.sync(changes)
