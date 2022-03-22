from glob import glob
from os import mkdir
import os
from posixpath import basename
from typing import List

from src.embedded_project.main.dir_reader.dir_reader_api import DirReaderApi
from src.embedded_project.main.dir_reader.file_model import FileModel
from src.utils.file_utils import clean_and_remake_dir
from src.utils.statsd_utils import statsd


class DirReaderCtrl(DirReaderApi):
    def __init__(self, dir: str) -> None:
        self.dir = dir

    def read_files(self) -> List[FileModel]:
        files = []
        with statsd.timer("read_files"):
            paths = glob(self.dir + "/**", recursive=True)

            for p in paths:
                if os.path.isdir(p):
                    files.append(
                        FileModel(path=p, name=basename(p), contents="", is_dir=True)
                    )
                else:
                    with open(p, mode="r") as f:
                        files.append(
                            FileModel(
                                path=p,
                                name=basename(p),
                                is_dir=False,
                                contents=f.read(),
                            )
                        )
        return files

    def reset(self) -> None:
        clean_and_remake_dir(self.dir)
