from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from src.file_syncer.main.dir_reader.directory_model import DirectoryChangesModel
from src.file_syncer.main.dir_synchronizer.dir_synchronizer_api import (
    DirSynchronizerApi,
)
from src.web_syncer.main.dir_synchronizer.dependencies import get_dir_sync_api

views_router = APIRouter()
BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@views_router.get("/")
async def root(
    request: Request,
    api: DirSynchronizerApi = Depends(get_dir_sync_api),
):
    dir_changes: List[DirectoryChangesModel] = api.list_changes()
    return templates.TemplateResponse(
        "index.html", {"request": request, "changes": jsonable_encoder(dir_changes)}
    )
