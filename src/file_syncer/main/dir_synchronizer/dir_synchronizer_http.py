from logging import getLogger
from typing import List
from pydantic import parse_obj_as

import requests
from src.file_syncer.main.dir_reader.directory_model import DirectoryChangesModel
from src.file_syncer.main.dir_synchronizer.dir_synchronizer_api import (
    DirSynchronizerApi,
)

log = getLogger(__name__)


class DirSynchronizerHttp(DirSynchronizerApi):
    def __init__(self, url: str) -> None:
        self.url = url

    def sync(self, changes: DirectoryChangesModel) -> None:
        requests.post(self.url + "/sync", data=changes.json())

    def list_changes(self) -> List[DirectoryChangesModel]:
        json = requests.get(self.url + "/changes").json
        return parse_obj_as(List[DirectoryChangesModel], json)
