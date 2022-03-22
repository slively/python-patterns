from logging import getLogger
from time import sleep
from typing import Dict, List, Optional

from src.embedded_project.main.dir_reader.dir_reader_api import DirReaderApi
from src.embedded_project.main.dir_reader.file_model import FileModel
from src.utils.statsd_utils import statsd
from src.utils.worker_utils import BaseWorker

log = getLogger(__name__)


class Worker(BaseWorker):
    """
    A worker that continuously checks the DirReaderApi to detect new files or file changes.
    """

    _current_files: List[FileModel] = []
    new_file_count = 0
    deleted_file_count = 0
    changed_file_count = 0

    def __init__(
        self,
        stop_timeout_seconds: Optional[float],
        loop_delay_seconds: float,
        api: DirReaderApi,
    ) -> None:
        super().__init__(stop_timeout_seconds)
        self.loop_delay_seconds = loop_delay_seconds
        self.api = api

    def _current_files_by_path(self) -> Dict[str, FileModel]:
        return {file.path: file for file in self._current_files}

    def run(self) -> None:
        """
        Polls the DirReaderApi in a loop while tracking and logging any changes.
        """
        while self.running:
            change_detected = False
            previous_files_by_path = self._current_files_by_path()
            self._current_files = self.api.read_files()
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

            statsd.gauge("new_file_count", self.new_file_count)
            statsd.gauge("changed_file_count", self.changed_file_count)
            statsd.gauge("deleted_file_count", self.deleted_file_count)

            sleep(self.loop_delay_seconds)
