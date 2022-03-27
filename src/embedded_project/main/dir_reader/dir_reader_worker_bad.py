from glob import glob
from logging import getLogger
import os
from posixpath import basename
from threading import Thread
from time import sleep
from typing import Dict, List

from src.embedded_project.main.dir_reader.file_model import FileModel
from src.utils.file_utils import clean_and_remake_dir
from src.utils.worker_utils import BaseWorker

log = getLogger(__name__)


class BadDirReaderWorker(BaseWorker):
    """
    A worker that continuously checks a directory for changes.
    """

    _current_files: List[FileModel] = []
    new_file_count = 0
    deleted_file_count = 0
    changed_file_count = 0

    def __init__(self, dir: str):
        self.dir = dir

    def start(self) -> None:
        log.info("Starting worker %s", self.__class__.__name__)
        self.running = True
        self._thread = Thread(target=self.run)
        self._thread.start()

    def stop(self) -> None:
        log.info("Stopping worker.")
        self.running = False
        if self._thread is not None:
            self._thread.join()

    def _current_files_by_path(self) -> Dict[str, FileModel]:
        return {file.path: file for file in self._current_files}

    def read_files(self) -> List[FileModel]:
        files = []
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

    def run(self) -> None:
        """
        Polls the DirReaderApi in a loop while tracking and logging any changes.
        """
        while self.running:
            change_detected = False
            files = []
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
            previous_files_by_path = self._current_files_by_path()
            self._current_files = files
            current_files_by_path = self._current_files_by_path()

            previous_file_paths = previous_files_by_path.keys()
            current_file_paths = current_files_by_path.keys()

            deleted_files = previous_file_paths - current_file_paths
            if len(deleted_files) > 0:
                change_detected = True
                self.deleted_file_count += 1
                log.info("Files deleted: %s", ", ".join(deleted_files))

            new_files = current_file_paths - previous_file_paths
            if len(new_files) > 0:
                change_detected = True
                self.new_file_count += 1
                log.info("Files created: %s", ", ".join(new_files))

            existing_files = current_file_paths - new_files
            changed_files = []
            for file_path in existing_files:
                previous_content = previous_files_by_path[file_path].contents
                current_content = current_files_by_path[file_path].contents
                if previous_content != current_content:
                    changed_files.append(file_path)

            if len(changed_files) > 0:
                change_detected = True
                self.changed_file_count += 1
                log.info("Files changed: %s", ", ".join(changed_files))

            if not change_detected:
                log.info("No changes detected.")

            sleep(2)
