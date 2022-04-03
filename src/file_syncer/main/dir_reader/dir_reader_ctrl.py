from glob import glob
import os
from posixpath import basename

from src.file_syncer.main.dir_reader.dir_reader_api import DirReaderApi
from src.file_syncer.main.dir_reader.directory_model import DirectoryModel
from src.file_syncer.main.dir_reader.file_model import FileModel
from src.utils.main.file_utils import clean_and_remake_dir
from src.utils.main.statsd_utils import statsd


class DirReaderCtrl(DirReaderApi):
    """
    The real implementation of DirReaderApi that uses glob to get all files in a directory.
    """

    def __init__(self, dir: str) -> None:
        self.dir = dir

    def read_directory(self) -> DirectoryModel:
        files = []
        with statsd.timer("read_files"):
            paths = glob(self.dir + "/**", recursive=True)

            for p in paths:
                name = basename(p)
                path_relative_to_root = os.path.relpath(p, self.dir)

                # skip the root dir
                if path_relative_to_root == ".":
                    continue
                elif os.path.isdir(p):
                    files.append(
                        FileModel(
                            path=path_relative_to_root,
                            name=name,
                            contents="",
                            is_dir=True,
                        )
                    )
                else:
                    with open(p, mode="r") as f:
                        files.append(
                            FileModel(
                                path=path_relative_to_root,
                                name=name,
                                is_dir=False,
                                contents=f.read(),
                            )
                        )

        return DirectoryModel(files=files)

    def reset(self) -> None:
        clean_and_remake_dir(self.dir)
